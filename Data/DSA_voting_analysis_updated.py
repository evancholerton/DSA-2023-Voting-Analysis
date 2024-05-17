import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from sklearn.linear_model import LogisticRegression
import numpy as np
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Update the file_path to be relative to the script directory
file_path_voting = os.path.join(script_dir, 'data', 'NPC 1st Place Vote by Chapter and Slate - NPC Raw Data.csv')
file_path_chapter_info = os.path.join(script_dir, 'data', 'dsa_chapters_info.csv')

# Load the CSV files
votes_df = pd.read_csv(file_path_voting)
chapter_info_df = pd.read_csv(file_path_chapter_info)

# Merge the dataframes on the 'chapter' column
merged_df = pd.merge(votes_df, chapter_info_df, on='chapter', how='left')

# List of moderate and left slates
moderate_slates = ["Groundwork", "North Star", "Socialist Majority Caucus"]
left_slates = ["Alexander Morash", "Brandy Pride", "Julius Kapushinski", "Luisa M.",
               "Anti-Zionist", "Bread & Roses", "Emerge", "Libertarian Socialist Caucus",
               "Marxist Unity Group", "Red Labor", "Red Star", "Reform & Revolution"]

# List of second choice candidates that determine if "Aaron Berger" voters are "left" or "moderate"
left_second_choices = ["Ahmed Husain", "C.S. Jackson", "Catherine Elias", "John Lewis", "Jorge Rocha",
                       "Kristin Schall", "Megan Romer", "Rashad X", "Sam Heft-Luthy", "Tom Julstrom"]
moderate_second_choices = ["Cara Tobe", "Colleen Johnston", "Grace Mausser", "Renée Paradis", "Rose DuBois"]

# Create a function to categorize slates
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

# Apply the categorization function
merged_df['slate_category'] = merged_df.apply(lambda row: categorize_slate(row['slate'], row['second_choice']), axis=1)

# Filter out rows with 'N/A' slate category
merged_df = merged_df[merged_df['slate_category'] != 'N/A']

# Analysis 1: Are smaller chapters more "left" than larger chapters?
merged_df['chapter_size'] = merged_df.groupby('chapter')['chapter'].transform('size')

# Descriptive statistics for chapter sizes based on slate category
descriptive_stats = merged_df.groupby('slate_category')['chapter_size'].describe()

# Extract chapter sizes for each group
left_sizes = merged_df[merged_df['slate_category'] == 'left']['chapter_size']
moderate_sizes = merged_df[merged_df['slate_category'] == 'moderate']['chapter_size']

# Perform t-test
t_stat, p_value = ttest_ind(left_sizes, moderate_sizes, equal_var=False)

# Print results
print("Descriptive Statistics (Chapter Size):")
print(descriptive_stats)
print("\\nT-Test Results (Chapter Size):")
print(f"t-statistic: {t_stat}, p-value: {p_value}")

# Visualization
plt.figure(figsize=(10, 6))
merged_df.boxplot(column='chapter_size', by='slate_category')
plt.title('Chapter Size by Slate Category')
plt.suptitle('')
plt.xlabel('Slate Category')
plt.ylabel('Chapter Size')
plt.savefig('chapter_size_by_slate_category.png')
plt.show()

# Logistic Regression Analysis for Chapter Size

# Prepare the data: Encode the slate category as a binary variable (0 for moderate, 1 for left)
merged_df['slate_binary'] = merged_df['slate_category'].apply(lambda x: 1 if x == 'left' else 0)

# Extract the predictor (chapter size) and the target (slate binary)
X = merged_df[['chapter_size']]
y = merged_df['slate_binary']

# Fit the logistic regression model
log_reg = LogisticRegression()
log_reg.fit(X, y)

# Get the coefficient and intercept
coef = log_reg.coef_[0][0]
intercept = log_reg.intercept_[0]

# Calculate the odds ratio
odds_ratio = np.exp(coef)

# Print results
print("\\nLogistic Regression Results (Chapter Size):")
print(f"Coefficient: {coef}")
print(f"Intercept: {intercept}")
print(f"Odds Ratio: {odds_ratio}")

# Visualization of the sigmoid function
chapter_size_range = pd.DataFrame({'chapter_size': np.linspace(X['chapter_size'].min(), X['chapter_size'].max(), 300)})
predicted_probabilities = log_reg.predict_proba(chapter_size_range)[:, 1]

plt.figure(figsize=(10, 6))
plt.plot(chapter_size_range['chapter_size'], predicted_probabilities, label='Sigmoid Curve')
plt.xlabel('Chapter Size')
plt.ylabel('Probability of Being Left')
plt.title('Probability of Being Left by Chapter Size')
plt.savefig('probability_left_by_chapter_size.png')
plt.show()

