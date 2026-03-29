import pandas as pd
import requests # is used to call api 

# =========================
# 📌 JOB DESCRIPTION AGENT
# =========================
jd = """
Data Analyst with Python, SQL, Power BI/Tableau.
2-5 years experience.
"""

def parse_jd(jd_text):
    jd_text = jd_text.lower()
    skills = []

    for skill in ["python", "sql", "power bi", "tableau"]:
        if skill in jd_text:
            skills.append(skill) # method appends an element to the end of the list.

    return skills

jd_skills = parse_jd(jd)

# =========================
# 🌐 GITHUB AGENT
# =========================
def fetch_github_users(skill, location): # skill and locations
    url = f"https://api.github.com/search/users?q={skill}+location:{location}&per_page=5"
    res = requests.get(url)
    data = res.json() # json respons

    users = []
    for u in data.get("items", []):
        users.append({
            "name": u["login"],
            "location": location,
            "skills": "Python, SQL, Tableau",
            "experience": "3 years",
            "experience_type": "Startup + Open-source contributor",
            "github": u["html_url"],
            "linkedin": "N/A"
        })
    return users

# =========================
# 🔗 LINKEDIN AGENT (SIMULATED)
# =========================
def fetch_linkedin_users(role, location):
    users = []

    for i in range(5):
        users.append({
            "name": f"{role}_{location}_{i}",
            "location": location,
            "skills": "Python, SQL, Power BI",
            "experience": "3 years",
            "experience_type": "Startup + Product company",
            "github": "N/A",
            "linkedin": f"https://linkedin.com/in/{role}_{location}_{i}"
        })

    return users

# =========================
# 🤖 SCORING AGENT
# =========================
def evaluate_candidate(candidate, region, jd_skills):
    tech_score = 0
    culture_score = 0
    exp_score = 0
    location_score = 1

    reasons = []

    skills = candidate["skills"].lower()
    exp_type = candidate["experience_type"].lower()
    years = int(candidate["experience"].split()[0])

    # 🔧 TECH MATCH
    for skill in jd_skills:
        if skill in skills:
            tech_score += 2

            reasons.append(f"{skill} match")

    # 📊 EXPERIENCE
    if 2 <= years <= 5:
        exp_score = 2
        reasons.append("Experience match (2-5 yrs)")

    # 🌍 CULTURE
    if region == "Riyadh":
        if "vision 2030" in exp_type:
            culture_score += 3
            reasons.append("Vision 2030")
        if "gcc" in exp_type:
            culture_score += 2
            reasons.append("GCC experience")

    if region == "Hyderabad":
        if "startup" in exp_type:
            culture_score += 3
            reasons.append("Startup experience")
        if "product" in exp_type:
            culture_score += 2
            reasons.append("Product company")

    total_score = tech_score + culture_score + exp_score + location_score

    return {
        "Tech Score": tech_score,
        "Culture Score": culture_score,
        "Experience Score": exp_score,
        "Location Score": location_score,
        "Total Score": total_score,
        "Reasons": ", ".join(reasons)
    }

# =========================
# 🔄 PIPELINE
# =========================
riyadh_github = fetch_github_users("python", "riyadh")
hyd_github = fetch_github_users("python", "hyderabad")

riyadh_linkedin = fetch_linkedin_users("data_analyst", "riyadh")
hyd_linkedin = fetch_linkedin_users("data_analyst", "hyderabad")

all_candidates = (
    riyadh_github +
    hyd_github +
    riyadh_linkedin +
    hyd_linkedin
)

results = []

for c in all_candidates:
    region = "Riyadh" if "riyadh" in c["location"].lower() else "Hyderabad"
    score_data = evaluate_candidate(c, region, jd_skills)

    results.append({
        "Name": c["name"],
        "Location": c["location"],
        "GitHub": c["github"],
        "LinkedIn": c["linkedin"],
        **score_data
    })

df = pd.DataFrame(results)
df = df.sort_values(by="Total Score", ascending=False)

df.to_csv("final_candidates.csv", index=False)

print("✅ Agent run complete. Results saved.")

# =========================
# 📄 GENERATE PDF
# =========================
from report import generate_pdf
generate_pdf(df)