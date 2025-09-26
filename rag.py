from langchain_neo4j import Neo4jGraph
from langchain_google_genai import ChatGoogleGenerativeAI

# -----------------------------
# 1. Setup LLM (Gemini)
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key="AIzaSyCSqcZqt7pUQIzP6VBlVd1pJ_E6Uh3FBfo"  # replace with your actual API key
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
# 3. Ask for career name
# -----------------------------
career_name = input("Enter the career name: ")  # e.g., "AR/VR Developer"

# -----------------------------
# 4. Fetch skills from Neo4j manually
# -----------------------------
cypher = f"""
MATCH (c:Career {{career: '{career_name}'}})-[:REQUIRES_SKILL]->(s:Skill)
RETURN s.name AS skill
"""

results = graph.query(cypher)  # returns a list of dictionaries
skills = [r["skill"] for r in results]

if not skills:
    print(f"No skills found for career '{career_name}'.")
else:
    skills = [r["skill"] for r in results if r["skill"] is not None]

    # -----------------------------
    # 5. Generate summary with LLM
    # -----------------------------
    prompt = f"A {career_name} needs these skills: {skills}. Summarize them in simple words."
    response = llm.invoke(prompt)

    # -----------------------------
    # 6. Print summarized skills
    # -----------------------------
    print("\nSkill Summary:\n")
    print(response.content)
