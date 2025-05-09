import json
from typing import List, Dict, Set

def calculate_jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """
    計算 Jaccard 相似度
    """
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0

def calculate_similarity_and_rank(input_file: str, output_file: str):
    """
    計算 Jaccard 相似度，按職缺排序並輸出到 JSON 文件
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    ranked_results = []

    for result in data:
        job_id = result["job_id"]
        job_title = result["job_title"]
        matched_skills = set(result["matched_skills"])
        unmatched_skills = set(result["unmatched_skills"])
        required_skills = matched_skills | unmatched_skills

        # 計算 Jaccard 相似度
        similarity = calculate_jaccard_similarity(matched_skills, required_skills)

        ranked_results.append({
            "job_id": job_id,
            "job_title": job_title,
            "resume_id": result["resume_id"],
            "similarity": round(similarity, 2),
            "matched_skills": list(matched_skills),
            "unmatched_skills": list(unmatched_skills)
        })

    # 按相似度排序
    ranked_results.sort(key=lambda x: x["similarity"], reverse=True)

    # 保存結果到 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(ranked_results, f, ensure_ascii=False, indent=2)

    print(f"相似度計算完成，結果已保存到 {output_file}")

# Example usage
calculate_similarity_and_rank(
    input_file="/Users/stella/Desktop/Resume_Screening_Solution/matching_results.json",
    output_file="/Users/stella/Desktop/Resume_Screening_Solution/ranked_results.json"
)