# -*- coding: utf-8 -*-
"""
ml_driver.py

Standalone driver version of InkAdditiveRFR.py to be called directly from GUI.
"""

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

def adjusted_sq_efficiency(row):
    base_eff = 0.337 * (row['Bandgap'] / 1.34) * np.exp(-(row['Bandgap'] - 1.34)**2 / 0.1)
    if 'Composition_Type_Zn' in row and row['Composition_Type_Zn']:
        base_eff *= 1.05
    if 'Composition_Type_Br' in row and row['Composition_Type_Br']:
        base_eff *= 0.95
    if 'Composition_Type_FA' in row and row['Composition_Type_FA']:
        base_eff *= 1.07
    if 'Composition_Type_EA' in row and row['Composition_Type_EA']:
        base_eff *= 0.92
    η_total = 0.90 * 0.95 * 0.97
    return np.clip(base_eff * η_total * 100, 0, 100)

def main():
    # Load dataset
    data = pd.read_excel("/home/ecd515/Desktop/PASS/src/PL_VALUES.xlsx")

    # Bandgap calculation
    data['Bandgap'] = 1240 / data['Wavelength'].replace(0, np.nan)
    data.dropna(subset=['Bandgap'], inplace=True)

    data['Composition_Value'] = data['Ink Composition %'].str.extract(r'(\d+)')[0].astype(float).fillna(0)
    data['Composition_Type_original'] = data['Ink Composition %']
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

    print("Model trained.")
    print("MAE:", mean_absolute_error(y_test, y_pred))
    print("R2:", r2_score(y_test, y_pred))

    data['Adjusted_SQ_Efficiency'] = data.apply(adjusted_sq_efficiency, axis=1)

    plt.figure(figsize=(8, 6))
    sns.histplot(data['Adjusted_SQ_Efficiency'], bins=30, kde=True)
    plt.title("Efficiency Distribution")
    plt.savefig("adjusted_efficiency_distribution.png")
    plt.close()

    print("Finished ML run and saved plots.")

if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    main()
