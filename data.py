import os
import csv

# Create data folder if not exists
os.makedirs("data", exist_ok=True)

# --- 1. personality.csv ---
personality_data = [
    ["personality_type", "traits", "suggested_careers"],
    ["INTJ", "Strategic, independent, logical", "Data Scientist, Engineer"],
    ["ENFP", "Creative, social, adaptive", "Marketing, UX Designer"],
]

with open("data/personality.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(personality_data)


# --- 2. careers.csv ---
careers_data = [
    ["career", "description", "required_skills"],
    ["Data Scientist", "Works with data to generate insights", "Python, ML, Statistics"],
    ["UX Designer", "Designs user-centered digital experiences", "Figma, UI/UX principles, HTML"],
]

with open("data/careers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(careers_data)


# --- 3. institutions.csv ---
institutions_data = [
    ["institution", "location", "courses_offered"],
    ["IIT Madras", "Chennai", "AI/ML, Data Science, Engineering"],
    ["NID Ahmedabad", "Ahmedabad", "Design, UX, Product Design"],
]

with open("data/institutions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(institutions_data)


# --- 4. paths.csv ---
paths_data = [
    ["career", "education_path", "additional_certifications"],
    ["Data Scientist", "B.Tech → MS in Data Science", "Coursera ML, Google Cloud ML"],
    ["UX Designer", "B.Des → M.Des in Interaction Design", "Adobe XD, Human-Centered Design"],
]

with open("data/paths.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(paths_data)


# --- 5. skills.csv ---
skills_data = [
    ["skill", "category", "related_careers"],
    ["Python", "Programming", "Data Scientist, AI Engineer"],
    ["Figma", "Design", "UX Designer, Product Designer"],
]

with open("data/skills.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(skills_data)


# --- 6. jobs.csv ---
jobs_data = [
    ["job_id", "career", "company", "location", "salary_range"],
    [1, "Data Scientist", "Google", "Bangalore", "₹12–18 LPA"],
    [2, "UX Designer", "Zoho Corp", "Chennai", "₹8–14 LPA"],
]

with open("data/jobs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(jobs_data)


print("✅ CSVs generated inside ./data/")
