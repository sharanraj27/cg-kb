# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_neo4j import Neo4jGraph
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI()

# Allow CORS for Flutter (mobile/web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your Flutter app URL
    allow_methods=["*"],
    allow_headers=["*"]
)

# Input model
class UserInput(BaseModel):
    skills: list[str]
    personality: list[str]

# -----------------------------
# 1. Connect to Neo4j
# -----------------------------
graph = Neo4jGraph(
    url="bolt://localhost:7687",
    username="neo4j",
    password="sharan,27"
)

# -----------------------------
# 2. Setup LLM fallback
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key="AIzaSyDkFS_LBSh4k7sutswW9PYwONZXkEPza5Q"
)

# -----------------------------
# 3. Endpoint for Flutter
# -----------------------------
@app.post("/recommend-careers")
def recommend_careers(user_input: UserInput):
    # Normalize input
    skills_list = [s.strip().lower() for s in user_input.skills]
    personality_list = [p.strip().lower() for p in user_input.personality]

    skills_str = "[" + ",".join(f'"{s}"' for s in skills_list) + "]"
    personality_str = "[" + ",".join(f'"{p}"' for p in personality_list) + "]"

    # Query Neo4j
    cypher = f"""
    MATCH (p:Personality)-[:SUITED_FOR]->(c:Career)<-[:REQUIRES_SKILL]-(s:Skill)
    WHERE toLower(p.name) IN {personality_str} AND toLower(s.name) IN {skills_str}
    RETURN DISTINCT c.career AS career, collect(DISTINCT s.name) AS matched_skills, collect(DISTINCT p.name) AS matched_personality
    """

    results = graph.query(cypher)

    if not results:
        # Fallback to LLM
        prompt = f"""
        The user has these skills: {skills_list} and these personality traits: {personality_list}.
        Suggest suitable careers with description.
        """
        response = llm.invoke(prompt)
        return {"fallback_text": response.content}

    # Structure results
    careers_data = []
    for r in results:
        careers_data.append({
            "career": r["career"],
            "skills_matched": r["matched_skills"],
            "personality_matched": r["matched_personality"]
        })

    return {"careers": careers_data}

# -----------------------------
# 4. Run locally
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=9000, reload=True)
