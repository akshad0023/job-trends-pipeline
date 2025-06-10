import pandas as pd
import os

# Load raw data
if not os.path.exists('data/rawjobs.csv'):
    raise FileNotFoundError("The file 'data/rawjobs.csv' was not found.")

df = pd.read_csv('data/rawjobs.csv')

# Drop irrelevant or empty columns
df = df.drop(columns=['job_url', 'crawl_timestamp'], errors='ignore')
df = df.dropna(subset=['job_title', 'location', 'job_description'])

# Clean salary field
def clean_salary(sal):
    if pd.isna(sal) or 'Not' in str(sal):
        return None
    sal = str(sal).replace('$', '').replace(',', '')
    try:
        return float(sal.split('-')[0])
    except (ValueError, IndexError):
        return None

df['min_salary'] = df['salary'].apply(clean_salary)

# Feature 1: Is Remote
df['is_remote'] = df['job_description'].str.contains('remote', case=False, na=False)

# Feature 2: Extract key skills (Python, SQL, Excel, etc.)
df['has_python'] = df['job_description'].str.contains('python', case=False, na=False)
df['has_sql'] = df['job_description'].str.contains(r'\bsql\b', case=False, na=False)
df['has_excel'] = df['job_description'].str.contains('excel', case=False, na=False)

# Feature 3: Salary Buckets
def salary_bucket(salary):
    if pd.isna(salary):
        return 'Unknown'
    elif salary < 50000:
        return 'Low'
    elif 50000 <= salary <= 100000:
        return 'Medium'
    else:
        return 'High'

df['salary_bucket'] = df['min_salary'].apply(salary_bucket)

# Save the cleaned data
df.to_csv('data/cleaned_jobs.csv', index=False)
print("✅ Cleaned data saved to data/cleaned_jobs.csv")