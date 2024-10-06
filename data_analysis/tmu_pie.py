import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv('TMU.csv') 


# Age classification

young_male = df[(df['age'] < 50) & (df['gender'] == 1)].shape[0]
young_female = df[(df['age'] < 50) & (df['gender'] == 0)].shape[0]
old_male = df[(df['age'] >= 50) & (df['gender'] == 1)].shape[0]
old_female = df[(df['age'] >= 50) & (df['gender'] == 0)].shape[0]

# Result summary
result = {
    'Young Male': young_male,
    'Old Male': old_male,
    'Young Female': young_female,
    'Old Female': old_female
}

print(result)

# Create pie chart
labels = result.keys()
sizes = result.values()
colors = ['paleturquoise', 'skyblue', 'salmon',  'lightpink']  # Colors for each slice
explode = (0, 0, 0, 0)  # Highlight the first slice (Young Male)

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, explode=explode)
plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
plt.title('TMU Age and Gender Distribution', fontsize=14)
plt.savefig('figure/tmu_pie_1.png')

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

# Create pie charts
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
colors = ['salmon', 'skyblue', 'lightpink', 'paleturquoise']  # Colors for each slice
# Pie chart for survivors
axs[0].pie(pivot_counts['Survived'], 
           labels=[f"{row['age_category']} {row['gender_category']}" for _, row in pivot_counts.iterrows()], 
           autopct='%1.1f%%', 
           startangle=90, 
           colors=colors)
axs[0].axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
axs[0].set_title('Survived (0) Distribution', fontsize=14)

# Pie chart for deaths
axs[1].pie(pivot_counts['Died'], 
           labels=[f"{row['age_category']} {row['gender_category']}" for _, row in pivot_counts.iterrows()], 
           autopct='%1.1f%%', 
           startangle=90, 
           colors=colors)
axs[1].axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
axs[1].set_title('Died (1) Distribution', fontsize=14)

# Show the pie charts
plt.tight_layout()

plt.savefig('figure/tmu_pie_2.png')
