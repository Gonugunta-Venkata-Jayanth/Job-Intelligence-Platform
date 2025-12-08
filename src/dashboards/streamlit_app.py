import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import pandas as pd
import streamlit as st
from sqlalchemy import text
from src.db.session import engine, init_db
@st.cache_data(show_spinner=False)
def load_jobs_and_skills():
    """
    Load jobs, companies, locations, and skills into pandas DataFrames.
    """
    init_db()
    jobs_query = text(
        """
        SELECT
            j.id,
            j.title,
            j.source,
            j.url,
            j.description,
            c.name AS company,
            l.raw_location AS location,
            j.min_salary,
            j.max_salary,
            j.salary_pred_min,
            j.salary_pred_max,
            j.currency,
            j.scraped_at,
            j.posted_date
        FROM jobs j
        LEFT JOIN companies c ON j.company_id = c.id
        LEFT JOIN locations l ON j.location_id = l.id
        """
    )
    jobs_df = pd.read_sql(jobs_query, engine)
    skills_query = text(
        """
        SELECT
            js.job_id,
            s.name AS skill_name
        FROM job_skills js
        JOIN skills s ON js.skill_id = s.id
        """
    )
    skills_df = pd.read_sql(skills_query, engine)
    if not skills_df.empty:
        skills_agg = (
            skills_df.groupby("job_id")["skill_name"]
            .apply(lambda x: ", ".join(sorted(set(x))))
            .reset_index()
            .rename(columns={"skill_name": "skills"})
        )
        jobs_df = jobs_df.merge(skills_agg, how="left", left_on="id", right_on="job_id")
        jobs_df.drop(columns=["job_id"], inplace=True, errors="ignore")
    else:
        jobs_df["skills"] = None
    return jobs_df, skills_df
def filter_jobs(jobs_df: pd.DataFrame, skills_df: pd.DataFrame):
    """
    Apply filters from the sidebar and return a filtered DataFrame.
    """
    df = jobs_df.copy()
    st.sidebar.header("Filters")
    search_text = st.sidebar.text_input(
        "Search (title / company / location / description)",
        value="",
        placeholder="e.g. data engineer, python, hyderabad",
    )
    locations = sorted(
        [loc for loc in df["location"].dropna().unique()]
    )
    selected_locations = st.sidebar.multiselect(
        "Location(s)", options=locations, default=[]
    )
    skill_options = (
        sorted(skills_df["skill_name"].unique())
        if not skills_df.empty
        else []
    )
    selected_skills = st.sidebar.multiselect(
        "Skill(s)", options=skill_options, default=[]
    )
    use_predicted = st.sidebar.checkbox(
        "Use predicted salary when actual is missing", value=True
    )
    if search_text:
        mask = (
            df["title"].fillna("").str.contains(search_text, case=False, na=False)
            | df["company"].fillna("").str.contains(search_text, case=False, na=False)
            | df["location"].fillna("").str.contains(search_text, case=False, na=False)
            | df["description"].fillna("").str.contains(search_text, case=False, na=False)
        )
        df = df[mask]
    if selected_locations:
        df = df[df["location"].isin(selected_locations)]
    if selected_skills:
        for skill in selected_skills:
            df = df[df["skills"].fillna("").str.contains(skill, case=False, na=False)]
    df["salary_display"] = df["min_salary"]
    df["has_actual_salary"] = df["min_salary"].notna() & df["max_salary"].notna()
    if use_predicted:
        avg_pred = (df["salary_pred_min"] + df["salary_pred_max"]) / 2.0
        df.loc[~df["has_actual_salary"] & avg_pred.notna(), "salary_display"] = avg_pred
    return df
def main():
    st.set_page_config(
        page_title="Job Intelligence Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("📊 Job Intelligence Dashboard")
    st.caption("Data Engineer / Python-focused job market insights")
    jobs_df, skills_df = load_jobs_and_skills()
    if jobs_df.empty:
        st.warning("No jobs found in the database yet. Load some data first.")
        return
    filtered_df = filter_jobs(jobs_df, skills_df)
    col1, col2, col3, col4 = st.columns(4)
    total_jobs = len(filtered_df)
    total_companies = filtered_df["company"].nunique()
    total_locations = filtered_df["location"].nunique()
    if not skills_df.empty:
        top_skill_series = (
            skills_df["skill_name"]
            .value_counts()
            .head(1)
        )
        if not top_skill_series.empty:
            top_skill_name = top_skill_series.index[0]
            top_skill_count = int(top_skill_series.iloc[0])
        else:
            top_skill_name, top_skill_count = "N/A", 0
    else:
        top_skill_name, top_skill_count = "N/A", 0
    with col1:
        st.metric("Total Jobs (filtered)", f"{total_jobs}")
    with col2:
        st.metric("Companies (filtered)", f"{total_companies}")
    with col3:
        st.metric("Locations (filtered)", f"{total_locations}")
    with col4:
        st.metric("Top Skill (overall)", f"{top_skill_name}", f"{top_skill_count} jobs")
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📈 Skills Overview", "💰 Salary Insights", "📄 Jobs Table"])
    with tab1:
        st.subheader("Top Skills (overall)")
        if not skills_df.empty:
            skill_counts = (
                skills_df.groupby("skill_name")
                .size()
                .reset_index(name="count")
                .sort_values("count", ascending=False)
            )
            st.bar_chart(skill_counts.set_index("skill_name")["count"])
        else:
            st.info("No skills data available yet. Run the skill extractor.")
    with tab2:
        st.subheader("Salary distribution (filtered jobs)")
        salary_df = filtered_df.copy()
        salary_df["avg_actual_salary"] = (
            (salary_df["min_salary"] + salary_df["max_salary"]) / 2.0
        )
        salary_df["avg_pred_salary"] = (
            (salary_df["salary_pred_min"] + salary_df["salary_pred_max"]) / 2.0
        )
        plot_rows = []
        for _, row in salary_df.iterrows():
            if pd.notna(row["avg_actual_salary"]):
                plot_rows.append(
                    {
                        "title": row["title"],
                        "company": row["company"],
                        "location": row["location"],
                        "type": "Actual",
                        "avg_salary": row["avg_actual_salary"],
                    }
                )
            elif pd.notna(row["avg_pred_salary"]):
                plot_rows.append(
                    {
                        "title": row["title"],
                        "company": row["company"],
                        "location": row["location"],
                        "type": "Predicted",
                        "avg_salary": row["avg_pred_salary"],
                    }
                )
        if plot_rows:
            plot_df = pd.DataFrame(plot_rows)
            st.bar_chart(
                plot_df.set_index("title")[["avg_salary"]]
            )
            st.caption(
                "Note: For now, each bar is labeled by job title; in real data, "
                "you may aggregate by location, company, or skill instead."
            )
        else:
            st.info("No salary information (actual or predicted) available for the filtered jobs.")
    with tab3:
        st.subheader("Jobs (filtered)")

        display_cols = [
            "id",
            "title",
            "company",
            "location",
            "skills",
            "min_salary",
            "max_salary",
            "salary_pred_min",
            "salary_pred_max",
            "currency",
            "posted_date",
            "source",
            "url",
        ]
        display_df = filtered_df[display_cols].copy()
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )
        st.caption("Tip: Use sidebar filters to narrow down by location, skills, and search terms.")
if __name__ == "__main__":
    main()
