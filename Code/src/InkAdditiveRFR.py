# -*- coding: utf-8 -*-
"""
InkAdiditiveRFR.py

Originally created in Google Colab.
Converted to .py for deployment.
"""


# **1. Importing Libraries**python InkAdditiveRFR.py


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_absolute_error, r2_score
# from skopt import gp_minimize
# from skopt.space import Integer, Real
# from skopt.utils import use_named_args
import warnings
# import pickle
from sklearn.model_selection import GridSearchCV
# from skopt.space import Real, Categorical
# import scipy.stats as stats
# from sklearn.ensemble import GradientBoostingRegressor
from category_encoders import TargetEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import random
# import plotly.express as px
from bayes_opt import BayesianOptimization
from scipy.interpolate import make_interp_spline

# import plotly.io as pio
# pio.renderers.default = "browser"


"""# **13. Optimization Loop beyond the dataset using Genetic Algorithm**

    **The Optimization Loop using a Genetic Algorithm iteratively generates new ink compositions beyond the dataset by mimicking natural selection. It evaluates compositions based on desired properties (e.g., bandgap) and evolves them through selection, crossover, and mutation. This approach helps discover novel formulations with improved performance.**
    """

# # Define the fitness function outside of the genetic_algorithm function
# def fitness(individual, best_rf, ink_encoder, additive_encoder, composition_encoder, adjusted_sq_efficiency):
#         """ Calculate the fitness of an individual (adjusted SQ efficiency) """
#         try:
#             # Create a synthetic row for efficiency calculation
#             synthetic_row = pd.DataFrame([{
#                 'Intensity': individual['Intensity'],
#                 'Ink Concentration [M]': individual['Ink_Concentration'],
#                 'Composition_Value': individual['Composition_Value'],
#                 'Ink': individual['Ink'],
#                 'Additive': individual['Additive'],
#                 'Composition_Type_original': individual['Composition_Type'],
#                 'Bandgap': None,
#                 'Composition_Type_Zn': int('Zn' in individual['Composition_Type']),
#                 'Composition_Type_Br': int('Br' in individual['Composition_Type']),
#                 'Composition_Type_FA': int('FA' in individual['Composition_Type']),
#                 'Composition_Type_EA': int('EA' in individual['Composition_Type'])
#             }])

#             # Encode categorical features
#             synthetic_row['Ink_encoded'] = ink_encoder.transform(synthetic_row[['Ink']])
#             synthetic_row['Additive_encoded'] = additive_encoder.transform(synthetic_row[['Additive']])
#             synthetic_row['Composition_Type_encoded'] = composition_encoder.transform(synthetic_row[['Composition_Type_original']])

#             # Prepare features for prediction
#             X_synthetic = synthetic_row[['Intensity', 'Ink Concentration [M]', 'Composition_Value',
#                                         'Ink_encoded', 'Additive_encoded', 'Composition_Type_encoded']]

#             # Predict bandgap
#             synthetic_row['Bandgap'] = best_rf.predict(X_synthetic)[0]

#             # Calculate efficiency
#             efficiency = adjusted_sq_efficiency(synthetic_row.iloc[0])
#             return efficiency
#         except Exception as e:
#             return -1  # Return very low fitness if there was an error

# def genetic_algorithm(n_generations=100, population_size=50, mutation_rate=0.1, tournament_size=5, max_no_improvement=10, best_rf=None, ink_encoder=None, additive_encoder=None, composition_encoder=None, adjusted_sq_efficiency=None):
#         # Define parameter ranges
#         param_ranges = {
#             'Intensity': (1000, 2000000),
#             'Ink_Concentration': (1.0, 1.3),
#             'Composition_Value': (0, 30),
#             'Ink': ['FASnI3', 'mix', 'MASnI3'],
#             'Additive': ['Zn', 'Br', 'MA', 'EASCN', '4-MePEABr', '0'],
#             'Composition_Type': ['Baseline', '5% Zn', '10% Zn', '15% Zn',
#                                 '5%Br', '10% Br', '20% Br', '20% FA',
#                                 '10% MA', '20% MA', '10% EA', '4-MePEABr',
#                                 '5% EA', '15% EA', 'EA 5%', 'EA 15%']
#         }

#         def create_individual():
#             """ Generate a random individual solution """
#             return {
#                 'Intensity': random.uniform(*param_ranges['Intensity']),
#                 'Ink_Concentration': random.uniform(*param_ranges['Ink_Concentration']),
#                 'Composition_Value': random.uniform(*param_ranges['Composition_Value']),
#                 'Ink': random.choice(param_ranges['Ink']),
#                 'Additive': random.choice(param_ranges['Additive']),
#                 'Composition_Type': random.choice(param_ranges['Composition_Type'])
#             }

#         def crossover(parent1, parent2):
#             """ Perform one-point crossover to produce offspring """
#             crossover_point = random.randint(0, len(parent1)-1)
#             offspring = parent1.copy()

#             # Swap from crossover point onwards with the second parent
#             for key in list(parent2.keys())[crossover_point:]:
#                 offspring[key] = parent2[key]
#             return offspring

#         def mutate(individual):
#             """ Apply mutation by randomly changing one of the parameters """
#             mutation_type = random.choice(list(individual.keys()))

