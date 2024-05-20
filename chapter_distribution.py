import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from scipy.stats import gaussian_kde

# Load the CSV file
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'NPC 1st Place Vote by Chapter and Slate - NPC Raw Data.csv')
    df = pd.read_csv(file_path)
    return df

# Calculate chapter sizes
def calculate_chapter_sizes(df):
    chapter_sizes = df.groupby('DSA Chapter')['Voter'].count()
    return chapter_sizes

# Plot PDF and CDF
def plot_distributions(chapter_sizes):
    # PDF
    plt.figure(figsize=(12, 6))
    sns.histplot(chapter_sizes, kde=True, stat="density", linewidth=0)
    plt.title('Probability Density Function of Chapter Sizes')
    plt.xlabel('Chapter Size')
    plt.ylabel('Density')
    plt.grid(True)
    plt.savefig('pdf_chapter_sizes.png')
    plt.show()

    # CDF
    plt.figure(figsize=(12, 6))
    sorted_sizes = np.sort(chapter_sizes)
    cdf = np.arange(1, len(sorted_sizes) + 1) / len(sorted_sizes)
    unique_sorted_sizes, unique_indices = np.unique(sorted_sizes, return_index=True)
    unique_cdf = cdf[unique_indices]
    plt.plot(sorted_sizes, cdf, marker='.', linestyle='none', label='Empirical CDF')

    # Smoothed CDF using Kernel Density Estimation with adjusted bandwidth
    kde_adjusted = gaussian_kde(chapter_sizes, bw_method=0.15)
    x = np.linspace(min(unique_sorted_sizes), max(unique_sorted_sizes), 1000)
    kde_values_adjusted = kde_adjusted.evaluate(x)
    kde_cdf_adjusted = np.cumsum(kde_values_adjusted)
    kde_cdf_adjusted /= kde_cdf_adjusted[-1]  # Normalize to get CDF

    plt.plot(x, kde_cdf_adjusted, linestyle='-', color='blue', label='Smoothed CDF (Adjusted KDE)')
    plt.title('Cumulative Distribution Function of Chapter Sizes')
    plt.xlabel('Chapter Size')
    plt.ylabel('CDF')
    plt.grid(True)
    plt.legend()
    plt.savefig('cdf_chapter_sizes.png')
    plt.show()

def main():
    # Load and preprocess data
    df = load_data()
    chapter_sizes = calculate_chapter_sizes(df)
    
    # Plot distributions
    plot_distributions(chapter_sizes)

if __name__ == "__main__":
    main()