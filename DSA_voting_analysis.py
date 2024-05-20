import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu, shapiro, levene
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Update the file_path to be relative to the script directory
file_path = os.path.join(script_dir, 'NPC 1st Place Vote by Chapter and Slate - NPC Raw Data.csv')
new_csv_path = os.path.join(script_dir, 'Relative Chapter Size - Sheet1SORTED.csv')

# Load the CSV files
df = pd.read_csv(file_path)
new_df = pd.read_csv(new_csv_path)

# List of moderate and left slates
moderate_slates = ["Groundwork", "North Star", "Socialist Majority Caucus"]
left_slates = ["Alexander Morash", "Brandy Pride", "Julius Kapushinski", "Luisa M.", 
               "Anti-Zionist", "Bread & Roses", "Emerge", "Libertarian Socialist Caucus", 
               "Marxist Unity Group", "Red Labor", "Red Star", "Reform & Revolution"]

# List of second choice candidates that determine if Aaron Berger voters are "left" or "moderate"
left_second_choices = ["Ahmed Husain", "C.S. Jackson", "Catherine Elias", "John Lewis", "Jorge Rocha",
                       "Kristin Schall", "Megan Romer", "Rashad X", "Sam Heft-Luthy", "Tom Julstrom"]
moderate_second_choices = ["Cara Tobe", "Colleen Johnston", "Grace Mausser", "Renée Paradis", "Rose DuBois"]

# Create a column to categorize the slates as 'moderate', 'left', or 'N/A'
def categorize_slate(slate, second_choice):
    if slate == "Aaron Berger":
        if second_choice in left_second_choices:
            return 'left'
        elif second_choice in moderate_second_choices:
            return 'moderate'
        else:
            return 'N/A'
    elif slate in moderate_slates:
        return 'moderate'
    elif slate in left_slates:
        return 'left'
    else:
        return 'N/A'

# Use '2th' for the second choice votes
df['slate_category'] = df.apply(lambda row: categorize_slate(row['Slate'], row['2th']), axis=1)

# Exclude N/A votes from the analysis but keep them for chapter size calculation
votes_df = df[df['slate_category'] != 'N/A']

# Calculate chapter sizes based on the original dataframe
chapter_sizes = df.groupby('DSA Chapter')['Voter'].count()

# Add chapter sizes to the votes_df
votes_df = votes_df.merge(chapter_sizes.rename('Absolute Chapter Size'), left_on='DSA Chapter', right_index=True)

# Merge with the new dataframe
merged_df = votes_df.merge(new_df, left_on='DSA Chapter', right_on='Chapter', how='left')

# Convert the % population (high) columns to numeric
merged_df['DSA % Population'] = merged_df['% population (high)'].str.rstrip('%').astype('float') / 100

# Drop rows with missing values in the DSA % Population column
merged_df = merged_df.dropna(subset=['DSA % Population'])

# Calculate descriptive statistics for Absolute Chapter Size and DSA % Population based on slate category
descriptive_stats_sizes = merged_df.groupby('slate_category')['Absolute Chapter Size'].describe()
descriptive_stats_population_high = merged_df.groupby('slate_category')['DSA % Population'].describe()

# Extract Absolute Chapter Size and DSA % Population for each group
left_sizes = merged_df[merged_df['slate_category'] == 'left']['Absolute Chapter Size']
moderate_sizes = merged_df[merged_df['slate_category'] == 'moderate']['Absolute Chapter Size']
left_population_high = merged_df[merged_df['slate_category'] == 'left']['DSA % Population']
moderate_population_high = merged_df[merged_df['slate_category'] == 'moderate']['DSA % Population']

# Perform Mann-Whitney U test
u_stat_sizes, p_value_sizes_mannwhitney = mannwhitneyu(left_sizes, moderate_sizes, alternative='two-sided')
u_stat_population_high, p_value_population_high_mannwhitney = mannwhitneyu(left_population_high, moderate_population_high, alternative='two-sided')

print("\nMann-Whitney U Test Results (Absolute Chapter Size):")
print(f"U-statistic: {u_stat_sizes}, p-value: {p_value_sizes_mannwhitney}")

print("\nMann-Whitney U Test Results (DSA % Population):")
print(f"U-statistic: {u_stat_population_high}, p-value: {p_value_population_high_mannwhitney}")

