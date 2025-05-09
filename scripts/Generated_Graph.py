import matplotlib.pyplot as plt
import json

def generate_bar_chart(input_file: str, resume_id: str):
    """
    為指定的簡歷生成棒形圖，顯示與所有職缺的相似度
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 過濾出指定簡歷的結果
    filtered_data = [d for d in data if d["resume_id"] == resume_id]

    if not filtered_data:
        print(f"未找到簡歷 ID 為 {resume_id} 的結果")
        return

    # 提取職缺名稱和相似度
    job_titles = [d["job_title"] for d in filtered_data]
    similarities = [d["similarity"] for d in filtered_data]

    # 生成棒形圖
    plt.figure(figsize=(10, 6))
    plt.barh(job_titles, similarities, color='skyblue')
    plt.xlabel('Jaccard Similarity')
    plt.ylabel('Job Titles')
    plt.title(f'Similarity Scores for Resume: {resume_id}')
    plt.tight_layout()
    plt.show()

# Example usage
generate_bar_chart(
    input_file="/Users/stella/Desktop/Resume_Screening_Solution/ranked_results.json",
    resume_id="Tamara_Kim_89"
)