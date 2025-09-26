from langchain_neo4j import Neo4jGraph
from langchain_google_genai import ChatGoogleGenerativeAI

# -----------------------------
# 1. Setup LLM (Gemini)
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key="AIzaSyDkFS_LBSh4k7sutswW9PYwONZXkEPza5Q"  # replace with your valid Gemini API key
)

# -----------------------------
# 2. Connect to Neo4j
# -----------------------------
graph = Neo4jGraph(
    url="bolt://localhost:7687",
    username="neo4j",
    password="sharan,27"
)

# -----------------------------
# 3. Ask for user input
# -----------------------------
user_skills = input("Enter your skills (comma separated): ")  # e.g., "Python, SQL, Data Analysis"
user_personality = input("Enter your personality traits (comma separated): ")  # e.g., "Visionary, Confident, Strategic"

# Normalize input (strip + lowercase)
skills_list = [s.strip().lower() for s in user_skills.split(",")]
personality_list = [p.strip().lower() for p in user_personality.split(",")]

# Convert to Neo4j list string
skills_str = "[" + ",".join(f'"{s}"' for s in skills_list) + "]"
personality_str = "[" + ",".join(f'"{p}"' for p in personality_list) + "]"

# -----------------------------
# 4. Query careers from Neo4j
# -----------------------------
cypher = f"""
MATCH (p:Personality)-[:SUITED_FOR]->(c:Career)<-[:REQUIRES_SKILL]-(s:Skill)
WHERE toLower(p.name) IN {personality_str} AND toLower(s.name) IN {skills_str}
RETURN DISTINCT c.career AS career, collect(DISTINCT s.name) AS matched_skills, collect(DISTINCT p.name) AS matched_personality
"""

results = graph.query(cypher)

careers = [r["career"] for r in results]
matched = {r["career"]: {"skills": r["matched_skills"], "personality": r["matched_personality"]} for r in results}

    # -----------------------------
    # 5. Ask LLM to suggest best career
    # -----------------------------
prompt = f"""
The user has these skills: {skills_list} and these personality traits: {personality_list}.
From the database, possible careers are: {careers} with matched details {matched}.
Suggest the most suitable career(s) and explain why in simple terms.
"""

response = llm.invoke(prompt)

    # -----------------------------
    # 6. Print result
    # -----------------------------
print("\n🎯 Career Recommendation:\n")
print(response.content)
