import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from sklearn.linear_model import LogisticRegression
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

# Absolute Size Analysis

# Exclude N/A votes from the analysis but keep them for chapter size calculation
votes_df = df[df['slate_category'] != 'N/A']

# Calculate chapter sizes based on the original dataframe
chapter_sizes = df.groupby('DSA Chapter')['Voter'].count()

# Add chapter sizes to the votes_df
votes_df = votes_df.merge(chapter_sizes.rename('chapter_size'), left_on='DSA Chapter', right_index=True)

# Merge with the new dataframe
merged_df = votes_df.merge(new_df, left_on='DSA Chapter', right_on='Chapter', how='left')

#Relative Size Analysis

# Convert the % population (high) columns to numeric
merged_df['% population (high)'] = merged_df['% population (high)'].str.rstrip('%').astype('float') / 100

# Drop rows with missing values in the % population (high) column
merged_df = merged_df.dropna(subset=['% population (high)'])

# Calculate descriptive statistics for chapter sizes and % population (high) based on slate category
descriptive_stats_sizes = merged_df.groupby('slate_category')['chapter_size'].describe()
descriptive_stats_population_high = merged_df.groupby('slate_category')['% population (high)'].describe()

# Extract chapter sizes and % population (high) for each group
left_sizes = merged_df[merged_df['slate_category'] == 'left']['chapter_size']
moderate_sizes = merged_df[merged_df['slate_category'] == 'moderate']['chapter_size']
left_population_high = merged_df[merged_df['slate_category'] == 'left']['% population (high)']
moderate_population_high = merged_df[merged_df['slate_category'] == 'moderate']['% population (high)']

# Perform t-tests
t_stat_sizes, p_value_sizes = ttest_ind(left_sizes, moderate_sizes, equal_var=False)
t_stat_population_high, p_value_population_high = ttest_ind(left_population_high, moderate_population_high, equal_var=False)

# Print results
print("\nDescriptive Statistics (Absolute Chapter Size):")
print(descriptive_stats_sizes)
print("\nT-Test Results (Absolute Chapter Size):")
print(f"t-statistic: {t_stat_sizes}, p-value: {p_value_sizes}")

print("\nDescriptive Statistics (DSA % Population):")
print(descriptive_stats_population_high)
print("\nT-Test Results (DSA % Population):")
print(f"t-statistic: {t_stat_population_high}, p-value: {p_value_population_high}")

# Visualization for chapter sizes
plt.figure(figsize=(10, 6))
merged_df.boxplot(column='chapter_size', by='slate_category')
plt.title('Chapter Size by Slate Category')
plt.suptitle('')
plt.xlabel('Slate Category')
plt.ylabel('Chapter Size')
plt.savefig('chapter_size_by_slate_category.png')
plt.show()

# Visualization for % population (high)
plt.figure(figsize=(10, 6))
merged_df.boxplot(column='% population (high)', by='slate_category')
plt.title('DSA % Population by Slate Category')
plt.suptitle('')
plt.xlabel('Slate Category')
plt.ylabel('DSA % Population')
plt.savefig('dsa_%_population_by_slate_category.png')
plt.show()

# Logistic Regression Analysis

# Prepare the data: Encode the slate category as a binary variable (0 for moderate, 1 for left)
merged_df['slate_binary'] = merged_df['slate_category'].apply(lambda x: 1 if x == 'left' else 0)

# Extract the predictors (chapter size and % population (high)) and the target (slate binary)
X_sizes = merged_df[['chapter_size']]
X_population_high = merged_df[['% population (high)']]
y = merged_df['slate_binary']

# Fit the logistic regression model for chapter sizes
log_reg_sizes = LogisticRegression()
log_reg_sizes.fit(X_sizes, y)

# Get the coefficient and intercept for chapter sizes
coef_sizes = log_reg_sizes.coef_[0][0]
intercept_sizes = log_reg_sizes.intercept_[0]

# Calculate the odds ratio for chapter sizes
odds_ratio_sizes = np.exp(coef_sizes)

# Fit the logistic regression model for % population (high)
log_reg_population_high = LogisticRegression()
log_reg_population_high.fit(X_population_high, y)

# Get the coefficient and intercept for % population (high)
coef_population_high = log_reg_population_high.coef_[0][0]
intercept_population_high = log_reg_population_high.intercept_[0]

# Calculate the odds ratio for % population (high)
odds_ratio_population_high = np.exp(coef_population_high)

# Print results for logistic regression
print("\nLogistic Regression Results (Absolute Chapter Size):")
print(f"Coefficient: {coef_sizes}")
print(f"Intercept: {intercept_sizes}")
print(f"Odds Ratio: {odds_ratio_sizes}")

print("\nLogistic Regression Results (DSA % Population):")
print(f"Coefficient: {coef_population_high}")
print(f"Intercept: {intercept_population_high}")
print(f"Odds Ratio: {odds_ratio_population_high}\n")