#             if mutation_type == 'Intensity':
#                 individual[mutation_type] = random.uniform(*param_ranges['Intensity'])
#             elif mutation_type == 'Ink_Concentration':
#                 individual[mutation_type] = random.uniform(*param_ranges['Ink_Concentration'])
#             elif mutation_type == 'Composition_Value':
#                 individual[mutation_type] = random.uniform(*param_ranges['Composition_Value'])
#             elif mutation_type == 'Ink':
#                 individual[mutation_type] = random.choice(param_ranges['Ink'])
#             elif mutation_type == 'Additive':
#                 individual[mutation_type] = random.choice(param_ranges['Additive'])
#             elif mutation_type == 'Composition_Type':
#                 individual[mutation_type] = random.choice(param_ranges['Composition_Type'])

#             return individual

#         def tournament_selection(population, best_rf, ink_encoder, additive_encoder, composition_encoder, adjusted_sq_efficiency):
#             """ Tournament selection to choose parents based on fitness """
#             tournament = random.sample(population, tournament_size)

#             # Pass necessary arguments to fitness function
#             tournament.sort(key=lambda x: fitness(x, best_rf, ink_encoder, additive_encoder, composition_encoder, adjusted_sq_efficiency), reverse=True)
#             return tournament[0], tournament[1]  # Return two best individuals

#         # Initialize population
#         population = [create_individual() for _ in range(population_size)]

#         best_individual = None
#         best_fitness = -1
#         no_improvement_count = 0

#         # Evolve the population over generations
#         with ProcessPoolExecutor() as executor:
#             for generation in range(n_generations):
#                 new_population = []

#                 for _ in range(population_size):
#                     parent1, parent2 = tournament_selection(population, best_rf, ink_encoder, additive_encoder, composition_encoder, adjusted_sq_efficiency)
#                     offspring = crossover(parent1, parent2)

#                     if random.random() < mutation_rate:
#                         offspring = mutate(offspring)

#                     new_population.append(offspring)

#                 # Evaluate the new population using parallelization
#                 fitness_values = list(executor.map(fitness, new_population, [best_rf]*population_size,
#                                                     [ink_encoder]*population_size, [additive_encoder]*population_size,
#                                                     [composition_encoder]*population_size, [adjusted_sq_efficiency]*population_size))

#                 # Track the best individual
#                 for idx, individual in enumerate(new_population):
#                     individual_fitness = fitness_values[idx]
#                     if individual_fitness > best_fitness:
#                         best_fitness = individual_fitness
#                         best_individual = individual
#                         no_improvement_count = 0
#                     else:
#                         no_improvement_count += 1

#                 print(f"Generation {generation+1}/{n_generations}: Best Fitness = {best_fitness:.4f}")

#                 # Early stopping if no improvement
#                 if no_improvement_count >= max_no_improvement:
#                     print("Early stopping due to no improvement in fitness.")
#                     break

#                 population = new_population

#         # Return best individual found
#         return best_individual, best_fitness
# Function to calculate efficiency with composition-specific scaling
def adjusted_sq_efficiency(row):
        """
        Adjusts Shockley-Queisser efficiency based on material composition.

        - Zn enhances charge transport, slight boost.
        - Br improves stability but lowers absorption.
        - FA increases efficiency.
        - EA affects crystallization.
        """
        base_efficiency = 0.337 * (row['Bandgap'] / 1.34) * np.exp(-(row['Bandgap'] - 1.34)**2 / 0.1)

        # Adjust efficiency based on composition
        if 'Composition_Type_Zn' in row and row['Composition_Type_Zn']:
            base_efficiency *= 1.05  # Zn slightly increases efficiency (+5%)

        if 'Composition_Type_Br' in row and row['Composition_Type_Br']:
            base_efficiency *= 0.95  # Br slightly decreases efficiency (-5%)

        if 'Composition_Type_FA' in row and row['Composition_Type_FA']:
            base_efficiency *= 1.07  # FA improves efficiency (+7%)

        if 'Composition_Type_EA' in row and row['Composition_Type_EA']:
            base_efficiency *= 0.92  # EA decreases stability and crystallinity (-8%)

        # Convert to percentage and clip between 0-100%
        η_total = 0.90 * 0.95 * 0.97
        return np.clip(base_efficiency * η_total * 100, 0, 100)
        
