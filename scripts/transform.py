import pandas as pd

# Load raw data from google drive
url = "https://drive.google.com/uc?export=download&id=1DijQab20Be2MVsHUE7ZBFFCM-VJKSWib"
df = pd.read_csv(url)

# Extract skill columns based on job_description
df['has_python'] = df['job_description'].str.contains('python', case=False, na=False)
df['has_sql'] = df['job_description'].str.contains('sql', case=False, na=False)
df['has_excel'] = df['job_description'].str.contains('excel', case=False, na=False)
df['has_aws'] = df['job_description'].str.contains('aws', case=False, na=False)
df['is_remote'] = df['job_description'].str.contains('remote', case=False, na=False)

# Define function to determine seniority from job_title
def get_seniority(title):
    title = str(title).lower()
    if any(x in title for x in ['senior', 'sr', 'lead', 'principal', 'manager', 'director', 'vp', 'head']):
        return 'Senior'
    elif any(x in title for x in ['junior', 'jr', 'associate', 'entry', 'intern']):
        return 'Junior'
    else:
        return 'Mid'


# Create seniority column
df['seniority'] = df['job_title'].apply(get_seniority)

# Extract min_salary from salary column
import re
import numpy as np

def parse_min_salary(salary_str):
    if pd.isna(salary_str):
        return np.nan
    salary_str = str(salary_str).lower().replace('$', '').replace(',', '')
    nums = re.findall(r'\d+', salary_str)
    if nums:
        return int(nums[0])
    return np.nan

df['min_salary'] = df['salary'].apply(parse_min_salary)

# Save cleaned data
df.to_csv('data/cleaned_jobs.csv', index=False)