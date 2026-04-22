import json
import re
from pathlib import Path
from collections import defaultdict

from app.services.classifier_service import predict_skill_category

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

CORE_MATCH_CATEGORIES = {
    "programming_languages","backend","frontend","databases","devops_cloud","ai_ml_core",
    "ai_ml_frameworks","llm_rag_agents","data_engineering","software_engineering",
    "cybersecurity_networking","embedded_iot_robotics","computer_vision_robotics",
    "mobile_desktop","mathematics_statistics","domain_experience",
}
MISSING_TECHNICAL_CATEGORIES = {
    "programming_languages","backend","frontend","databases","devops_cloud","ai_ml_frameworks",
    "llm_rag_agents","data_engineering","software_engineering","cybersecurity_networking",
    "embedded_iot_robotics","computer_vision_robotics","mobile_desktop","mathematics_statistics",
    "domain_experience",
}
HIDE_IN_MISSING_TECHNICAL = {
    "Communication","Collaboration","Teamwork","Learning Ability","Self-learning","Logical Thinking",
    "Analytical Thinking","Time Management","Attention to Detail","Ownership","Resilience",
    "Documentation","Documentation Writing","Testing","Unit Testing","Integration Testing",
    "Functional Testing","Problem Solving","Troubleshooting","Code Review","Agile Development",
    "Scrum","Refactoring","Clean Code",
}
PREFER_RELATED_BACKGROUND_IF_MISSING = {
    "Artificial Intelligence","Data Analysis","Software Engineering","Machine Learning",
    "Debugging","Communication","Teamwork","Learning Ability","Problem Solving",
}
PROMOTE_TO_CORE_MATCH = {"Debugging","Software Engineering"}
RELATED_BACKGROUND_CATEGORIES = {"soft_skills","mathematics_statistics"}
STRICT_SHORT_SKILLS = {"C","R","Go","AI","ML","LLM","NLP","SQL","JWT"}
TRANSFERABLE_SIGNAL_SKILLS = {
    "Python","Java","JavaScript","TypeScript","C++","FastAPI","REST API","Node.js","Express.js","React",
    "TensorFlow","PyTorch","Scikit-learn","OpenCV","YOLO","Machine Learning","Artificial Intelligence",
    "Data Analysis","Debugging","Software Engineering","Computer Vision","Embedded Systems","IoT",
    "Raspberry Pi","Arduino","Git","Linux","Database Design","MySQL","PostgreSQL","MongoDB",
    "Web Development","Frontend Development","Backend Development","Model Deployment",
    "AI Product Development","Intelligent Applications","Prompt Engineering","AI Agents","LangChain","RAG",
}
TRANSFERABLE_RULES = {
    "Prompt Engineering": {"Large Language Models","LLM","LangChain","RAG","AI Agents","Function Calling","Tool Calling"},
    "AI Agents": {"LangChain","RAG","Function Calling","Tool Calling","Backend Development","API Development"},
    "AI Product Development": {"Machine Learning","Artificial Intelligence","TensorFlow","PyTorch","Scikit-learn","Debugging","Software Engineering"},
    "Intelligent Applications": {"Machine Learning","Artificial Intelligence","TensorFlow","OpenCV","Computer Vision","Backend Development","Frontend Development"},
    "Large Model Deployment": {"Model Deployment","Large Language Models","LLM","LangChain","RAG","FastAPI","Docker","Cloud Deployment"},
    "Model Fine-tuning": {"Machine Learning","Deep Learning","TensorFlow","PyTorch","Fine-tuning"},
    "Fine-tuning": {"Machine Learning","Deep Learning","TensorFlow","PyTorch"},
    "Model Deployment": {"FastAPI","Docker","Cloud Deployment","Backend Development","TensorFlow","PyTorch"},
    "PyTorch": {"TensorFlow","Machine Learning","Deep Learning"},
    "Scikit-learn": {"Machine Learning","Data Analysis","Python"},
    "TensorFlow": {"Machine Learning","Deep Learning","Computer Vision","Python"},
    "Artificial Intelligence": {"Machine Learning","TensorFlow","PyTorch","OpenCV","Computer Vision"},
    "Data Analysis": {"Machine Learning","Pandas","NumPy","Matplotlib","Statistics","Data Visualization"},
}

