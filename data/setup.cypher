/* ---------------------------
   0. Constraints & indexes
   --------------------------- */
CREATE CONSTRAINT FOR (c:Career) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT FOR (s:Skill) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT FOR (i:Institution) REQUIRE i.id IS UNIQUE;
CREATE CONSTRAINT FOR (j:Job) REQUIRE j.job_id IS UNIQUE;
CREATE CONSTRAINT FOR (p:Personality) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT FOR (path:Path) REQUIRE path.id IS UNIQUE;

/* ---------------------------
   1. Load Career nodes
   headers: id,career,description,required_skills
   --------------------------- */
LOAD CSV WITH HEADERS FROM 'file:///careers.csv' AS row
MERGE (c:Career {id: row.id})
SET c.name = row.career,
    c.description = row.description,
    c.required_skills = row.required_skills;

/* ---------------------------
   2. Load Skill nodes
   headers: id,skill,category,related_careers  (skills_fixed.csv)
   --------------------------- */
LOAD CSV WITH HEADERS FROM 'file:///skills_fixed.csv' AS row
MERGE (s:Skill {id: row.id})
SET s.name = row.skill,
    s.category = row.category,
    s.related_careers = row.related_careers;

/* ---------------------------
   3. Load Institution nodes
   headers: id,institution,location,courses_offered
   --------------------------- */
LOAD CSV WITH HEADERS FROM 'file:///institutions.csv' AS row
MERGE (i:Institution {id: row.id})
SET i.name = row.institution,
    i.location = row.location,
    i.courses_offered = row.courses_offered;

/* ---------------------------
   4. Load Job nodes
   headers: job_id,career,company,location,salary_range
   --------------------------- */
LOAD CSV WITH HEADERS FROM 'file:///jobs.csv' AS row
MERGE (j:Job {job_id: row.job_id})
SET j.title = row.career,
    j.company = row.company,
    j.location = row.location,
    j.salary_range = row.salary_range;

/* ---------------------------
   5. Load Path nodes
   headers: id,career,education_path,additional_certifications
   --------------------------- */
LOAD CSV WITH HEADERS FROM 'file:///paths.csv' AS row
MERGE (p:Path {id: row.id})
SET p.career = row.career,
    p.education_path = row.education_path,
    p.additional_certifications = row.additional_certifications;

/* ---------------------------
   6. Load Personality nodes
   headers: id,personality_type,traits,suggested_careers
   --------------------------- */
LOAD CSV WITH HEADERS FROM 'file:///personality.csv' AS row
MERGE (pp:Personality {id: row.id})
SET pp.personality_type = row.personality_type,
    pp.traits = row.traits,
    pp.suggested_careers = row.suggested_careers;

/* ---------------------------
   7. Create Skill <-> Career relationships using skills_fixed.related_careers
      (skills_fixed.related_careers is comma-separated list of career names)
   --------------------------- */
LOAD CSV WITH HEADERS FROM 'file:///skills_fixed.csv' AS row
WITH row, split(row.related_careers, ',') AS careerNames
UNWIND careerNames AS careerName
WITH row, trim(careerName) AS careerNameTrim
MATCH (s:Skill {id: row.id})
MATCH (c:Career)
WHERE toLower(c.name) = toLower(careerNameTrim)
MERGE (c)-[:REQUIRES]->(s);

/* ---------------------------
   8. Create Career -> Skill using careers.required_skills (comma-separated)
   --------------------------- */
LOAD CSV WITH HEADERS FROM 'file:///careers.csv' AS row
WITH row, split(row.required_skills, ',') AS skillNames
UNWIND skillNames AS skillName
WITH row, trim(skillName) AS skillNameTrim
MATCH (c:Career {id: row.id})
MATCH (s:Skill)
WHERE toLower(s.name) = toLower(skillNameTrim)
MERGE (c)-[:REQUIRES]->(s);

/* ---------------------------
   9. Personality -> Career using personality.suggested_careers (comma-separated)
   --------------------------- */
LOAD CSV WITH HEADERS FROM 'file:///personality.csv' AS row
WITH row, split(row.suggested_careers, ',') AS careerNames
UNWIND careerNames AS careerName
WITH row, trim(careerName) AS careerNameTrim
MATCH (p:Personality {id: row.id})
MATCH (c:Career)
WHERE toLower(c.name) = toLower(careerNameTrim)
MERGE (p)-[:SUITED_FOR]->(c);

/* ---------------------------
   10. Career -> Job (jobs.csv)
   --------------------------- */
LOAD CSV WITH HEADERS FROM 'file:///jobs.csv' AS row
MATCH (c:Career) WHERE toLower(c.name) = toLower(row.career)
MATCH (j:Job {job_id: row.job_id})
MERGE (c)-[:HAS_JOB]->(j);

/* ---------------------------
   11. Career -> Path (paths.csv)
   --------------------------- */
LOAD CSV WITH HEADERS FROM 'file:///paths.csv' AS row
MATCH (c:Career) WHERE toLower(c.name) = toLower(row.career)
MATCH (p:Path {id: row.id})
MERGE (c)-[:HAS_PATH]->(p);

/* ---------------------------
   12. Institution -> Course nodes (split courses_offered) and relationship
   --------------------------- */
LOAD CSV WITH HEADERS FROM 'file:///institutions.csv' AS row
WITH row, split(row.courses_offered, ',') AS courseNames
UNWIND courseNames AS courseName
WITH row, trim(courseName) AS courseNameTrim
MATCH (i:Institution {id: row.id})
MERGE (course:Course {name: courseNameTrim})
MERGE (i)-[:OFFERS_COURSE]->(course);

/* ---------------------------
   Done. You can run verification queries below.
   --------------------------- */
