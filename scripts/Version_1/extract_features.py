import os
import json
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_job_description(job_desc_path):
    """Read job requirement and work experiments from the job description file."""
    with open(job_desc_path, 'r', encoding='utf-8') as f:
        job_desc_text = f.read()

    skills_match = re.findall(r"- (.*?)\n", re.search(r"Skills Required:(.*?)Experience Required:", job_desc_text, re.DOTALL).group(1))
    experience_match = re.findall(r"- (.*?)\n", re.search(r"Experience Required:(.*)", job_desc_text, re.DOTALL).group(1))

    return {
        "skills": skills_match,
        "experience": experience_match
    }

def calculate_feature_vector(resume, job_desc):
    """Calculate the feature vector, including skill and experience score"""
    features = {
        "filename": resume["filename"],
        "name": resume.get("name", ""),
        "email": resume.get("email", ""),
        "phone": resume.get("phone", ""),
        "skills_match_score": 0,
        "experience_score": 0
    }

    resume_skills = set(resume.get("skills", []))
    job_skills = set(job_desc["skills"])
    matched_skills = resume_skills.intersection(job_skills)
    features["skills_match_score"] = len(matched_skills) / len(job_skills) if job_skills else 0

    resume_experience = int(resume.get("years_experience", 0))
    required_experience = max([int(re.search(r"(\d+)", exp).group(1)) for exp in job_desc["experience"] if re.search(r"(\d+)", exp)], default=0)
    if required_experience > 0:
        features["experience_score"] = resume_experience / required_experience
    else:
        features["experience_score"] = 0

    return features

def extract_features(resumes_path, job_desc_path, output_path):
    """Extract features from resumes and job description, and save to JSON file."""
    job_desc = load_job_description(job_desc_path)

    with open(resumes_path, 'r', encoding='utf-8') as f:
        resumes = json.load(f)

    feature_vectors = []
    for resume in resumes:
        feature_vector = calculate_feature_vector(resume, job_desc)
        feature_vectors.append(feature_vector)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(feature_vectors, f, ensure_ascii=False, indent=2)

    print(f"Extact successfully {len(feature_vectors)} CV Stored at {output_path}")

if __name__ == "__main__":
    resumes_path = os.path.join("data", "parsed_resumes.json")
    job_desc_path = os.path.join("data", "job_descriptions", "Aircraft_Maintenance_Engineer.txt")
    output_path = os.path.join("data", "features.json")

    extract_features(resumes_path, job_desc_path, output_path)