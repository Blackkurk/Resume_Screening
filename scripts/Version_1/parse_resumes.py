import os
import re
import json
import pdfplumber  

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using pdfplumber."""
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def parse_resume_text(text):
    data = {
        "name": "",
        "email": "",
        "phone": "",
        "years_experience": "",
        "skills": [],
        "aircraft_type": "",
        "certification": ""
    }

    skills_section = re.search(r"Skills\s*(.*?)(?:\n(?:Experience|Certifications|$))", text, re.DOTALL)
    if skills_section:
        skills_raw = skills_section.group(1)
        skills_lines = skills_raw.splitlines()
        skills = []
        for line in skills_lines:
            match = re.search(r"[a-zA-Z].*", line)
            if match:
                skills.append(match.group(0).strip())
        data["skills"] = skills

    cert_section = re.search(r"Certifications\s*(.*?)(?:\n\n|\Z)", text, re.DOTALL)
    if cert_section:
        cert_raw = cert_section.group(1)
        cert_lines = cert_raw.splitlines()
        certifications = []
        for line in cert_lines:
            match = re.search(r"[a-zA-Z].*", line)
            if match:
                certifications.append(match.group(0).strip())
        data["certification"] = ", ".join(certifications)

    name_match = re.search(r"^(.*?)\n", text)
    email_match = re.search(r"Email:\s*(.*)", text)
    phone_match = re.search(r"Phone:\s*(.*)", text)
    exp_match = re.search(r"(\d+)\s+years of experience", text)
    aircraft_match = re.search(r"maintenance of (.*?) aircraft", text)

    if name_match:
        data["name"] = name_match.group(1).strip()
    if email_match:
        data["email"] = email_match.group(1).strip()
    if phone_match:
        data["phone"] = phone_match.group(1).strip()
    if exp_match:
        data["years_experience"] = int(exp_match.group(1))
    if aircraft_match:
        data["aircraft_type"] = aircraft_match.group(1).strip()

    return data

def parse_all_resumes(resume_dir):
    results = []
    for file in os.listdir(resume_dir):
        if file.endswith('.pdf'):
            file_path = os.path.join(resume_dir, file)
            try:
                text = extract_text_from_pdf(file_path) 
                parsed = parse_resume_text(text)
                parsed["filename"] = file
                results.append(parsed)
            except Exception as e:
                print(f"Can't anaylse {file}: {e}")
    return results

if __name__ == "__main__":
    resume_folder = os.path.join("data", "resumes")
    parsed_data = parse_all_resumes(resume_folder)

    output_path = os.path.join("data", "parsed_resumes.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=2)

    print(f"Complete the analysis, {len(parsed_data)} CV，Results are stored to {output_path}")