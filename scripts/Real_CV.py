import os
import random
import tempfile
import time
from faker import Faker
from jinja2 import Template
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import pandas as pd

# 本腳本改用 JSON Resume 標準和主題系統來生成履歷，並同時產生對應的 JSON 格式檔案。

def generate_random_template():
    """動態生成隨機 HTML 模板"""
    # 隨機化樣式
    font_family = random.choice(['Arial', 'Times New Roman', 'Helvetica', 'Georgia'])
    font_size = random.choice(['12px', '14px', '16px'])
    color = random.choice(['#000', '#333', '#555', '#007BFF'])
    margin = random.choice(['1cm', '1.5cm', '2cm'])
    heading_align = random.choice(['left', 'center', 'right'])
    header_position = random.choice(['top', 'bottom'])  # 決定聯絡資訊放哪

    background_color = random.choice(["#ffffff", "#f5f5f5", "#e6f7ff", "#fff8e1"])
    use_two_columns = random.choice([True, False])
    show_profile_image = random.choice([True, False])

    heading_variants = {
        "summary": random.choice(["Professional Summary", "Profile", "About Me"]),
        "skills": random.choice(["Skills", "Key Competencies", "Technical Skills"]),
        "experience": random.choice(["Experience", "Work History", "Employment"]),
        "certifications": random.choice(["Certifications", "Licenses & Certifications"]),
        "languages": random.choice(["Languages", "Spoken Languages", "Language Proficiency"])
    }
    separator = random.choice(["<hr>", "<br><br>", "<div style='margin:1em 0;border-top:1px solid #ccc'></div>"])

    summary_text = ("Aircraft maintenance engineer with "
        f"{{{{ years_experience }}}} years of experience, skilled in {{{{ skill_summary }}}}."
        if random.random() < 0.5 else
        "Aircraft maintenance engineer with extensive hands-on expertise performing scheduled and unscheduled inspections, resolving technical discrepancies, and ensuring regulatory compliance across multiple aircraft models, with proficiency in industry tools and protocols like AMOS, CAMP, and MEL application.")

    header_block = """
        <h1>{{ name }}</h1>
        <p><strong>Email:</strong> {{ email }}</p>
        <p><strong>Phone:</strong> {{ phone }}</p>
    """

    # 隨機化段落結構
    sections = [
        f'<h2>{heading_variants["summary"]}</h2><p>{summary_text}</p>',
        f'<h2>{heading_variants["skills"]}</h2><ul>{{% for skill in skills %}}<li>{{{{ skill }}}}</li>{{% endfor %}}</ul>',
        f'<h2>{heading_variants["experience"]}</h2><ul><li>Worked on maintenance of {{{{ aircraft_type }}}} aircraft at {{{{ company }}}}, ensuring airworthiness and regulatory compliance.</li></ul>',
        f'<h2>{heading_variants["certifications"]}</h2><ul><li>{{{{ certification }}}}</li></ul>',
        f'<h2>{heading_variants["languages"]}</h2><ul>{{% for language in languages %}}<li>{{{{ language }}}}</li>{{% endfor %}}</ul>',
        f'<h2>Education</h2><ul>{{% for edu in education %}}<li>{{{{ edu.degree }}}}, {{{{ edu.institution }}}} ({{{{ edu.year }}}})</li>{{% endfor %}}</ul>',
        f'<h2>Work Experience</h2><ul>{{% for job in work_experience %}}<li>{{{{ job.job_title }}}} at {{{{ job.company }}}} ({{{{ job.years }}}}) - {{{{ job.description }}}}</li>{{% endfor %}}</ul>',
    ]
    random.shuffle(sections)  # 隨機排列段落順序

    content = separator.join(sections)

    if use_two_columns:
        profile_image_html = '<img src="{{ image_url }}" width="100" style="border-radius: 50%;">' if show_profile_image else ''
        template_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: {font_family}; font-size: {font_size}; line-height: 1.5; margin: {margin}; color: {color}; background-color: {background_color}; }}
                h1, h2 {{ text-align: {heading_align}; }}
                ul {{ margin: 0.5em 0; padding-left: 1.5em; }}
                .container {{ display: flex; gap: 2em; }}
                .left, .right {{ flex: 1; }}
                .left {{ max-width: 200px; }}
                img {{ display: block; margin-bottom: 1em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="left">
                    {profile_image_html}
                    {header_block}
                </div>
                <div class="right">
                    {content}
                </div>
            </div>
        </body>
        </html>
        """
    else:
        if header_position == 'top':
            profile_image_html = '<img src="{{ image_url }}" width="100" style="border-radius: 50%;">' if show_profile_image else ''
            template_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: {font_family}; font-size: {font_size}; line-height: 1.5; margin: {margin}; color: {color}; background-color: {background_color}; }}
                    h1, h2 {{ text-align: {heading_align}; }}
                    ul {{ margin: 0.5em 0; padding-left: 1.5em; }}
                    img {{ display: block; margin-bottom: 1em; max-width: 100px; border-radius: 50%; }}
                </style>
            </head>
            <body>
                {profile_image_html}
                {header_block}
                {content}
            </body>
            </html>
            """
        else:
            profile_image_html = '<img src="{{ image_url }}" width="100" style="border-radius: 50%;">' if show_profile_image else ''
            template_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: {font_family}; font-size: {font_size}; line-height: 1.5; margin: {margin}; color: {color}; background-color: {background_color}; }}
                    h1, h2 {{ text-align: {heading_align}; }}
                    ul {{ margin: 0.5em 0; padding-left: 1.5em; }}
                    img {{ display: block; margin-bottom: 1em; max-width: 100px; border-radius: 50%; }}
                </style>
            </head>
            <body>
                {content}
                {profile_image_html}
                {header_block}
            </body>
            </html>
            """
    return Template(template_content)

def extract_skills_from_csv(input_csv):
    """
    從 CSV 文件中提取所有技能短語
    """
    df = pd.read_csv(input_csv)
    skills_col = None
    for col in df.columns:
        col_cleaned = col.strip().lower()
        if col_cleaned == 'skills required':
            skills_col = col
            break

    if not skills_col:
        print("[錯誤] CSV 文件缺少 'Skills Required' 列")
        return []

    # 提取所有技能短語，去重並返回列表
    all_skills = set()
    for skills_raw in df[skills_col].dropna():
        skills = [skill.strip() for skill in skills_raw.split(';') if skill.strip()]
        all_skills.update(skills)
    return list(all_skills)

def generate_resumes():
    fake = Faker()
    output_dir = r'/Users/stella/Desktop/Resume_Screening_Solution/data/resumes'
    os.makedirs(output_dir, exist_ok=True)

    # 清空舊的 PDF 文件
    for file in os.listdir(output_dir):
        if file.endswith('.pdf'):
            try:
                os.remove(os.path.join(output_dir, file))
            except:
                pass

    # 從 CSV 中提取技能
    input_csv = "/Users/stella/Desktop/Resume_Screening_Solution/scripts/job_data.csv"
    job_skills = extract_skills_from_csv(input_csv)
    if not job_skills:
        print("[警告] 無法從 CSV 提取技能，將完全隨機生成技能")

    total = 100  # 生成的履歷數量
    batch_size = 20
    success = 0

    with tempfile.TemporaryDirectory() as font_cache:
        font_config = FontConfiguration()
        
        for i in range(total):
            try:
                # 動態生成模板
                template = generate_random_template()

                # 新增語言清單與熟練度
                common_languages = ["English", "Cantonese", "Mandarin", "Japanese", "Korean", "French", "German"]
                proficiency_levels = ["Fluent", "Proficient", "Intermediate", "Basic"]
                # 確保英文必定出現且有熟練度標籤，放在語言列表最前
                language_list = [f"English ({random.choice(proficiency_levels)})"] + [
                    f"{lang} ({random.choice(proficiency_levels)})"
                    for lang in random.sample(common_languages, random.randint(1, 3))
                    if lang != "English"
                ]

                # 動態生成技能列表
                random_skills = [fake.job() for _ in range(random.randint(3, 6))]
                selected_job_skills = random.sample(job_skills, random.randint(1, len(job_skills) // 2)) if job_skills else []
                # 40% 機會使用 CSV 中的技能
                if random.random() < 0.4:
                    skills = selected_job_skills + random.sample(random_skills, max(0, 6 - len(selected_job_skills)))
                else:
                    skills = random_skills

                # 動態生成數據
                data = {
                    "name": fake.name(),
                    "email": fake.email(),
                    "phone": f"+852 {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
                    "years_experience": random.randint(1, 20),
                    "skills": skills,
                    "company": fake.company(),
                    "aircraft_type": random.choice(["Boeing 777", "Airbus A350", "Boeing 787", "A330neo", "A380"]),
                    "certification": random.choice(["FAA A&P License", "EASA Part-66 License", "HKCAD Cat B1"]),
                    "languages": language_list,
                    "skill_summary": ", ".join(skills),
                    "image_url": f"https://i.pravatar.cc/150?img={random.randint(1,70)}",
                    "education": [{
                        "degree": random.choice(["BEng", "BSc", "Higher Diploma", "Associate Degree"]),
                        "institution": fake.company() + " University",
                        "year": random.randint(2010, 2023)
                    }],
                    "work_experience": [{
                        "job_title": fake.job(),
                        "company": fake.company(),
                        "years": f"{random.randint(2015, 2020)} - {random.randint(2021, 2024)}",
                        "description": "Worked on aircraft maintenance and safety compliance."
                    }],
                }

                # 渲染模板
                rendered = template.render(**data)

                # 保存為 PDF
                out_file = f"{data['name'].replace(' ', '_')}_{i}.pdf"
                out_path = os.path.join(output_dir, out_file)
                
                HTML(string=rendered).write_pdf(
                    out_path,
                    stylesheets=[CSS(string='''
                        @page { size: A4; margin: 1cm; }
                        body { font-family: Arial, sans-serif; line-height: 1.5; word-break: break-word; }
                    ''')],
                    font_config=font_config,
                    optimize_size=('fonts', 'images')
                )

                success += 1

                if (i + 1) % batch_size == 0:
                    print(f"Generated {i + 1}/{total} CV")
                    time.sleep(0.5)

            except Exception as e:
                print(f"Error generating CV {i}: {str(e)}")
                continue

    print(f"Generated {success} CVs, Failed {total - success}")

if __name__ == "__main__":
    generate_resumes()

