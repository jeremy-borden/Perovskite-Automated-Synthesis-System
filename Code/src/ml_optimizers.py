import pickle
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

# Load model + encoders
with open("ml_models/random_forest_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("ml_models/ink_encoder.pkl", "rb") as f:
    ink_encoder = pickle.load(f)
with open("ml_models/additive_encoder.pkl", "rb") as f:
    additive_encoder = pickle.load(f)
with open("ml_models/composition_encoder.pkl", "rb") as f:
    composition_encoder = pickle.load(f)

# Efficiency function
def adjusted_sq_efficiency(row):
    base_eff = 0.337 * (row['Bandgap'] / 1.34) * np.exp(-(row['Bandgap'] - 1.34)**2 / 0.1)
    if row.get('Composition_Type_Zn', 0): base_eff *= 1.05
    if row.get('Composition_Type_Br', 0): base_eff *= 0.95
    if row.get('Composition_Type_FA', 0): base_eff *= 1.07
    if row.get('Composition_Type_EA', 0): base_eff *= 0.92
    return np.clip(base_eff * 100, 0, 100)

# Optimization logic
def genetic_algorithm(n_generations=10, population_size=20):
    param_space = {
        'Intensity': (500000, 1600000),
        'Ink_Concentration': (1.0, 1.3),
        'Composition_Value': (0, 30),
        'Ink': ['FASnI3', 'MASnI3', 'mix'],
        'Additive': ['Br', 'Zn', 'MA', 'EASCN', '4-MePEABr', '0'],
        'Composition_Type': ['10% Br', '10% Zn', 'Baseline', '10% EA', '20% Br']
    }

    def create_individual():
        return {
            'Intensity': random.uniform(*param_space['Intensity']),
            'Ink Concentration [M]': random.uniform(*param_space['Ink_Concentration']),
            'Composition_Value': random.uniform(*param_space['Composition_Value']),
            'Ink': random.choice(param_space['Ink']),
            'Additive': random.choice(param_space['Additive']),
            'Composition_Type_original': random.choice(param_space['Composition_Type'])
        }

    def evaluate(individual):
        try:
            row = pd.DataFrame([{
                **individual,
                'Composition_Type_Zn': int('Zn' in individual['Composition_Type_original']),
                'Composition_Type_Br': int('Br' in individual['Composition_Type_original']),
                'Composition_Type_FA': int('FA' in individual['Composition_Type_original']),
                'Composition_Type_EA': int('EA' in individual['Composition_Type_original'])
            }])
            row['Ink_encoded'] = ink_encoder.transform(row[['Ink']])
            row['Additive_encoded'] = additive_encoder.transform(row[['Additive']])
            row['Composition_Type_encoded'] = composition_encoder.transform(row[['Composition_Type_original']])
            X = row[['Intensity', 'Ink Concentration [M]', 'Composition_Value',
                     'Ink_encoded', 'Additive_encoded', 'Composition_Type_encoded']]
            bandgap = model.predict(X)[0]
            row['Bandgap'] = bandgap
            efficiency = adjusted_sq_efficiency(row.iloc[0])
            return efficiency, bandgap
        except Exception as e:
            return -1, -1

    population = [create_individual() for _ in range(population_size)]
    best = None
    best_score = -1

    for _ in range(n_generations):
        scored = []
        for ind in population:
            eff, bg = evaluate(ind)
            ind['Efficiency'] = eff
            ind['Bandgap'] = bg
            scored.append((eff, ind))
        scored.sort(reverse=True)
        population = [ind for _, ind in scored[:population_size]]
        best = population[0]
        best_score = best['Efficiency']

        # Create new gen with mutation
        new_pop = []
        for _ in range(population_size):
            p1, p2 = random.sample(population[:10], 2)
            child = {k: p1[k] if random.random() < 0.5 else p2[k] for k in p1}
            if random.random() < 0.1:  # mutation
                child = create_individual()
            new_pop.append(child)
        population = new_pop

    return best

# Suggest Top 5 Recipes
def get_top_5_recipes(n=50):
    results = []
    for _ in range(n):
        try:
            result = genetic_algorithm(n_generations=5, population_size=15)
            results.append(result)
        except Exception as e:
            print(f"[Optimization Error] {e}")
    results.sort(key=lambda x: x['Efficiency'], reverse=True)
    return results[:5]

# Plot Feature Importance
def plot_feature_importance():
    labels = ['Intensity', 'Ink Conc', 'Comp Value', 'Ink_enc', 'Add_enc', 'Comp_enc']
    values = model.feature_importances_

    plt.figure(figsize=(6, 4))
    plt.barh(labels, values)
    plt.xlabel("Importance")
    plt.title("Random Forest Feature Importance")
    plt.tight_layout()
    plt.savefig("feature_importance.png")
    print("[ML] Saved feature_importance.png")

# Plot SQ Efficiency Limit Overlay
def plot_sq_limit_overlay(predicted_bandgap=None, efficiency=None):
    bandgap_values = np.linspace(0.5, 3.0, 300)
    sq_eff = 0.337 * (bandgap_values / 1.34) * np.exp(-(bandgap_values - 1.34)**2 / 0.1)
    sq_eff *= 100

    plt.figure(figsize=(7, 5))
    plt.plot(bandgap_values, sq_eff, label="SQ Limit", linewidth=2)

    if predicted_bandgap is not None and efficiency is not None:
        plt.scatter([predicted_bandgap], [efficiency], color='red', label="Prediction", zorder=5)

    plt.xlabel("Bandgap (eV)")
    plt.ylabel("Efficiency (%)")
    plt.title("Shockley–Queisser Limit Overlay")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("sq_limit_overlay.png")
    print("[ML] Saved sq_limit_overlay.png")
