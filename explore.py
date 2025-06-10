import pandas as pd

# Load cleaned data
df = pd.read_csv('data/cleaned_jobs.csv')

# Quick look at data shape and columns
print(f"Rows: {len(df)}")
print(f"Columns: {df.columns.tolist()}")

# Preview first 5 rows
print(df.head())

import matplotlib.pyplot as plt
import seaborn as sns

# Plot salary distribution histogram
plt.figure(figsize=(10,6))
sns.histplot(df['min_salary'].dropna(), bins=30, kde=True)
plt.title('Minimum Salary Distribution')
plt.xlabel('Salary ($)')
plt.ylabel('Number of Jobs')
plt.savefig('screenshots/salary_distribution.png')
plt.show()

# Count how many jobs require Python
python_jobs = df['has_python'].sum()
total_jobs = len(df)
print(f"Python jobs: {python_jobs} out of {total_jobs} ({python_jobs/total_jobs:.2%})")

# Bar plot for Python skill presence
plt.figure(figsize=(6,4))
sns.countplot(x='has_python', data=df)
plt.title('Jobs Requiring Python')
plt.xlabel('Has Python Skill')
plt.ylabel('Count')
plt.xticks([0,1], ['No', 'Yes'])
plt.savefig('screenshots/python_skill_presence.png')
plt.show()

input("Press Enter to exit...")