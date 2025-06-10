import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv('data/cleaned_jobs.csv')

st.set_page_config(layout="wide")
st.title("📊 Tech Job Trends Interactive Dashboard")

# Sidebar filter
st.sidebar.header("🔍 Filter Jobs")
locations = st.sidebar.multiselect("Select Location(s):", options=df['location'].dropna().unique())

# Seniority filter
seniorities = st.sidebar.multiselect("Select Seniority Level(s):", options=df['seniority'].dropna().unique())

# Skill filters
st.sidebar.subheader("Filter by Skills")
has_python = st.sidebar.checkbox("Python")
has_sql = st.sidebar.checkbox("SQL")
has_excel = st.sidebar.checkbox("Excel")
has_aws = st.sidebar.checkbox("AWS")

filtered_df = df
if locations:
    filtered_df = filtered_df[filtered_df['location'].isin(locations)]

if seniorities:
    filtered_df = filtered_df[filtered_df['seniority'].isin(seniorities)]

# Filter by selected skills
if has_python:
    filtered_df = filtered_df[filtered_df['has_python'] == True]
if has_sql:
    filtered_df = filtered_df[filtered_df['has_sql'] == True]
if has_excel:
    filtered_df = filtered_df[filtered_df['has_excel'] == True]
if has_aws:
    filtered_df = filtered_df[filtered_df['has_aws'] == True]

# Download filtered data
csv = filtered_df.to_csv(index=False)
st.sidebar.download_button("⬇️ Download Filtered Data", csv, "filtered_jobs.csv", "text/csv")

# Summary Stats
st.markdown("## 🔢 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", len(filtered_df))
if len(filtered_df) > 0:
    remote_pct = filtered_df['is_remote'].mean() * 100
    avg_min_salary = filtered_df['min_salary'].mean()
else:
    remote_pct = 0
    avg_min_salary = 0
col2.metric("Remote Jobs (%)", f"{remote_pct:.2f}%")
col3.metric("Average Min Salary", f"${avg_min_salary:,.2f}")

# Skill counts metrics
skill_cols = []
if has_python:
    skill_cols.append('Python')
if has_sql:
    skill_cols.append('SQL')
if has_excel:
    skill_cols.append('Excel')
if has_aws:
    skill_cols.append('AWS')

if skill_cols:
    skill_counts = []
    for skill in skill_cols:
        col_name = f'has_{skill.lower()}'
        count = filtered_df[col_name].sum()
        skill_counts.append((skill, count))
    cols = st.columns(len(skill_counts))
    for i, (skill, count) in enumerate(skill_counts):
        cols[i].metric(f"Jobs Requiring {skill}", count)

# Tabs
tab1, tab2 = st.tabs(["📄 Data Preview", "📈 Visualizations"])

with tab1:
    st.dataframe(filtered_df)

with tab2:
    # Plot 1: Salary Distribution
    st.subheader("Salary Distribution")
    fig1, ax1 = plt.subplots()
    sns.histplot(filtered_df['min_salary'].dropna(), bins=30, kde=True, ax=ax1)
    st.pyplot(fig1)

    # Plot 2: Python Skill Presence
    st.subheader("Jobs Requiring Python")
    fig2, ax2 = plt.subplots()
    sns.countplot(x='has_python', data=filtered_df, ax=ax2)
    ax2.set_xticklabels(['No', 'Yes'])
    st.pyplot(fig2)

    # Plot 3: Bar chart for selected skills
    if skill_cols:
        st.subheader("Jobs by Selected Skill")
        skill_counts_df = pd.DataFrame(skill_counts, columns=['Skill', 'Count'])
        fig3, ax3 = plt.subplots()
        sns.barplot(x='Skill', y='Count', data=skill_counts_df, ax=ax3)
        ax3.set_ylabel('Number of Jobs')
        st.pyplot(fig3)

    # Plot 4: Bar chart for seniority counts
    st.subheader("Jobs by Seniority Level")
    seniority_counts = filtered_df['seniority'].value_counts().reset_index()
    seniority_counts.columns = ['Seniority', 'Count']
    fig4, ax4 = plt.subplots()
    sns.barplot(x='Seniority', y='Count', data=seniority_counts, ax=ax4)
    ax4.set_ylabel('Number of Jobs')
    ax4.set_xlabel('Seniority Level')
    st.pyplot(fig4)