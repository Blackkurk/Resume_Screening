import json

def rank_candidates(features_path, output_path):
    """
    According to the skills_match_score and experience_score, rank the candidates.
    The higher the score, the better the candidate.
    """
    with open(features_path, 'r', encoding='utf-8') as f:
        features = json.load(f)

    ranked_candidates = sorted(
        features,
        key=lambda x: (x.get("skills_match_score", 0), x.get("experience_score", 0)),
        reverse=True
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(ranked_candidates, f, ensure_ascii=False, indent=2)

    print(f"Complete the task {output_path}")

if __name__ == "__main__":
    features_path = "/Users/stella/Desktop/Resume_Screening_Solution/data/features.json"
    output_path = "/Users/stella/Desktop/Resume_Screening_Solution/data/ranked_candidates.json"

    rank_candidates(features_path, output_path)