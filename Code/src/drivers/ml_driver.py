# -*- coding: utf-8 -*-
"""
ml_driver.py

Standalone ML module for PASS. Runs the model and saves all output plots.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from category_encoders import TargetEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.interpolate import make_interp_spline
from bayes_opt import BayesianOptimization

# --- Efficiency Function ---
def adjusted_sq_efficiency(row):
    base_eff = 0.337 * (row['Bandgap'] / 1.34) * np.exp(-(row['Bandgap'] - 1.34)**2 / 0.1)
    if row.get('Composition_Type_Zn'): base_eff *= 1.05
    if row.get('Composition_Type_Br'): base_eff *= 0.95
    if row.get('Composition_Type_FA'): base_eff *= 1.07
    if row.get('Composition_Type_EA'): base_eff *= 0.92
    η_total = 0.90 * 0.95 * 0.97
    return np.clip(base_eff * η_total * 100, 0, 100)

# --- Main ML Logic ---
def main():
    print("[MLDriver] Starting model...")

    base_dir = "/home/ecd515/Desktop/PASS/src"
    data_path = os.path.join(base_dir, "PL_VALUES.xlsx")

    data = pd.read_excel(data_path)
    data['Bandgap'] = 1240 / data['Wavelength'].replace(0, np.nan)
    data.dropna(subset=['Bandgap'], inplace=True)

    data['Composition_Value'] = data['Ink Composition %'].str.extract(r'(\d+)')[0].astype(float).fillna(0)
    data['Composition_Type_original'] = data['Ink Composition %']
    data['Composition_Type_Zn'] = data['Composition_Type_original'].str.contains("Zn")
    data['Composition_Type_Br'] = data['Composition_Type_original'].str.contains("Br")
    data['Composition_Type_FA'] = data['Composition_Type_original'].str.contains("FA")
    data['Composition_Type_EA'] = data['Composition_Type_original'].str.contains("EA")

    ink_encoder = TargetEncoder(cols=['Ink'])
    additive_encoder = TargetEncoder(cols=['Additive'])
    comp_encoder = TargetEncoder(cols=['Composition_Type_original'])

    data['Ink_encoded'] = ink_encoder.fit_transform(data['Ink'], data['Bandgap'])
    data['Additive_encoded'] = additive_encoder.fit_transform(data['Additive'], data['Bandgap'])
    data['Composition_Type_encoded'] = comp_encoder.fit_transform(data['Composition_Type_original'], data['Bandgap'])

    X = data[['Intensity', 'Ink Concentration [M]', 'Composition_Value', 'Ink_encoded', 'Additive_encoded', 'Composition_Type_encoded']]
    y = data['Bandgap']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)

    print("MAE:", mean_absolute_error(y_test, y_pred))
    print("R2:", r2_score(y_test, y_pred))

    data['Adjusted_SQ_Efficiency'] = data.apply(adjusted_sq_efficiency, axis=1)

    # === PLOTTING ===
    # 1. Feature Importance
    plt.figure(figsize=(8, 5))
    plt.barh(X.columns, rf.feature_importances_)
    plt.title("Feature Importance")
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, "Feature Importance.png"))
    plt.close()

    # 2. Actual vs Predicted Bandgap
    y_pred_all = rf.predict(X)
    plt.figure(figsize=(8, 6))
    plt.scatter(y, y_pred_all, alpha=0.6, c='blue', label='Data')
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title("Actual vs Predicted Bandgap")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, "Actual vs Predicted Bandgap.png"))
    plt.close()

    # 3. Residual Distribution
    residuals = y - y_pred_all
    plt.figure(figsize=(8, 6))
    sns.kdeplot(residuals, fill=True)
    plt.title("Density Distribution of Residuals")
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, "Density Distribution of Residuals.png"))
    plt.close()

    # 4. SQ Limit Curve with Samples
    bandgap_values = np.linspace(0.9, 2.1, 500)
    sq_eff = 0.337 * (bandgap_values / 1.34) * np.exp(-(bandgap_values - 1.34)**2 / 0.15) * 100
    grouped = data.groupby('Bandgap')['Adjusted_SQ_Efficiency'].mean().reset_index()
    x = grouped['Bandgap'].values
    y_smooth = grouped['Adjusted_SQ_Efficiency'].values
    x_smooth = np.linspace(x.min(), x.max(), 300)
    spline = make_interp_spline(x, y_smooth, k=3)
    y_spline = spline(x_smooth)

    plt.figure(figsize=(10, 6))
    plt.plot(bandgap_values, sq_eff, label="SQ Limit", color='black')
    plt.plot(x_smooth, y_spline, label="ML Curve", color='blue')
    plt.scatter(data['Bandgap'], data['Adjusted_SQ_Efficiency'], color='green', s=30, alpha=0.6, label="Samples")
    plt.axvline(x=1.34, color='red', linestyle='--', label="Ideal Bandgap")
    plt.legend()
    plt.xlabel("Bandgap (eV)")
    plt.ylabel("Efficiency (%)")
    plt.title("SQ Limit vs ML Prediction")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, "sq_limit_with_all_samples.png"))
    plt.close()

    # 5. Adjusted Efficiency Distribution
    plt.figure(figsize=(8, 6))
    sns.histplot(data['Adjusted_SQ_Efficiency'], bins=30, kde=True, color='green')
    plt.title("Adjusted Efficiency Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, "adjusted_efficiency_distribution.png"))
    plt.close()

    print("[MLDriver] All plots saved to:", base_dir)

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main()