def load_skills():
    with open(DATA_DIR / "skills.json","r",encoding="utf-8") as f:
        return json.load(f)

def load_learning_resources():
    with open(DATA_DIR / "learning_resources.json","r",encoding="utf-8") as f:
        return json.load(f)

def normalize_text(text:str)->str:
    text = text.replace("–","-").replace("—","-")
    return re.sub(r"\s+"," ",text.lower()).strip()

def flatten_skills(skills_data):
    all_skills=[]
    for _,skill_list in skills_data["skill_categories"].items():
        all_skills.extend(skill_list)
    return all_skills

def build_skill_to_category(skills_data):
    mapping={}
    for category, skill_list in skills_data["skill_categories"].items():
        for skill in skill_list:
            mapping[skill]=category
    return mapping

def build_pattern(alias:str, canonical_skill:str)->str:
    alias_norm = alias.lower().strip()
    escaped = re.escape(alias_norm)
    if canonical_skill in STRICT_SHORT_SKILLS or alias in STRICT_SHORT_SKILLS:
        return rf"(?<![a-z0-9+#]){escaped}(?![a-z0-9+#])"
    return rf"(?<![a-z0-9+#]){escaped}(?![a-z0-9+#])"

def post_filter_false_positives(found:set[str], text_norm:str)->set[str]:
    if "C++" in found and "C" in found:
        found.discard("C")
    if "tf-idf" in text_norm and "TensorFlow" in found:
        if not re.search(r"(?<![a-z0-9+#])tensorflow(?![a-z0-9+#])|(?<![a-z0-9+#])tensor flow(?![a-z0-9+#])", text_norm):
            found.discard("TensorFlow")
    if "R" in found:
        valid_r_patterns = [
            r"(?<![a-z0-9+#])r language(?![a-z0-9+#])",
            r"(?<![a-z0-9+#])using r(?![a-z0-9+#])",
            r"(?<![a-z0-9+#])written in r(?![a-z0-9+#])",
            r"(?<![a-z0-9+#])programming in r(?![a-z0-9+#])",
        ]
        if not any(re.search(p, text_norm) for p in valid_r_patterns):
            found.discard("R")
    if "Communication" in found:
        if re.search(r"(?<![a-z0-9+#])data communication(?![a-z0-9+#])", text_norm):
            if not re.search(r"communication skills|good communication|strong communication|communicate effectively|team communication", text_norm):
                found.discard("Communication")
    return found

def extract_skills(text:str, skills_data:dict)->list[str]:
    text_norm = normalize_text(text)
    aliases = skills_data.get("skill_aliases", {})
    found=set()
    for canonical_skill, alias_list in aliases.items():
        for alias in alias_list:
            if re.search(build_pattern(alias, canonical_skill), text_norm, flags=re.IGNORECASE):
                found.add(canonical_skill)
                break
    for skill in flatten_skills(skills_data):
        if re.search(build_pattern(skill, skill), text_norm, flags=re.IGNORECASE):
            found.add(skill)
    found = post_filter_false_positives(found, text_norm)
    return sorted(found)

def group_by_category(skills:list[str], skill_to_category:dict)->dict[str,list[str]]:
    grouped=defaultdict(list)
    for skill in skills:
        grouped[skill_to_category.get(skill,"other")].append(skill)
    return {k: sorted(v) for k,v in grouped.items()}

def build_learning_suggestions(skills:list[str], learning_resources:dict)->list[str]:
    suggestions=[]
    for skill in skills:
        if skill in learning_resources:
            for item in learning_resources[skill]:
                suggestions.append(f"{skill}: {item}")
        else:
            suggestions.append(f"{skill}: Learn the fundamentals and build one small practice project.")
    return suggestions

def compute_transferable_background(resume_skills:set[str], direct_missing_skills:list[str]):
    transferable_matches=[]
    transferable_evidence={}
    resume_transferable_pool = set(resume_skills) & TRANSFERABLE_SIGNAL_SKILLS
    for target_skill in direct_missing_skills:
        evidence_found = sorted(resume_transferable_pool & TRANSFERABLE_RULES.get(target_skill, set()))
        if evidence_found:
            transferable_matches.append(target_skill)
            transferable_evidence[target_skill]=evidence_found
    score = 0.0 if len(direct_missing_skills)==0 else round(len(transferable_matches)/len(direct_missing_skills)*100,2)
    return sorted(transferable_matches), transferable_evidence, score

