import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Update the file_path to be relative to the script directory
file_path = os.path.join(script_dir, 'NPC 1st Place Vote by Chapter and Slate - NPC Raw Data.csv')

# Load the CSV file
df = pd.read_csv(file_path)

# List of moderate and left slates
moderate_slates = ["Aaron Berger", "Groundwork", "North Star", "Socialist Majority Caucus"]
left_slates = ["Alexander Morash", "Brandy Pride", "Julius Kapushinski", "Luisa M.", 
               "Anti-Zionist", "Bread & Roses", "Emerge", "Libertarian Socialist Caucus", 
               "Marxist Unity Group", "Red Labor", "Red Star", "Reform & Revolution"]

# Create a column to categorize the slates as 'moderate', 'left', or 'N/A'
def categorize_slate(slate):
    if slate in moderate_slates:
        return 'moderate'
    elif slate in left_slates:
        return 'left'
    else:
        return 'N/A'

df['slate_category'] = df['Slate'].apply(categorize_slate)

# Exclude N/A votes from the analysis but keep them for chapter size calculation
votes_df = df[df['slate_category'] != 'N/A']

# Calculate chapter sizes based on the original dataframe
chapter_sizes = df.groupby('DSA Chapter')['Voter'].count()

# Add chapter sizes to the votes_df
votes_df = votes_df.merge(chapter_sizes.rename('chapter_size'), left_on='DSA Chapter', right_index=True)

# Calculate descriptive statistics for chapter sizes based on slate category
descriptive_stats = votes_df.groupby('slate_category')['chapter_size'].describe()

# Extract chapter sizes for each group
left_sizes = votes_df[votes_df['slate_category'] == 'left']['chapter_size']
moderate_sizes = votes_df[votes_df['slate_category'] == 'moderate']['chapter_size']

# Perform t-test
t_stat, p_value = ttest_ind(left_sizes, moderate_sizes, equal_var=False)

# Print results
print("Descriptive Statistics:")
print(descriptive_stats)
print("\\nT-Test Results:")
print(f"t-statistic: {t_stat}, p-value: {p_value}")

# Visualization
plt.figure(figsize=(10, 6))
votes_df.boxplot(column='chapter_size', by='slate_category')
plt.title('Chapter Size by Slate Category')
plt.suptitle('')
plt.xlabel('Slate Category')
plt.ylabel('Chapter Size')
plt.savefig('chapter_size_by_slate_category.png')
plt.show()