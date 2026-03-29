from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(df):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("Cross-Border Recruiter Report", styles["Title"]))
    content.append(Spacer(1, 10))

    for _, row in df.iterrows():
        text = f"""
        <b>{row['Name']}</b><br/>
        Location: {row['Location']}<br/>
        GitHub: {row['GitHub']}<br/>
        LinkedIn: {row['LinkedIn']}<br/>
        Total Score: {row['Total Score']}<br/>
        Tech: {row['Tech Score']} | Culture: {row['Culture Score']} |
        Experience: {row['Experience Score']} | Location: {row['Location Score']}<br/>
        Reasons: {row['Reasons']}<br/><br/>
        """
        content.append(Paragraph(text, styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)