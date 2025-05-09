import json
from typing import List, Dict

def match_skills_with_tokenization(job_file: str, resume_file: str, output_file: str):
    """
    根据 Tokenization 功能，将简历技能与职位技能进行匹配，并更新 resume_skills 字段
    """
    # 加载职位数据
    with open(job_file, 'r', encoding='utf-8') as f:
        job_data = json.load(f)

    # 加载简历数据
    with open(resume_file, 'r', encoding='utf-8') as f:
        resume_data = json.load(f)

    results = []

    # 遍历每个职位
    for job in job_data:
        job_id = job['id']
        job_title = job['title']
        required_skills = set(skill.lower() for skill in job['required_skills'])  # 忽略大小写

        # 遍历每份简历
        for resume in resume_data:
            resume_id = resume['id']
            tokenized_phrases = set(phrase.lower() for phrase in resume['tokenized_phrases'])  # 忽略大小写

            # 匹配技能
            matched_skills = required_skills & tokenized_phrases  # 交集
            unmatched_skills = required_skills - matched_skills  # 差集

            # 保存结果
            results.append({
                "job_id": job_id,
                "job_title": job_title,
                "resume_id": resume_id,
                "matched_skills": list(matched_skills),
                "unmatched_skills": list(unmatched_skills)
            })

    # 保存匹配结果到文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"匹配结果已保存到 {output_file}")

if __name__ == "__main__":
    # 文件路径
    job_file = "/Users/stella/Desktop/Resume_Screening_Solution/job_parsed.json"
    resume_file = "/Users/stella/Desktop/Resume_Screening_Solution/processed_resumes.json"
    output_file = "/Users/stella/Desktop/Resume_Screening_Solution/matching_results.json"

    # 执行技能匹配
    match_skills_with_tokenization(job_file, resume_file, output_file)