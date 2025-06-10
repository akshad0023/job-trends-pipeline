import pandas as pd

# Load the cleaned data
df = pd.read_csv('data/cleaned_jobs.csv')

# Print all column names
print("Columns in cleaned_jobs.csv:", df.columns.tolist())

# Show first 5 rows of key columns if they exist
cols_to_check = ['min_salary', 'is_remote', 'seniority', 'has_python', 'has_sql', 'has_aws', 'has_excel']
existing_cols = [col for col in cols_to_check if col in df.columns]

print("\nSample data:")
print(df[existing_cols].head())