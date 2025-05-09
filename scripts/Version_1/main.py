import os
import json
from parse_resumes import parse_all_resumes
from extract_features import extract_features
from rank_candidates import rank_candidates
from generated_resumes import generate_resumes
import csv

def main():
    base_dir = "/Users/stella/Desktop/Resume_Screening_Solution"
    resumes_path = os.path.join(base_dir, "data", "resumes")
    job_desc_path = os.path.join(base_dir, "data", "job_descriptions", "Aircraft_Maintenance_Engineer.txt")
    parsed_resumes_path = os.path.join(base_dir, "data", "parsed_resumes.json")
    features_path = os.path.join(base_dir, "data", "features.json")
    ranked_candidates_path = os.path.join(base_dir, "data", "ranked_candidates.json")

    print("Generating CV...")
    generate_resumes()
    print("CV generation completed, CVs saved to data/resumes/")

    print("Analysing CV...")
    parsed_resumes = parse_all_resumes(resumes_path)
    with open(parsed_resumes_path, 'w', encoding='utf-8') as f:
        json.dump(parsed_resumes, f, ensure_ascii=False, indent=2)
    print("CV analysis completed, results saved to parsed_resumes.json")

    print("Extracting features from the CV...")
    extract_features(parsed_resumes_path, job_desc_path, features_path)
    print("Feature extraction completed, results saved to features.json")

    print("Ranking the candidates...")
    rank_candidates(features_path, ranked_candidates_path)
    print("Output the results to ranked_candidates.csv ...")
    csv_output_path = os.path.join(base_dir, "data", "ranked_candidates.csv")
    with open(ranked_candidates_path, 'r', encoding='utf-8') as f:
        ranked_candidates = json.load(f)

    with open(parsed_resumes_path, 'r', encoding='utf-8') as f:
        parsed_resumes = json.load(f)

    work_experience_map = {
        resume["filename"]: {
            "work_experience": f"Worked on maintenance of {resume.get('aircraft_type', '')} aircraft, ensuring airworthiness and regulatory compliance.",
            "skills": ", ".join(resume.get("skills", [])),
            "certification": resume.get("certification", ""),
            "years_experience": resume.get("years_experience", 0)
        }
        for resume in parsed_resumes
    }

    with open(csv_output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'rank', 'name', 'email', 'phone', 'skills_match_score', 'experience_score',
            'years_experience', 'work_experience', 'skills', 'certification'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for idx, candidate in enumerate(ranked_candidates, start=1):
            filename = candidate.get('filename', '')
            work_experience_data = work_experience_map.get(filename, {})
            work_experience = work_experience_data.get("work_experience", "")
            skills = work_experience_data.get("skills", "")
            certification = work_experience_data.get("certification", "")
            years_experience = work_experience_data.get("years_experience", 0)

            if candidate.get('experience_score', 0) < 1 or candidate.get('skills_match_score', 0) == 0:
                continue

            row = {
                'rank': idx,
                'name': candidate.get('name', ''),
                'email': candidate.get('email', ''),
                'phone': candidate.get('phone', ''),
                'skills_match_score': candidate.get('skills_match_score', 0),
                'experience_score': candidate.get('experience_score', 0),
                'years_experience': years_experience,
                'work_experience': work_experience,
                'skills': skills,
                'certification': certification
            }
            writer.writerow(row)

    print("The results are saved to data/ volume/ranked_candidates.csv")

if __name__ == "__main__":
    main()