# **2. Uploading and Loading Data**"""
def main():
    # Upload the file
    data = pd.read_excel("/home/ecd515/Desktop/PASS/src/PL_VALUES.xlsx")  

    """# **3. Function to display all the features in the target dataset**"""

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(data)

    """# **4. Data Preprocessing & Splitting (Feature Encoding, Input-Output Setup)**

    """

    # np.random.seed(42)
    # data_size = 500

    # # Creating a sample dataset
    # df = pd.DataFrame({
    #     "Intensity": np.random.uniform(0.1, 1.0, data_size),
    #     "Ink Concentration [M]": np.random.uniform(0.01, 1.0, data_size),
    #     "Composition_Value": np.random.uniform(0.1, 1.0, data_size),
    #     "Ink_encoded": np.random.choice([0, 1], data_size),
    #     "Additive_encoded": np.random.choice([0, 1], data_size),
    #     "Composition_Type_encoded": np.random.choice([0, 1], data_size),
    #     "Efficiency": np.random.uniform(10, 30, data_size)  # Target variable
    # })

    # # Define features and target
    # X = df.drop(columns=["Efficiency"])  # Feature set
    # y = df["Efficiency"]  # Target variable

    # # Split dataset into training (80%) and testing (20%) sets
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # # Initialize the Gradient Boosting Regressor
    # gb_model = GradientBoostingRegressor(random_state=42)

    # # Train the model
    # gb_model.fit(X_train, y_train)

    # # Make predictions
    # y_pred = gb_model.predict(X_test)

    # Step 1: Calculate Bandgap (same as before)
    data['Bandgap'] = 1240 / data['Wavelength'].replace(0, np.nan)
    data['Bandgap'] = data['Bandgap'].replace([np.inf, -np.inf], np.nan)
    data.dropna(subset=['Bandgap'], inplace=True)

    # Step 2: Extract numerical composition values
    data['Composition_Value'] = data['Ink Composition %'].str.extract(r'(\d+)')[0].astype(float)
    data['Composition_Value'] = data['Composition_Value'].fillna(0)

    # Step 3: Retain original columns for interpretation
    data['Ink_original'] = data['Ink']
    data['Additive_original'] = data['Additive']
    data['Composition_Type_original'] = data['Ink Composition %']

    # Step 4: Apply Target Encoding to categorical variables
    ink_encoder = TargetEncoder(cols=['Ink'])
    additive_encoder = TargetEncoder(cols=['Additive'])
    composition_encoder = TargetEncoder(cols=['Composition_Type_original'])

    # Fit and transform the encoders
    data['Ink_encoded'] = ink_encoder.fit_transform(data['Ink'], data['Bandgap'])
    data['Additive_encoded'] = additive_encoder.fit_transform(data['Additive'], data['Bandgap'])
    data['Composition_Type_encoded'] = composition_encoder.fit_transform(
        data['Composition_Type_original'], data['Bandgap']
    )

    # Step 5: Define input features and target
    X = data[['Intensity', 'Ink Concentration [M]', 'Composition_Value',
            'Ink_encoded', 'Additive_encoded', 'Composition_Type_encoded']]
    y = data['Bandgap']

    # Step 6: Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Display the shapes of the training and testing sets
    print("Training data shape:", X_train.shape, y_train.shape)
    print("Testing data shape:", X_test.shape, y_test.shape)

    """# **5. Organizing & Displaying Processed Data**"""

    # Create mappings for interpretation
    ink_mapping = data[['Ink_original', 'Ink_encoded']].drop_duplicates()
    additive_mapping = data[['Additive_original', 'Additive_encoded']].drop_duplicates()
    composition_mapping = data[['Composition_Type_original', 'Composition_Type_encoded']].drop_duplicates()

    # Display mappings
    print(ink_mapping.head())
    print(additive_mapping.head())
    print(composition_mapping.head())
    # print("\nInk Mapping:")
    # print(ink_mapping.to_markdown(index=False, tablefmt="grid"))

    # print("\nAdditive Mapping:")
    # print(additive_mapping.to_markdown(index=False, tablefmt="grid"))

    # print("\nComposition Type Mapping:")
    # print(composition_mapping.to_markdown(index=False, tablefmt="grid"))

    # Display full training data
    # train_data = X_train.copy()
    # train_data['Bandgap'] = y_train
    # train_data['Sample_No'] = data.loc[X_train.index, 'Sample_No']
    # train_data = train_data.merge(data[['Sample_No', 'Ink_original', 'Additive_original',
    #                                 'Composition_Type_original']], on='Sample_No')

    # print("\nFull Training Data:")
    # print(train_data[['Sample_No', 'Intensity', 'Ink Concentration [M]', 'Composition_Value',
    #                 'Ink_original', 'Additive_original', 'Composition_Type_original', 'Bandgap']].to_markdown(index=False, tablefmt="grid"))

    # # Display full testing data
    # test_data = X_test.copy()
    # test_data['Bandgap'] = y_test
    # test_data['Sample_No'] = data.loc[X_test.index, 'Sample_No']
    # test_data = test_data.merge(data[['Sample_No', 'Ink_original', 'Additive_original',
    #                                 'Composition_Type_original']], on='Sample_No')

    # print("\nFull Testing Data:")
    # print(test_data[['Sample_No', 'Intensity', 'Ink Concentration [M]', 'Composition_Value',
    #                 'Ink_original', 'Additive_original', 'Composition_Type_original', 'Bandgap']].to_markdown(index=False, tablefmt="grid"))

    """# **6. Model Training and Making Predictions**"""

    # Initialize Random Forest Regressor
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Train the model
    rf_model.fit(X_train, y_train)

    # Make predictions
    y_pred_rf = rf_model.predict(X_test)

    """# **7. Model Evaluations**

    ### **7.1 Initial model evaluation before tuning**
    """

    # Evaluate performance
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    mse_rf = mean_squared_error(y_test, y_pred_rf)
    rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
    r2_rf = r2_score(y_test, y_pred_rf)

    # Print results
    print("\nRandom Forest Regression Evaluation:")
    print(f"Mean Absolute Error (MAE): {mae_rf:.6f}")
    print(f"Mean Squared Error (MSE): {mse_rf:.6f}")
    print(f"Root Mean Squared Error (RMSE): {rmse_rf:.6f}")
    print(f"R-squared (R²): {r2_rf:.6f}")

    """### **7.2 Hyperparameter Tuning using Grid SearchCV**



    """

    # # Define the hyperparameter grid
    # param_grid = {
    #     'n_estimators': [50, 100, 200],  # Number of trees in the forest
    #     'max_depth': [None, 10, 20, 30],  # Maximum depth of trees
    #     'min_samples_split': [2, 5, 10],  # Minimum samples required to split a node
    #     'min_samples_leaf': [1, 2, 4]  # Minimum samples required at a leaf node
    # }

    # # Initialize RandomForestRegressor
    # rf = RandomForestRegressor(random_state=42)

    # # Set up GridSearchCV
    # grid_search = GridSearchCV(estimator=rf, param_grid=param_grid,
    #                         cv=5, n_jobs=-1, verbose=2, scoring='r2')

    # # Train using GridSearchCV
    # grid_search.fit(X_train, y_train)

    # # Best parameters from GridSearch
    # best_params = grid_search.best_params_
    # print(f"Best Hyperparameters: {best_params}")

    # # Train Random Forest with best parameters
    # best_rf = RandomForestRegressor(**best_params, random_state=42)
    # best_rf.fit(X_train, y_train)

    # # Predictions
    # y_pred = best_rf.predict(X_test)

    # # Evaluate the optimized model
    # mae = mean_absolute_error(y_test, y_pred)
    # mse = mean_squared_error(y_test, y_pred)
    # rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    # r2 = r2_score(y_test, y_pred)

    # # Print evaluation metrics
    # print(f"Optimized Random Forest Performance:")
    # print(f"Mean Absolute Error (MAE): {mae:.6f}")
    # print(f"Mean Squared Error (MSE): {mse:.6f}")
    # print(f"Root Mean Squared Error (RMSE): {rmse:.6f}")
    # print(f"R-squared (R²): {r2:.6f}")

    # """### **7.3. Hyperparameter Optimization Useing Bayesian Optimization**

    # **Hyperparameter Optimization for Random Forest Uses Bayesian Optimization to find the best hyperparameters for a Random Forest model by minimizing the negative R² score. Optimized parameters are used to train the final Random Forest model.**
    # """

    # # Define function for Bayesian Optimization
    # def rf_evaluate(n_estimators, max_depth, min_samples_split, min_samples_leaf, max_features):
    #     max_features = min(max_features, 1.0)  # Ensure max_features is within range
    #     model = RandomForestRegressor(
    #         n_estimators=int(n_estimators),
    #         max_depth=int(max_depth),
    #         min_samples_split=int(min_samples_split),
    #         min_samples_leaf=int(min_samples_leaf),
    #         max_features=max_features,  # Ensuring valid range
    #         random_state=42,
    #         n_jobs=-1
    #     )
    #     model.fit(X_train, y_train)
    #     y_pred = model.predict(X_test)
    #     return -mean_squared_error(y_test, y_pred)

    # # Define search space
    # param_bounds = {
    #     "n_estimators": (50, 400),
    #     "max_depth": (5, 25),
    #     "min_samples_split": (2, 10),
    #     "min_samples_leaf": (1, 5),
    #     "max_features": (0.3, 1.0)
    # }

    # # Perform Bayesian Optimization
    # optimizer = BayesianOptimization(f=rf_evaluate, pbounds=param_bounds, random_state=42)
    # optimizer.maximize(init_points=10, n_iter=50)

    # # Get best parameters
    # best_params = optimizer.max['params']
    # best_params['n_estimators'] = int(best_params['n_estimators'])
    # best_params['max_depth'] = int(best_params['max_depth'])
    # best_params['min_samples_split'] = int(best_params['min_samples_split'])
    # best_params['min_samples_leaf'] = int(best_params['min_samples_leaf'])

    # print("\nBest Hyperparameters:", best_params)

    # # Train final model with optimized parameters
    # best_rf = RandomForestRegressor(**best_params, random_state=42, n_jobs=-1)
    # best_rf.fit(X_train, y_train)
    # y_pred_best = best_rf.predict(X_test)

    # # Evaluate the optimized model
    # mae = mean_absolute_error(y_test, y_pred_best)
    # mse = mean_squared_error(y_test, y_pred_best)
    # rmse = np.sqrt(mse)
    # r2 = r2_score(y_test, y_pred_best)

    # print("\nOptimized Random Forest Performance:")
    # print(f"Mean Absolute Error (MAE): {mae:.6f}")
    # print(f"Mean Squared Error (MSE): {mse:.6f}")
    # print(f"Root Mean Squared Error (RMSE): {rmse:.6f}")
    # print(f"R-squared (R²): {r2:.6f}")

    """# **8. Visualization Functions**

    ### **8.1. Visualization comparing R² Score and MAE across all three models:**
    """

    # For Initial Model (after fitting rf_model)
    mae_initial = mean_absolute_error(y_test, y_pred_rf)
    r2_initial = r2_score(y_test, y_pred_rf)

    # # For Tuned Model (after fitting best_rf)
    # mae_tuned = mean_absolute_error(y_test, y_pred)
    # r2_tuned = r2_score(y_test, y_pred)

    # # For Optimized Model (after fitting best_rf from Bayesian Optimization)
    # mae_optimized = mean_absolute_error(y_test, y_pred_best)
    # r2_optimized = r2_score(y_test, y_pred_best)

    # # Define models and their respective performance metrics
    # models = ['Initial Model', 'Tuned Model', 'Optimized Model']
    # mae_values = [mae_initial, mae_tuned, mae_optimized]  # MAE values for the 3 models
    # r2_values = [r2_initial, r2_tuned, r2_optimized]  # R² values for the 3 models

    # # Plot MAE comparison
    # plt.figure(figsize=(8, 4))
    # plt.bar(models, mae_values, color=['red', 'blue', 'green'])
    # plt.ylabel('Mean Absolute Error (MAE)')
    # plt.title('MAE Comparison: Initial vs. Tuned vs. Optimized Model')
    # plt.savefig("mae_comparison.png")
    # plt.close()

    # # Plot R² Score comparison
    # plt.figure(figsize=(8, 4))
    # plt.bar(models, r2_values, color=['red', 'blue', 'green'])
    # plt.ylabel('R² Score')
    # plt.title('R² Score Comparison: Initial vs. Tuned vs. Optimized Model')
    # plt.savefig("R²_comparison.png")
    # plt.close()

    """### **8.2.  Model coefficients and Plot for feature importances**

    **To display the importance of each feature in predicting the Bandgap.**

    **Helps prioritize variables for feature engineering or model refinement.**
    """

    # Feature Importance (Random Forest)
    feature_importances = rf_model.feature_importances_

    # Print the feature importances
    print("\nFeature Importances:")
    for feature, importance in zip(X_train.columns, feature_importances):
        print(f"{feature}: {importance:.4f}")

    # Plot Feature Importance
    plt.figure(figsize=(8, 5))
    plt.barh(X_train.columns, feature_importances, align="center")
    plt.xlabel("Feature Importance")
    plt.title("Random Forest Feature Importances")
    plt.savefig("Feature Importance.png")
    plt.close()
    
    


    """**A strong, positive relationship between PL intensity and bandgap means stable and efficient bandgap.**

    ### **8.3 Scatter Plot of Actual vs Predicted Values**
    """

    # all data points
    y_pred_all = rf_model.predict(X)

    plt.figure(figsize=(10, 6))
    plt.scatter(y, y_pred_all, alpha=0.6, edgecolor=None, c='blue', label='All Data')
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2, label='Prediction Line')
    plt.xlabel('Actual Bandgap')
    plt.ylabel('Predicted Bandgap')
    plt.title('Actual vs Predicted Bandgap (Random Forest)')
    plt.savefig("Actual vs Predicted Bandgap.png")
    plt.close()
    plt.legend()
    plt.grid()
    

    """**The closer the points are to the line, the better the model’s performance. Wider spread indicates poor predictive accuracy.**

    **The outlier is a valid data point. The prediction error for this point is small (0.0638 eV) and within an acceptable range, and removing it would bias the dataset and reduce the model's ability to generalize. Additionally, the model's overall performance metrics (MAE = 0.0049, R² = 0.4473) remain satisfactory, and the outlier can serve as a case study to guide future improvements, such as feature engineering or targeted data collection.**



    ### **8.4 Density Distribution Plot of Residuals**
    """

    # Calculate residuals
    y_pred_all = rf_model.predict(X)
    residuals_all = y - y_pred_all

    # Plot
    plt.figure(figsize=(10, 6))
    sns.kdeplot(residuals_all, fill=True, color='blue', alpha=0.6, label='Residual Density')
    plt.axvline(0, color='red', linestyle='--', label='Zero Error Line')
    plt.title('Density Distribution of Residuals')
    plt.xlabel('Residuals')
    plt.ylabel('Density')
    plt.legend()
    plt.grid()
    plt.savefig("Density Distribution of Residuals.png")
    plt.close()

    """**The density plot is symmetrical and centered at 0 and spread is minimal, the model is performing well across the dataset**

    # **9. Efficiency Calculation and Visualization using Shockley-Queisser limit**
    """
    # --- 9. Efficiency Calculation and Visualization using Shockley–Queisser Limit ---

    # Step 1: Apply efficiency calculation to dataset
    data['Adjusted_SQ_Efficiency'] = data.apply(adjusted_sq_efficiency, axis=1)

    bandgap_values = np.linspace(0.9, 2.1, 500)
    sq_efficiency_curve = 0.337 * (bandgap_values / 1.34) * np.exp(-(bandgap_values - 1.34)**2 / 0.15)
    sq_efficiency_percent = sq_efficiency_curve * 100

    # 2. Clean real dataset points
    filtered = data.dropna(subset=['Bandgap', 'Adjusted_SQ_Efficiency'])
    raw_x = filtered['Bandgap'].values
    raw_y = filtered['Adjusted_SQ_Efficiency'].values

    # 3. Smooth interpolated curve
    grouped = filtered.groupby('Bandgap', as_index=False)['Adjusted_SQ_Efficiency'].mean()
    grouped = grouped.sort_values('Bandgap')

    x = grouped['Bandgap'].values
    y = grouped['Adjusted_SQ_Efficiency'].values

    if len(x) >= 4:
        x_smooth = np.linspace(x.min(), x.max(), 300)
        spline = make_interp_spline(x, y, k=3)
        y_smooth = spline(x_smooth)
    else:
        x_smooth, y_smooth = x, y

    # Final Plot
    # 4. Final Plot
    plt.figure(figsize=(12, 8))

    # Ideal curve
    plt.plot(bandgap_values, sq_efficiency_percent, color='black', linewidth=2, label="Shockley–Queisser Limit (Ideal)")

    # Interpolated model curve
    plt.plot(x_smooth, y_smooth, color='blue', linewidth=2.5, label="ML Predicted Efficiency Curve")

    # Real data points
    plt.scatter(raw_x, raw_y, color='green', edgecolor='black', s=45, alpha=0.8, label="Measured Sample Efficiencies")

    # Red vertical line at 1.34 eV
    plt.axvline(x=1.34, color='red', linestyle='--', linewidth=1.5, label="Optimal Bandgap (1.34 eV)")

    # Labels & aesthetics
    plt.xlabel("Bandgap (eV)", fontsize=13)
    plt.ylabel("Efficiency (%)", fontsize=13)
    plt.title("Dataset Efficiency vs Theoretical Limit", fontsize=15)
    plt.xlim(0.9, 2.1)
    plt.ylim(0, 40)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(fontsize=11)
    plt.tight_layout()

    # Save and show
    plt.savefig("sq_limit_with_all_samples.png")
    plt.close()

    # # Predefined Shockley-Queisser (SQ) limit curve (bandgap vs efficiency)
    # bandgap_values = np.linspace(0.5, 3.0, 100)  # Bandgap range (eV)
    # sq_efficiency_curve = 0.337 * (bandgap_values / 1.34) * np.exp(-(bandgap_values - 1.34)**2 / 0.1)  # Standard SQ limit

    # # Plot SQ limit curve for reference
    # plt.figure(figsize=(8, 6))
    # plt.plot(bandgap_values, sq_efficiency_curve * 100, label="Shockley-Queisser Limit")
    # plt.axvline(x=1.34, color='red', linestyle='--', label="Optimal Bandgap (1.34 eV)")
    # plt.xlabel("Bandgap (eV)")
    # plt.ylabel("Efficiency (%)")
    # plt.title("Shockley-Queisser Limit for Different Compositions")
    # plt.grid(True)
    # plt.legend()
    # plt.savefig("sq_limit_curve.png")
    # plt.close()


    # # Apply efficiency calculation to dataset
    # data['Adjusted_SQ_Efficiency'] = data.apply(adjusted_sq_efficiency, axis=1)

    #  Print efficiency results
    print(data[['Bandgap', 'Adjusted_SQ_Efficiency']])

    # Efficiency Distribution Plot
    plt.figure(figsize=(8, 6))
    sns.histplot(data['Adjusted_SQ_Efficiency'], bins=30, kde=True, color="green", label="Adjusted Efficiency")
    plt.xlabel("Efficiency (%)")
    plt.ylabel("Count")
    plt.title("Adjusted Efficiency Distribution Based on Composition")
    plt.grid(True)
    plt.legend()
    plt.savefig("adjusted_efficiency_distribution.png")
    plt.close()

    # Save updated dataset
    data.to_csv("dataset_with_adjusted_efficiency.csv", index=False)

    # """**If the peak is around 30, most samples have 30% efficiency.**"""

    # fig = px.scatter_3d(
    #     data,
    #     x='Composition_Type_original',
    #     y='Ink Concentration [M]',
    #     z='Bandgap',
    #     color='Adjusted_SQ_Efficiency'
    # )
    # fig.write_html("3d_efficiency_plot.html")
    # #fig.write_image("3d_efficiency_plot.png")
    
    

    """# **10. Finding the Most Efficient Samples in the Dataset**"""

    # Find the most efficient sample based on Adjusted SQ Efficiency
    most_efficient_sample = data.loc[data['Adjusted_SQ_Efficiency'].idxmax()]
    most_efficient_sample_df = most_efficient_sample.to_frame().T

    # Print the most efficient sample
    print("\nMost Efficient Sample in the Dataset (Adjusted SQ Efficiency):")
    print(most_efficient_sample_df.to_string(index=False))

    # Find the top 5 most efficient samples
    top_samples = data.nlargest(5, 'Adjusted_SQ_Efficiency')

    # Print the top 5 most efficient samples
    print("\nTop 5 Most Efficient Samples in the Dataset (Adjusted SQ Efficiency):")
    print(top_samples.to_string(index=False))

    """# **11. Optimization Loop beyond the dataset using Random Search**

    **Model performs a random search by generating new, unseen combinations of Intensity, Ink, and Additive beyond the original dataset. It uses the trained Random Forest model to predict Bandgap for these combinations and identifies the optimal parameters that maximize Bandgap. This allows for the exploration of a wider parameter space to find better configurations.**
    """

    def random_search_optimization(n_iterations=1000, model=None):
        """
        Performs random search optimization to find parameter combinations
        that maximize the adjusted SQ efficiency.
        """
        # Define parameter ranges based on dataset analysis
        param_ranges = {
            'Intensity': (1000, 2000000),
            'Ink_Concentration': (1.0, 1.3),
            'Composition_Value': (0, 30),
            'Ink': ['FASnI3', 'mix', 'MASnI3'],
            'Additive': ['Zn', 'Br', 'MA', 'EASCN', '4-MePEABr', '0'],
            'Composition_Type': ['Baseline', '5% Zn', '10% Zn', '15% Zn',
                            '5%Br', '10% Br', '20% Br', '20% FA',
                            '10% MA', '20% MA', '10% EA', '4-MePEABr',
                            '5% EA', '15% EA', 'EA 5%', 'EA 15%']
        }

        best_params = None
        best_efficiency = -1  # Initialize with minimum possible value
        results = []
        successful_runs = 0

        for _ in tqdm(range(n_iterations), desc="Random Search Progress"):
            # Generate random parameters within ranges
            params = {
                'Intensity': random.uniform(*param_ranges['Intensity']),
                'Ink_Concentration': random.uniform(*param_ranges['Ink_Concentration']),
                'Composition_Value': random.uniform(*param_ranges['Composition_Value']),
                'Ink': random.choice(param_ranges['Ink']),
                'Additive': random.choice(param_ranges['Additive']),
                'Composition_Type': random.choice(param_ranges['Composition_Type'])
            }

            try:
                # Create a synthetic row for efficiency calculation
                synthetic_row = pd.DataFrame([{
                    'Intensity': params['Intensity'],
                    'Ink Concentration [M]': params['Ink_Concentration'],
                    'Composition_Value': params['Composition_Value'],
                    'Ink': params['Ink'],
                    'Additive': params['Additive'],
                    'Composition_Type_original': params['Composition_Type'],
                    'Bandgap': None,
                    'Composition_Type_Zn': int('Zn' in params['Composition_Type']),
                    'Composition_Type_Br': int('Br' in params['Composition_Type']),
                    'Composition_Type_FA': int('FA' in params['Composition_Type']),
                    'Composition_Type_EA': int('EA' in params['Composition_Type'])
                }])

                # Encode categorical features
                synthetic_row['Ink_encoded'] = ink_encoder.transform(synthetic_row[['Ink']])
                synthetic_row['Additive_encoded'] = additive_encoder.transform(synthetic_row[['Additive']])
                synthetic_row['Composition_Type_encoded'] = composition_encoder.transform(synthetic_row[['Composition_Type_original']])

                # Prepare features for prediction
                X_synthetic = synthetic_row[['Intensity', 'Ink Concentration [M]', 'Composition_Value',
                                        'Ink_encoded', 'Additive_encoded', 'Composition_Type_encoded']]

                # Predict bandgap
                synthetic_row['Bandgap'] = model.predict(X_synthetic)[0]

                # Calculate efficiency
                efficiency = adjusted_sq_efficiency(synthetic_row.iloc[0])
                params['Efficiency'] = efficiency
                results.append(params)
                successful_runs += 1

                # Update best parameters
                if efficiency > best_efficiency:
                    best_efficiency = efficiency
                    best_params = params.copy()

            except Exception as e:
                # print(f"Skipping parameters due to error: {params}\nError: {str(e)}")
                continue

        if best_params is None:
            raise ValueError("No valid parameter combinations were found. Check your adjusted_sq_efficiency function and encoders.")

        print(f"\nSuccessfully evaluated {successful_runs}/{n_iterations} parameter combinations")
        return best_params, pd.DataFrame(results)

    # Run random search optimization
    best_random_params, random_results = random_search_optimization(n_iterations=500, model=rf_model)

    # Display best parameters found
    if best_random_params is not None:
        print("\nOptimal Parameters Found (Random Search - Adjusted SQ Efficiency):")
        print(f"Intensity: {best_random_params['Intensity']:.2f}")
        print(f"Ink: {best_random_params['Ink']}")
        print(f"Additive: {best_random_params['Additive']}")
        print(f"Ink Concentration [M]: {best_random_params['Ink_Concentration']:.4f}")
        print(f"Composition Type: {best_random_params['Composition_Type']}")
        print(f"Predicted Efficiency: {best_random_params['Efficiency']:.4f}%")
    else:
        print("No valid parameter combinations found.")

    """# **12. Optimization Loop beyond the dataset using Bayesian Optimization**

    **Model uses Bayesian Optimization to efficiently explore new, unseen combinations of Intensity, Ink, and Additive beyond the dataset. It iteratively suggests parameter combinations, predicts Bandgap using the trained model, and identifies the optimal values that maximize Bandgap. This method is more systematic and efficient than random search, focusing on promising regions of the parameter space.**
    """

    def encode_category(value, categories):
        return categories.index(value)

    def decode_category(index, categories):
        return categories[int(index)]

    def bayesian_optimization(n_iterations=100):
        """
        Performs Bayesian optimization to find parameter combinations
        that maximize the adjusted SQ efficiency.
        """
        param_ranges = {
            'Intensity': (1000, 2000000),
            'Ink_Concentration': (1.0, 1.3),
            'Composition_Value': (0, 30),
            'Ink': ['FASnI3', 'mix', 'MASnI3'],
            'Additive': ['Zn', 'Br', 'MA', 'EASCN', '4-MePEABr', '0'],
            'Composition_Type': ['Baseline', '5% Zn', '10% Zn', '15% Zn',
                            '5%Br', '10% Br', '20% Br', '20% FA',
                            '10% MA', '20% MA', '10% EA', '4-MePEABr',
                            '5% EA', '15% EA', 'EA 5%', 'EA 15%']
        }

        ink_categories = param_ranges['Ink']
        additive_categories = param_ranges['Additive']
        composition_type_categories = param_ranges['Composition_Type']

        def objective_function(Intensity, Ink_Concentration, Composition_Value, Ink, Additive, Composition_Type):
            """ Function to be optimized """
            Ink = decode_category(round(Ink), ink_categories)
            Additive = decode_category(round(Additive), additive_categories)
            Composition_Type = decode_category(round(Composition_Type), composition_type_categories)

            try:
                synthetic_row = pd.DataFrame([{
                    'Intensity': Intensity,
                    'Ink Concentration [M]': Ink_Concentration,
                    'Composition_Value': Composition_Value,
                    'Ink': Ink,
                    'Additive': Additive,
                    'Composition_Type_original': Composition_Type,
                    'Bandgap': None,
                    'Composition_Type_Zn': int('Zn' in Composition_Type),
                    'Composition_Type_Br': int('Br' in Composition_Type),
                    'Composition_Type_FA': int('FA' in Composition_Type),
                    'Composition_Type_EA': int('EA' in Composition_Type)
                }])

                synthetic_row['Ink_encoded'] = ink_encoder.transform(synthetic_row[['Ink']])
                synthetic_row['Additive_encoded'] = additive_encoder.transform(synthetic_row[['Additive']])
                synthetic_row['Composition_Type_encoded'] = composition_encoder.transform(synthetic_row[['Composition_Type_original']])

                X_synthetic = synthetic_row[['Intensity', 'Ink Concentration [M]', 'Composition_Value',
                                            'Ink_encoded', 'Additive_encoded', 'Composition_Type_encoded']]

                synthetic_row['Bandgap'] = rf_model.predict(X_synthetic)[0]
                efficiency = adjusted_sq_efficiency(synthetic_row.iloc[0])
                return efficiency
            except:
                return -1  # Return a very low efficiency in case of errors

        pbounds = {
            'Intensity': param_ranges['Intensity'],
            'Ink_Concentration': param_ranges['Ink_Concentration'],
            'Composition_Value': param_ranges['Composition_Value'],
            'Ink': (0, len(ink_categories) - 1),
            'Additive': (0, len(additive_categories) - 1),
            'Composition_Type': (0, len(composition_type_categories) - 1)
        }

        optimizer = BayesianOptimization(f=objective_function, pbounds=pbounds, random_state=42)
        optimizer.maximize(init_points=10, n_iter=n_iterations)

        best_params = optimizer.max['params']
        best_params['Ink'] = decode_category(round(best_params['Ink']), ink_categories)
        best_params['Additive'] = decode_category(round(best_params['Additive']), additive_categories)
        best_params['Composition_Type'] = decode_category(round(best_params['Composition_Type']), composition_type_categories)

        return best_params

    # Run Bayesian optimization
    best_bayesian_params = bayesian_optimization(n_iterations=100)

    # Display best parameters found
    print("\nOptimal Parameters Found (Bayesian Optimization - Adjusted SQ Efficiency):")
    print(f"Intensity: {best_bayesian_params['Intensity']:.2f}")
    print(f"Ink: {best_bayesian_params['Ink']}")
    print(f"Additive: {best_bayesian_params['Additive']}")
    print(f"Ink Concentration [M]: {best_bayesian_params['Ink_Concentration']:.4f}")
    print(f"Composition Type: {best_bayesian_params['Composition_Type']}")

    # Assuming the optimal parameters found from Bayesian optimization
    optimal_params = {
        'Intensity': 1558467.96,
        'Ink': 'mix',
        'Additive': 'EASCN',
        'Ink Concentration [M]': 1.0121,
        'Composition Type': '20% FA',  # Just an example, adjust based on your composition data
        'Bandgap':   1.50242   # Example bandgap, this will come from your dataset or model
    }

    # Define a new function to compute the adjusted efficiency based on the optimized parameters
    def compute_bayesian_efficiency(optimal_params):
        # Create a DataFrame for the row of optimal parameters
        optimal_row = {
            'Bandgap': optimal_params['Bandgap'],
            'Composition_Type_Zn': 1 if optimal_params['Ink'] == 'Zn' else 0,
            'Composition_Type_Br': 1 if optimal_params['Ink'] == 'Br' else 0,
            'Composition_Type_FA': 1 if optimal_params['Composition Type'] == '20% FA' else 0,
            'Composition_Type_EA': 1 if optimal_params['Additive'] == 'EASCN' else 0,
            'Ink': optimal_params['Ink'],
            'Additive': optimal_params['Additive'],
            'Ink Concentration [M]': optimal_params['Ink Concentration [M]']
        }

        # Calculate the adjusted SQ efficiency using the function defined earlier
        adjusted_efficiency = adjusted_sq_efficiency(optimal_row)

        return adjusted_efficiency

    # Calculate the adjusted efficiency for the optimal parameters
    optimal_efficiency = compute_bayesian_efficiency(optimal_params)

    # Print the result
    print(f"Optimal Efficiency: {optimal_efficiency:.2f}%")

