# # ml_driver.py
# import os
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from category_encoders import TargetEncoder
# from sklearn.metrics import mean_absolute_error, r2_score
# from scipy.interpolate import make_interp_spline

# PERSISTENT_DIR = "/home/ecd515/Desktop/PASS/Code/src/persistent"

# def adjusted_sq_efficiency(row):
#     base_eff = 0.337 * (row['Bandgap'] / 1.34) * np.exp(-(row['Bandgap'] - 1.34)**2 / 0.1)
#     if row.get('Composition_Type_Zn'): base_eff *= 1.05
#     if row.get('Composition_Type_Br'): base_eff *= 0.95
#     if row.get('Composition_Type_FA'): base_eff *= 1.07
#     if row.get('Composition_Type_EA'): base_eff *= 0.92
#     return np.clip(base_eff * 0.90 * 0.95 * 0.97 * 100, 0, 100)

# def run_model():
#     data_path = "/home/ecd515/Desktop/PASS/Code/src/PL_VALUES.xlsx"
#     data = pd.read_excel(data_path)

#     data['Bandgap'] = 1240 / data['Wavelength'].replace(0, np.nan)
#     data.dropna(subset=['Bandgap'], inplace=True)
#     data['Composition_Value'] = data['Ink Composition %'].str.extract(r'(\d+)')[0].astype(float).fillna(0)
#     data['Composition_Type_original'] = data['Ink Composition %']
#     data['Composition_Type_Zn'] = data['Composition_Type_original'].str.contains("Zn")
#     data['Composition_Type_Br'] = data['Composition_Type_original'].str.contains("Br")
#     data['Composition_Type_FA'] = data['Composition_Type_original'].str.contains("FA")
#     data['Composition_Type_EA'] = data['Composition_Type_original'].str.contains("EA")

#     ink_enc = TargetEncoder(cols=['Ink'])
#     add_enc = TargetEncoder(cols=['Additive'])
#     comp_enc = TargetEncoder(cols=['Composition_Type_original'])
#     data['Ink_encoded'] = ink_enc.fit_transform(data['Ink'], data['Bandgap'])
#     data['Additive_encoded'] = add_enc.fit_transform(data['Additive'], data['Bandgap'])
#     data['Composition_Type_encoded'] = comp_enc.fit_transform(data['Composition_Type_original'], data['Bandgap'])

#     X = data[['Intensity', 'Ink Concentration [M]', 'Composition_Value', 'Ink_encoded', 'Additive_encoded', 'Composition_Type_encoded']]
#     y = data['Bandgap']
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     rf = RandomForestRegressor(n_estimators=100, random_state=42)
#     rf.fit(X_train, y_train)
#     y_pred = rf.predict(X_test)
#     data['Adjusted_SQ_Efficiency'] = data.apply(adjusted_sq_efficiency, axis=1)

#     # Feature Importance
#     plt.figure()
#     plt.barh(X.columns, rf.feature_importances_)
#     plt.title("Feature Importance")
#     plt.tight_layout()
#     plt.savefig(os.path.join(PERSISTENT_DIR, "Feature Importance.png"))
#     plt.close()

#     # Actual vs Predicted
#     y_pred_all = rf.predict(X)
#     plt.figure()
#     plt.scatter(y, y_pred_all, alpha=0.6)
#     plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
#     plt.title("Actual vs Predicted Bandgap")
#     plt.tight_layout()
#     plt.savefig(os.path.join(PERSISTENT_DIR, "Actual vs Predicted Bandgap.png"))
#     plt.close()

#     # Residuals
#     residuals = y - y_pred_all
#     plt.figure()
#     sns.kdeplot(residuals, fill=True)
#     plt.title("Density Distribution of Residuals")
#     plt.tight_layout()
#     plt.savefig(os.path.join(PERSISTENT_DIR, "Density Distribution of Residuals.png"))
#     plt.close()

#     # SQ Limit Plot
#     sq_curve = 0.337 * (np.linspace(0.9, 2.1, 500) / 1.34) * np.exp(-(np.linspace(0.9, 2.1, 500) - 1.34)**2 / 0.15) * 100
#     grouped = data.groupby('Bandgap')['Adjusted_SQ_Efficiency'].mean().reset_index()
#     spline = make_interp_spline(grouped['Bandgap'], grouped['Adjusted_SQ_Efficiency'], k=3)
#     x_smooth = np.linspace(grouped['Bandgap'].min(), grouped['Bandgap'].max(), 300)
#     y_smooth = spline(x_smooth)

#     plt.figure()
#     plt.plot(np.linspace(0.9, 2.1, 500), sq_curve, label="SQ Limit", color='black')
#     plt.plot(x_smooth, y_smooth, label="ML Curve", color='blue')
#     plt.scatter(data['Bandgap'], data['Adjusted_SQ_Efficiency'], color='green', alpha=0.5, label="Samples")
#     plt.axvline(1.34, color='red', linestyle='--', label="Ideal")
#     plt.legend()
#     plt.xlabel("Bandgap (eV)")
#     plt.ylabel("Efficiency (%)")
#     plt.title("SQ Limit vs ML Prediction")
#     plt.grid()
#     plt.tight_layout()
#     plt.savefig(os.path.join(PERSISTENT_DIR, "sq_limit_with_all_samples.png"))
#     plt.close()

#     # Efficiency Distribution
#     plt.figure()
#     sns.histplot(data['Adjusted_SQ_Efficiency'], bins=30, kde=True, color="green")
#     plt.title("Adjusted Efficiency Distribution")
#     plt.tight_layout()
#     plt.savefig(os.path.join(PERSISTENT_DIR, "adjusted_efficiency_distribution.png"))
#     plt.close()