# Analysis 2: Are urban chapters more "moderate" than rural chapters?

# Descriptive statistics for urbanization percentage based on slate category
urbanization_stats = merged_df.groupby('slate_category')['urbanization_percentage'].describe()

# Extract urbanization percentages for each group
left_urban = merged_df[merged_df['slate_category'] == 'left']['urbanization_percentage']
moderate_urban = merged_df[merged_df['slate_category'] == 'moderate']['urbanization_percentage']

# Perform t-test
t_stat_urban, p_value_urban = ttest_ind(left_urban, moderate_urban, equal_var=False)

# Print results
print("\\nDescriptive Statistics (Urbanization Percentage):")
print(urbanization_stats)
print("\\nT-Test Results (Urbanization Percentage):")
print(f"t-statistic: {t_stat_urban}, p-value: {p_value_urban}")

# Logistic Regression Analysis for Urbanization Percentage

# Extract the predictor (urbanization percentage) and the target (slate binary)
X_urban = merged_df[['urbanization_percentage']]

# Fit the logistic regression model
log_reg_urban = LogisticRegression()
log_reg_urban.fit(X_urban, y)

# Get the coefficient and intercept
coef_urban = log_reg_urban.coef_[0][0]
intercept_urban = log_reg_urban.intercept_[0]

# Calculate the odds ratio
odds_ratio_urban = np.exp(coef_urban)

# Print results
print("\\nLogistic Regression Results (Urbanization Percentage):")
print(f"Coefficient: {coef_urban}")
print(f"Intercept: {intercept_urban}")
print(f"Odds Ratio: {odds_ratio_urban}")

# Visualization of the sigmoid function for urbanization percentage
urbanization_range = pd.DataFrame({'urbanization_percentage': np.linspace(X_urban['urbanization_percentage'].min(), X_urban['urbanization_percentage'].max(), 300)})
predicted_probabilities_urban = log_reg_urban.predict_proba(urbanization_range)[:, 1]

plt.figure(figsize=(10, 6))
plt.plot(urbanization_range['urbanization_percentage'], predicted_probabilities_urban, label='Sigmoid Curve')
plt.xlabel('Urbanization Percentage')
plt.ylabel('Probability of Being Left')
plt.title('Probability of Being Left by Urbanization Percentage')
plt.savefig('probability_left_by_urbanization_percentage.png')
plt.show()

# Analysis 3: Are higher-income chapters more "moderate" than lower-income chapters?

# Descriptive statistics for median income based on slate category
income_stats = merged_df.groupby('slate_category')['median_income'].describe()

# Extract median incomes for each group
left_income = merged_df[merged_df['slate_category'] == 'left']['median_income']
moderate_income = merged_df[merged_df['slate_category'] == 'moderate']['median_income']

# Perform t-test
t_stat_income, p_value_income = ttest_ind(left_income, moderate_income, equal_var=False)

# Print results
print("\\nDescriptive Statistics (Median Income):")
print(income_stats)
print("\\nT-Test Results (Median Income):")
print(f"t-statistic: {t_stat_income}, p-value: {p_value_income}")

# Logistic Regression Analysis for Median Income

# Extract the predictor (median income) and the target (slate binary)
X_income = merged_df[['median_income']]

# Fit the logistic regression model
log_reg_income = LogisticRegression()
log_reg_income.fit(X_income, y)

# Get the coefficient and intercept
coef_income = log_reg_income.coef_[0][0]
intercept_income = log_reg_income.intercept_[0]

# Calculate the odds ratio
odds_ratio_income = np.exp(coef_income)

# Print results
print("\\nLogistic Regression Results (Median Income):")
print(f"Coefficient: {coef_income}")
print(f"Intercept: {intercept_income}")
print(f"Odds Ratio: {odds_ratio_income}")

# Visualization of the sigmoid function for median income
income_range = pd.DataFrame({'median_income': np.linspace(X_income['median_income'].min(), X_income['median_income'].max(), 300)})
predicted_probabilities_income = log_reg_income.predict_proba(income_range)[:, 1]

plt.figure(figsize=(10, 6))
plt.plot(income_range['median_income'], predicted_probabilities_income, label='Sigmoid Curve')
plt.xlabel('Median Income')
plt.ylabel('Probability of Being Left')
plt.title('Probability of Being Left by Median Income')
plt.savefig('probability_left_by_median_income.png')
plt.show()

# Save the updated script with the correct paths to the data files
file_path_py_updated = '/mnt/data/DSA_voting_analysis_updated_corrected.py'
with open(file_path_py_updated, 'w') as file:
    file.write(script_part1 + script_part2 + script_part3)

file_path_py_updated