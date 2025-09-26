from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_neo4j import Neo4jGraph
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model
class UserInput(BaseModel):
    skills: list[str]
    personality: list[str]

# -----------------------------
# Setup LLM
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key="YOUR_GOOGLE_API_KEY"
)

# -----------------------------
# Connect to Neo4j
# -----------------------------
graph = Neo4jGraph(
    url="bolt://localhost:7687",
    username="neo4j",
    password="sharan,27"
)

@app.post("/get-careers")
def get_careers(user_input: UserInput):
    # Normalize input
    skills_list = [s.strip().lower() for s in user_input.skills]
    personality_list = [p.strip().lower() for p in user_input.personality]

    skills_str = "[" + ",".join(f'"{s}"' for s in skills_list) + "]"
    personality_str = "[" + ",".join(f'"{p}"' for p in personality_list) + "]"

    # Cypher query
    cypher = f"""
    MATCH (p:Personality)-[:SUITED_FOR]->(c:Career)<-[:REQUIRES_SKILL]-(s:Skill)
    WHERE toLower(p.name) IN {personality_str} AND toLower(s.name) IN {skills_str}
    RETURN DISTINCT c.career AS career, collect(DISTINCT s.name) AS matched_skills, collect(DISTINCT p.name) AS matched_personality
    """

    results = graph.query(cypher)

    if not results:
        # If no data in DB, fallback to LLM-based suggestion
        prompt = f"""
        The user has these skills: {skills_list} and these personality traits: {personality_list}.
        Suggest suitable careers with description.
        """
        response = llm.invoke(prompt)
        # Parse LLM response to dictionary (simple fallback)
        # Here we just return the raw text for simplicity
        return {"fallback_text": response.content}

    # Structure careers data
    careers_data = {}
    for r in results:
        career_name = r["career"]
        skills = r["matched_skills"]
        personality = r["matched_personality"]
        description = f"Skills matched: {skills}. Personality matched: {personality}."
        careers_data[career_name] = description

    return careers_data