def extract_resume_candidate_sentences(resume_text:str)->list[str]:
    raw_lines=[line.strip("• ").strip() for line in resume_text.splitlines()]
    candidate_lines=[]
    for line in raw_lines:
        if not line or len(line.split())<4:
            continue
        if ":" in line and len(line.split())<=6:
            continue
        candidate_lines.append(line)
    unique_lines=[]; seen=set()
    for line in candidate_lines:
        key=line.lower()
        if key not in seen:
            seen.add(key); unique_lines.append(line)
    return unique_lines

def classify_resume_background(resume_text:str):
    sentences = extract_resume_candidate_sentences(resume_text)
    distribution = {"backend":0,"frontend":0,"ai_ml":0,"tools":0}
    classified=[]
    for sentence in sentences:
        try:
            result = predict_skill_category(sentence)
            label = result["label"]
            confidence = float(result["confidence"])
            if label in distribution:
                distribution[label]+=1
            classified.append({"text": sentence, "label": label, "confidence": round(confidence,4)})
        except Exception:
            continue
    return distribution, classified

def analyze_match(resume_text:str, jd_text:str):
    skills_data = load_skills()
    learning_resources = load_learning_resources()
    skill_to_category = build_skill_to_category(skills_data)

    resume_skills = extract_skills(resume_text, skills_data)
    jd_skills = extract_skills(jd_text, skills_data)

    matched_all = sorted(set(resume_skills) & set(jd_skills))
    missing_all = sorted(set(jd_skills) - set(resume_skills))

    matched_core_skills=[]; missing_technical_skills=[]; related_background=[]; hidden_missing_skills=[]
    for skill in matched_all:
        category = skill_to_category.get(skill, "other")
        if skill in PROMOTE_TO_CORE_MATCH:
            matched_core_skills.append(skill)
        elif skill in HIDE_IN_MISSING_TECHNICAL or category in RELATED_BACKGROUND_CATEGORIES:
            related_background.append(skill)
        elif category in CORE_MATCH_CATEGORIES:
            matched_core_skills.append(skill)
        else:
            related_background.append(skill)
    for skill in missing_all:
        category = skill_to_category.get(skill, "other")
        if skill in HIDE_IN_MISSING_TECHNICAL:
            hidden_missing_skills.append(skill)
        elif skill in PREFER_RELATED_BACKGROUND_IF_MISSING:
            related_background.append(skill)
        elif category in MISSING_TECHNICAL_CATEGORIES:
            missing_technical_skills.append(skill)
        else:
            hidden_missing_skills.append(skill)

    matched_core_skills=sorted(set(matched_core_skills))
    missing_technical_skills=sorted(set(missing_technical_skills))
    related_background=sorted(set(related_background))
    hidden_missing_skills=sorted(set(hidden_missing_skills))

    scoring_jd_skills = sorted(set(matched_core_skills) | set(missing_technical_skills))
    direct_match_score = 0.0 if len(scoring_jd_skills)==0 else round(len(matched_core_skills)/len(scoring_jd_skills)*100,2)

    transferable_matches, transferable_evidence, transferable_background_score = compute_transferable_background(set(resume_skills), missing_technical_skills)
    learning_suggestions = build_learning_suggestions(missing_technical_skills, learning_resources)
    resume_experience_distribution, classified_resume_sentences = classify_resume_background(resume_text)

    return {
        "matched_core_skills": matched_core_skills,
        "missing_technical_skills": missing_technical_skills,
        "related_background": related_background,
        "transferable_matches": transferable_matches,
        "transferable_evidence": transferable_evidence,
        "learning_suggestions": learning_suggestions,
        "direct_match_score": direct_match_score,
        "transferable_background_score": transferable_background_score,
        "resume_experience_distribution": resume_experience_distribution,
        "classified_resume_sentences": classified_resume_sentences,
        "resume_extracted_skills": resume_skills,
        "jd_extracted_skills": jd_skills,
        "hidden_missing_skills": hidden_missing_skills,
        "grouped_missing_technical_skills": group_by_category(missing_technical_skills, skill_to_category),
    }