# Visualization for Absolute Chapter Size
plt.figure(figsize=(10, 6))
sns.boxplot(x='slate_category', y='Absolute Chapter Size', data=merged_df)
plt.title('Absolute Chapter Size by Slate Category')
plt.xlabel('Slate Category')
plt.ylabel('Absolute Chapter Size')
plt.savefig('boxplot_absolute_chapter_size.png')
plt.show()

# Visualization for DSA % Population
plt.figure(figsize=(10, 6))
sns.boxplot(x='slate_category', y='DSA % Population', data=merged_df)
plt.title('DSA % Population by Slate Category')
plt.xlabel('Slate Category')
plt.ylabel('DSA % Population')
plt.savefig('boxplot_dsa_population.png')
plt.show()

# Logistic Regression Analysis

# Prepare the data: Encode the slate category as a binary variable (0 for moderate, 1 for left)
merged_df['slate_binary'] = merged_df['slate_category'].apply(lambda x: 1 if x == 'left' else 0)

# Separate logistic regression for Absolute Chapter Size
X_sizes = merged_df[['Absolute Chapter Size']]
poly_sizes = PolynomialFeatures(degree=2, include_bias=False)
X_sizes_poly = poly_sizes.fit_transform(X_sizes)
log_reg_sizes = LogisticRegression()
log_reg_sizes.fit(X_sizes_poly, merged_df['slate_binary'])

# Separate logistic regression for DSA % Population
X_population_high = merged_df[['DSA % Population']]
poly_population_high = PolynomialFeatures(degree=2, include_bias=False)
X_population_high_poly = poly_population_high.fit_transform(X_population_high)
log_reg_population_high = LogisticRegression()
log_reg_population_high.fit(X_population_high_poly, merged_df['slate_binary'])

# Generate a range of values for plotting
X_test_sizes = pd.DataFrame(np.linspace(X_sizes['Absolute Chapter Size'].min(), X_sizes['Absolute Chapter Size'].max(), 500), columns=['Absolute Chapter Size'])
X_test_population_high = pd.DataFrame(np.linspace(X_population_high['DSA % Population'].min(), X_population_high['DSA % Population'].max(), 500), columns=['DSA % Population'])

# Create polynomial features for the test data
X_test_sizes_poly = poly_sizes.transform(X_test_sizes)
X_test_population_high_poly = poly_population_high.transform(X_test_population_high)

# Ensure no feature names are included during prediction
X_test_sizes_poly = pd.DataFrame(X_test_sizes_poly)
X_test_population_high_poly = pd.DataFrame(X_test_population_high_poly)

# Predict probabilities
y_pred_sizes = log_reg_sizes.predict_proba(X_test_sizes_poly)[:, 1]
y_pred_population_high = log_reg_population_high.predict_proba(X_test_population_high_poly)[:, 1]

# Plot the logistic regression curve for Absolute Chapter Size
plt.figure(figsize=(10, 6))
plt.scatter(X_sizes, merged_df['slate_binary'], label='Data', alpha=0.3)
plt.plot(X_test_sizes, y_pred_sizes, color='red', label='Logistic Regression Curve')
plt.xlabel('Absolute Chapter Size')
plt.ylabel('Probability of Left Slate')
plt.title('Logistic Regression Curve for Absolute Chapter Size')
plt.legend()
plt.savefig('logistic_regression_curve_chapter_sizes.png')
plt.show()

# Plot the logistic regression curve for DSA % Population
plt.figure(figsize=(10, 6))
plt.scatter(X_population_high, merged_df['slate_binary'], label='Data', alpha=0.3)
plt.plot(X_test_population_high, y_pred_population_high, color='red', label='Logistic Regression Curve')
plt.xlabel('DSA % Population')
plt.ylabel('Probability of Left Slate')
plt.title('Logistic Regression Curve for DSA % Population')
plt.legend()
plt.savefig('logistic_regression_curve_population_high.png')
plt.show()

# Class imbalance check
left_count = sum(merged_df['slate_binary'])
moderate_count = len(merged_df['slate_binary']) - left_count
print(f"\nClass distribution:\nLeft: {left_count}\nModerate: {moderate_count}")