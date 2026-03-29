import streamlit as st
import pandas as pd
import subprocess

st.set_page_config(page_title="Recruiter AI", layout="wide")

st.title("🌍 Cross-Border Recruiter Agent")

jd = st.text_area("📄 Enter Job Description")

if st.button("🚀 Run Agent"):
    # Save JD to file (so main.py can read if needed)
    with open("jd.txt", "w") as f:
        f.write(jd)

    # Run backend agent
    subprocess.run(["python", "main.py"])

    df = pd.read_csv("final_candidates.csv")

    st.subheader("🏆 Top Candidates")
    st.dataframe(df)

    st.subheader("📊 Score Distribution")
    st.bar_chart(df["Total Score"])

    st.subheader("🧠 Fit Score Breakdown")
    st.dataframe(df[[
        "Name", "Tech Score", "Culture Score",
        "Experience Score", "Location Score", "Total Score"
    ]])

    # PDF download
    try:
        with open("report.pdf", "rb") as f:
            st.download_button("📄 Download PDF Report", f, file_name="report.pdf")
    except:
        st.warning("⚠️ PDF not found. Run agent first.")