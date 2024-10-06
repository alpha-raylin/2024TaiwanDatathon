import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv('TMU.csv') 

# Categorize age and gender
df['age_category'] = df['age'].apply(lambda x: 'Young' if x < 50 else 'Old')
df['gender_category'] = df['gender'].apply(lambda x: 'Male' if x == 1 else 'Female')

# Group by age, gender categories, and mortality
counts = df.groupby(['age_category', 'gender_category', 'mortality']).size().reset_index(name='counts')

# Pivot the data for easier plotting
pivot_counts = counts.pivot_table(index=['age_category', 'gender_category'], 
                                   columns='mortality', 
                                   values='counts', 
                                   fill_value=0).reset_index()

# Rename columns for clarity
pivot_counts.columns.name = None  # Remove the name of the columns
pivot_counts.columns = ['age_category', 'gender_category', 'Survived', 'Died']

# Calculate the death rate for each group
pivot_counts['Total'] = pivot_counts['Survived'] + pivot_counts['Died']
pivot_counts['Death Rate (%)'] = (pivot_counts['Died'] / pivot_counts['Total']) * 100

# Plotting
plt.figure(figsize=(10, 6))

# Set bar width
bar_width = 0.35
x = range(len(pivot_counts))

# Create bars for each mortality category
plt.bar(x, pivot_counts['Survived'], width=bar_width, label='Survived (0)', color='#1f77b4')
plt.bar([p + bar_width for p in x], pivot_counts['Died'], width=bar_width, label='Died (1)', color='#ff7f0e')

# Add death rate annotations above the bars
for i in range(len(pivot_counts)):
    death_rate_text = f"{pivot_counts['Death Rate (%)'].iloc[i]:.1f}%"
    plt.text(i + bar_width / 2, pivot_counts['Died'].iloc[i] + 2, death_rate_text, ha='center', fontsize=10, color='black')

# Customize the plot
plt.xlabel('Group', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title('TMU Count of Mortality by Age and Gender Categories', fontsize=14)
plt.xticks([p + bar_width / 2 for p in x], 
           [f"{row['age_category']} {row['gender_category']}" for _, row in pivot_counts.iterrows()])

# Add legends
plt.legend()

plt.tight_layout()
plt.savefig('figure/tmu_bar.png')

# Show the plot
plt.show()
