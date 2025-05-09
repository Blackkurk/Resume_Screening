import os
import random
import tempfile
import time
import re
from faker import Faker 
from jinja2 import Environment, FileSystemLoader 
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def generate_resumes():
    fake = Faker()
    template_env = Environment(loader=FileSystemLoader('.'))
    template = template_env.get_template('resume_template.html')
    output_dir = r'/Users/stella/Desktop/Resume_Screening_Solution/data/resumes'
    
    os.makedirs(output_dir, exist_ok=True)

    skills_pool = [
        "Airframe inspections", "Powerplant maintenance", "Hydraulic systems",
        "Fuel systems", "Avionics troubleshooting", "Safety compliance",
        "Documentation & reporting"
    ]

    job_desc_path = r'data/job_descriptions/Aircraft_Maintenance_Engineer.txt'
    with open(job_desc_path, 'r', encoding='utf-8') as f:
        job_desc_text = f.read()

    skills_from_jd = re.findall(r"- (.*?)\n", re.search(r"Skills Required:(.*?)Experience Required:", job_desc_text, re.DOTALL).group(1))
    print("Required Skill：", skills_from_jd)

    skills_pool = list(set(skills_pool + skills_from_jd))

    aircraft_types = ["Boeing 777", "Airbus A350", "Boeing 787", "A330neo", "A380"]
    certifications = ["FAA A&P License", "EASA Part-66 License", "HKCAD Cat B1"]

    for file in os.listdir(output_dir):
        if file.endswith('.pdf'):
            try:
                os.remove(os.path.join(output_dir, file))
            except:
                pass

    total = 1000
    batch_size = 200
    success = 0

    with tempfile.TemporaryDirectory() as font_cache:
        font_config = FontConfiguration()
        
        for i in range(total):
            try:
                data = {
                    "name": fake.name(),
                    "email": fake.email(),
                    "phone": fake.phone_number(),
                    "years_experience": random.randint(5, 20),
                    "skills": random.sample(skills_pool, 4),
                    "company": fake.company(),
                    "aircraft_type": random.choice(aircraft_types),
                    "certification": random.choice(certifications)
                }
                data["skill_summary"] = ", ".join(data["skills"])

                rendered = template.render(**data)

                out_file = f"{data['name'].replace(' ', '_')}_{i}.pdf"
                out_path = os.path.join(output_dir, out_file)
                
                HTML(string=rendered).write_pdf(
                    out_path,
                    stylesheets=[CSS(string='''
                        @page { size: A4; margin: 1cm; }
                        body { 
                            font-family: Arial, sans-serif;
                            line-height: 1.5;
                            word-break: break-word;
                        }
                        ul { margin: 0.5em 0; padding-left: 1.5em; }
                    ''')],
                    font_config=font_config,
                    optimize_size=('fonts', 'images')
                )
                success += 1

                if (i + 1) % batch_size == 0:
                    print(f"Generated {i + 1}/{total} CV")
                    time.sleep(0.5)

            except Exception as e:
                print(f" {i} CV with mistake: {str(e)}")
                continue

    print(f"Generated {success} CV，Fail {total - success}")

if __name__ == "__main__":
    generate_resumes()