#     # Run the Genetic Algorithm with optimizations
#     best_genetic_params, best_genetic_efficiency = genetic_algorithm(
#         n_generations=50,
#         population_size=50,
#         mutation_rate=0.1,
#         tournament_size=5,
#         max_no_improvement=10,
#         best_rf=best_rf,
#         ink_encoder=ink_encoder,
#         additive_encoder=additive_encoder,
#         composition_encoder=composition_encoder,
#         adjusted_sq_efficiency=adjusted_sq_efficiency
# )

#     # Display the results
#     print("\nOptimal Parameters Found (Genetic Algorithm - Adjusted SQ Efficiency):")
#     print(f"Intensity: {best_genetic_params['Intensity']:.2f}")
#     print(f"Ink: {best_genetic_params['Ink']}")
#     print(f"Additive: {best_genetic_params['Additive']}")
#     print(f"Ink Concentration [M]: {best_genetic_params['Ink_Concentration']:.4f}")
#     print(f"Composition Type: {best_genetic_params['Composition_Type']}")
#     print(f"Predicted Efficiency: {best_genetic_efficiency:.4f}%")
    
#      # Save the trained model using pickle
#     with open('random_forest_model.pkl', 'wb') as file:
#         pickle.dump(best_rf, file)
        
if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    main()
