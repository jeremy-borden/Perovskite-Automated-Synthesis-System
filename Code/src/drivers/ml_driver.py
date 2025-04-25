import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from category_encoders import TargetEncoder
from sklearn.metrics import mean_absolute_error, r2_score
from scipy.interpolate import make_interp_spline
from bayes_opt import BayesianOptimization
import warnings
import contextlib
import io

warnings.filterwarnings("ignore")

PERSISTANT_DIR = os.path.join(os.path.dirname(__file__), "..", "persistant")

def adjusted_sq_efficiency(row):
    base_eff = 0.337 * (row['Bandgap'] / 1.34) * np.exp(-(row['Bandgap'] - 1.34)**2 / 0.1)
    if row.get('Composition_Type_Zn'): base_eff *= 1.05
    if row.get('Composition_Type_Br'): base_eff *= 0.95
    if row.get('Composition_Type_FA'): base_eff *= 1.07
    if row.get('Composition_Type_EA'): base_eff *= 0.92
    η_total = 0.90 * 0.95 * 0.97
    return np.clip(base_eff * η_total * 100, 0, 100)

def run_model():
    data_path = os.path.join(os.path.dirname(__file__), "..", "PL_VALUES.xlsx")
    data = pd.read_excel(data_path)

    data['Bandgap'] = 1240 / data['Wavelength'].replace(0, np.nan)
    data.dropna(subset=['Bandgap'], inplace=True)
    data['Composition_Value'] = data['Ink Composition %'].str.extract(r'(\d+)')[0].astype(float).fillna(0)
    data['Composition_Type_original'] = data['Ink Composition %']
    data['Composition_Type_Zn'] = data['Composition_Type_original'].str.contains("Zn")
    data['Composition_Type_Br'] = data['Composition_Type_original'].str.contains("Br")
    data['Composition_Type_FA'] = data['Composition_Type_original'].str.contains("FA")
    data['Composition_Type_EA'] = data['Composition_Type_original'].str.contains("EA")

    ink_enc = TargetEncoder(cols=['Ink'])
    add_enc = TargetEncoder(cols=['Additive'])
    comp_enc = TargetEncoder(cols=['Composition_Type_original'])

    data['Ink_encoded'] = ink_enc.fit_transform(data['Ink'], data['Bandgap'])
    data['Additive_encoded'] = add_enc.fit_transform(data['Additive'], data['Bandgap'])
    data['Composition_Type_encoded'] = comp_enc.fit_transform(data['Composition_Type_original'], data['Bandgap'])

    X = data[['Intensity', 'Ink Concentration [M]', 'Composition_Value',
              'Ink_encoded', 'Additive_encoded', 'Composition_Type_encoded']]
    y = data['Bandgap']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    data['Adjusted_SQ_Efficiency'] = data.apply(adjusted_sq_efficiency, axis=1)

    if not os.path.exists(PERSISTANT_DIR):
        os.makedirs(PERSISTANT_DIR)

    # Feature Importance
    plt.figure(figsize=(8, 6), dpi=150)
    plt.barh(X.columns, rf.feature_importances_, color='steelblue')
    plt.xlabel("Importance")
    plt.title("Feature Importance")
    plt.tight_layout()
    plt.savefig(os.path.join(PERSISTANT_DIR, "Feature Importance.png"), bbox_inches="tight")
    plt.close()

    # Actual vs Predicted Bandgap
    y_pred_all = rf.predict(X)
    plt.figure(figsize=(8, 6), dpi=150)
    plt.scatter(y, y_pred_all, alpha=0.6, edgecolor=None, c='blue', label='All Data')
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2, label='Prediction Line')
    plt.xlabel("Actual Bandgap")
    plt.ylabel("Predicted Bandgap")
    plt.title("Actual vs Predicted Bandgap")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(PERSISTANT_DIR, "Actual vs Predicted Bandgap.png"), bbox_inches="tight")
    plt.close()

    # Residuals
    residuals = y - y_pred_all
    plt.figure(figsize=(8, 6), dpi=150)
    sns.kdeplot(residuals, fill=True, color="cornflowerblue", linewidth=2)
    plt.axvline(0, linestyle="--", color="red", label="Zero Error Line")
    plt.title("Density Distribution of Residuals")
    plt.xlabel("Residuals")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(PERSISTANT_DIR, "Density Distribution of Residuals.png"), bbox_inches="tight")
    plt.close()

    # Adjusted Efficiency Histogram
    plt.figure(figsize=(8, 6), dpi=150)
    sns.histplot(data['Adjusted_SQ_Efficiency'], bins=30, kde=True, color="green", edgecolor="black")
    plt.xlabel("Adjusted SQ Efficiency (%)")
    plt.ylabel("Count")
    plt.title("Adjusted SQ Efficiency Distribution")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(PERSISTANT_DIR, "adjusted_efficiency_distribution.png"), bbox_inches="tight")
    plt.close()

    # Shockley–Queisser Limit vs Dataset Curve
    bandgap_values = np.linspace(0.4, 3.0, 500)
    sq_eff = 0.337 * (bandgap_values / 1.34) * np.exp(-(bandgap_values - 1.34) ** 2 / 0.15) * 100
    filtered = data.dropna(subset=['Bandgap', 'Adjusted_SQ_Efficiency'])
    grouped = filtered.groupby('Bandgap', as_index=False)['Adjusted_SQ_Efficiency'].mean()
    grouped = grouped.sort_values('Bandgap')

    if len(grouped) >= 4:
        x = grouped['Bandgap'].values
        y_smooth = grouped['Adjusted_SQ_Efficiency'].values
        spline = make_interp_spline(x, y_smooth, k=3)
        x_smooth = np.linspace(x.min(), x.max(), 300)
        y_smooth = spline(x_smooth)
    else:
        x_smooth = grouped['Bandgap'].values
        y_smooth = grouped['Adjusted_SQ_Efficiency'].values

    plt.figure(figsize=(8, 6), dpi=150)
    plt.plot(bandgap_values, sq_eff, color='black', linewidth=2, label="Shockley–Queisser Limit (Ideal)")
    plt.plot(x_smooth, y_smooth, color='blue', linewidth=2.2, label="Interpolated Dataset Efficiency")
    plt.scatter(filtered['Bandgap'], filtered['Adjusted_SQ_Efficiency'], color='green', s=35, alpha=0.5, label="Dataset Samples")
    plt.axvline(x=1.34, color='red', linestyle='--', label="Optimal Bandgap (1.34 eV)")
    plt.xlabel("Bandgap (eV)")
    plt.ylabel("Efficiency (%)")
    plt.title("Solar Efficiency: Dataset Samples vs Shockley–Queisser Limit")
    plt.xlim(0.9, 2.1)
    plt.ylim(0, 40)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PERSISTANT_DIR, "sq_limit_with_all_samples.png"), bbox_inches="tight")
    plt.close()

    # Print sorted efficiency summary
    summary = filtered[['Bandgap', 'Adjusted_SQ_Efficiency']].copy().sort_values('Bandgap')
    print("\nEfficiency Summary Table:\n", summary.to_string(index=False))

    # Top 3 Samples
    top3 = data.nlargest(3, 'Adjusted_SQ_Efficiency')[['Ink', 'Additive', 'Ink Concentration [M]', 'Composition_Type_original', 'Adjusted_SQ_Efficiency']]
    print("\nTop 3 Efficient Samples from Dataset:")
    print(top3.to_string(index=False))

    # Bayesian Optimization
    best_result = None
    best_eff = 0
    compositions = data['Composition_Type_original'].dropna().unique()
    inks = data['Ink'].dropna().unique()
    additives = data['Additive'].dropna().unique()

    for comp_type in compositions:
        for ink in inks:
            for additive in additives:
                comp_val = float(''.join(filter(str.isdigit, comp_type))) if any(char.isdigit() for char in comp_type) else 0

                def objective(Intensity, Ink_Concentration):
                    sample = pd.DataFrame([{
                        'Intensity': Intensity,
                        'Ink Concentration [M]': Ink_Concentration,
                        'Composition_Value': comp_val,
                        'Ink': ink,
                        'Additive': additive,
                        'Composition_Type_original': comp_type
                    }])
                    sample['Ink_encoded'] = ink_enc.transform(sample[['Ink']])
                    sample['Additive_encoded'] = add_enc.transform(sample[['Additive']])
                    sample['Composition_Type_encoded'] = comp_enc.transform(sample[['Composition_Type_original']])
                    X_synth = sample[['Intensity', 'Ink Concentration [M]', 'Composition_Value',
                                      'Ink_encoded', 'Additive_encoded', 'Composition_Type_encoded']]
                    sample['Bandgap'] = rf.predict(X_synth)[0]
                    sample['Composition_Type_Zn'] = 'Zn' in comp_type
                    sample['Composition_Type_Br'] = 'Br' in comp_type
                    sample['Composition_Type_FA'] = 'FA' in comp_type
                    sample['Composition_Type_EA'] = 'EA' in comp_type
                    return adjusted_sq_efficiency(sample.iloc[0])

                with contextlib.redirect_stdout(io.StringIO()):
                    optimizer = BayesianOptimization(
                        f=objective,
                        pbounds={
                            'Intensity': (1000, 2000000),
                            'Ink_Concentration': (1.0, 1.3)
                        },
                        random_state=42
                    )
                    optimizer.maximize(init_points=2, n_iter=5)

                if optimizer.max['target'] > best_eff:
                    best_eff = optimizer.max['target']
                    best_result = {
                        "Composition_Type": comp_type,
                        "Ink": ink,
                        "Additive": additive,
                        "params": optimizer.max['params'],
                        "efficiency": best_eff
                    }

    print("\n[Bayesian Optimization Result]")
    print(f"Best Composition Type: {best_result['Composition_Type']}")
    print(f"Ink Used: {best_result['Ink']}")
    print(f"Additive Used: {best_result['Additive']}")
    print(f"Intensity: {best_result['params']['Intensity']:.4f}")
    print(f"Ink_Concentration: {best_result['params']['Ink_Concentration']:.4f}")
    print(f"Predicted Efficiency: {best_result['efficiency']:.2f}%")

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    run_model()
