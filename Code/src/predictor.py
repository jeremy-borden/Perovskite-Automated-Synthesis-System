import pickle
import numpy as np
import pandas as pd

# --- Load model and encoders ---
with open("ml_models/random_forest_model.pkl", "rb") as f:
    rf_model = pickle.load(f)

with open("ml_models/ink_encoder.pkl", "rb") as f:
    ink_encoder = pickle.load(f)

with open("ml_models/additive_encoder.pkl", "rb") as f:
    additive_encoder = pickle.load(f)

with open("ml_models/composition_encoder.pkl", "rb") as f:
    composition_encoder = pickle.load(f)

# --- Adjusted SQ Efficiency Formula ---
def adjusted_sq_efficiency(row):
    base_eff = 0.337 * (row['Bandgap'] / 1.34) * np.exp(-(row['Bandgap'] - 1.34)**2 / 0.1)
    if row.get('Composition_Type_Zn', 0): base_eff *= 1.05
    if row.get('Composition_Type_Br', 0): base_eff *= 0.95
    if row.get('Composition_Type_FA', 0): base_eff *= 1.07
    if row.get('Composition_Type_EA', 0): base_eff *= 0.92
    return np.clip(base_eff * 100, 0, 100)

# --- Bandgap + Efficiency Prediction ---
def predict_bandgap_and_efficiency(intensity, ink, additive, concentration, composition_value, composition_type):
    try:
        row = pd.DataFrame([{
            'Intensity': intensity,
            'Ink Concentration [M]': concentration,
            'Composition_Value': composition_value,
            'Ink': ink,
            'Additive': additive,
            'Composition_Type_original': composition_type,
            'Composition_Type_Zn': int('Zn' in composition_type),
            'Composition_Type_Br': int('Br' in composition_type),
            'Composition_Type_FA': int('FA' in composition_type),
            'Composition_Type_EA': int('EA' in composition_type)
        }])

        # Encode categorical features
        row['Ink_encoded'] = ink_encoder.transform(row[['Ink']])
        row['Additive_encoded'] = additive_encoder.transform(row[['Additive']])
        row['Composition_Type_encoded'] = composition_encoder.transform(row[['Composition_Type_original']])

        # Prepare input features
        features = row[['Intensity', 'Ink Concentration [M]', 'Composition_Value',
                        'Ink_encoded', 'Additive_encoded', 'Composition_Type_encoded']]

        # Predict bandgap
        bandgap = rf_model.predict(features)[0]
        row['Bandgap'] = bandgap

        # Predict efficiency
        efficiency = adjusted_sq_efficiency(row.iloc[0])

        return bandgap, efficiency
    except Exception as e:
        print(f"[Prediction Error] {e}")
        return None, None
