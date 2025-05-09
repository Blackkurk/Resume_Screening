import os
import json
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from typing import List
from PyPDF2 import PdfReader
import inflect

p = inflect.engine()

input_csv = "/Users/stella/Desktop/Resume_Screening_Solution/scripts/job_data.csv"
resume_folder = "/Users/stella/Desktop/Resume_Screening_Solution/data/resumes"

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

def custom_suffix_cleaning(lemma: str) -> str:
    if lemma.endswith("ed") and len(lemma) > 4:
        return lemma[:-2]
    if lemma.endswith("ing") and len(lemma) > 5:
        return lemma[:-3]
    return lemma

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def preprocess_text(text: str) -> List[str]:
    doc = nlp(text)
    lemmas = []

    # Words to keep even if they are stop words
    preserve_stop_words = {"and", "to", "of"}

    for token in doc:
        if token.is_alpha:
            lemma = custom_suffix_cleaning(token.lemma_.lower())

            # Remove stop words except competency keywords
            if (token.is_stop and lemma not in preserve_stop_words) or lemma in STOP_WORDS:
                continue

            # Final check: ignore 1-2 letter fragments
            if len(lemma) > 2 or lemma in preserve_stop_words:
                lemmas.append(lemma)

    return lemmas

def generate_ngrams(words: List[str], n: int) -> List[str]:
    return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]

def process_resumes(resume_dir: str):
    results = []
    for filename in os.listdir(resume_dir):
        if filename.endswith(".pdf"):
            path = os.path.join(resume_dir, filename)
            raw_text = extract_text_from_pdf(path)
            lemmas = preprocess_text(raw_text)
            bigrams = generate_ngrams(lemmas, 2)
            trigrams = generate_ngrams(lemmas, 3)
            tokenized_phrases = lemmas + bigrams + trigrams

            result = {
                "id": filename.split(".")[0],
                "lemmas": lemmas,
                "tokenized_phrases": tokenized_phrases
            }
            results.append(result)
    return results

if __name__ == "__main__":
    processed = process_resumes(resume_folder)
    output_path = "processed_resumes.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)
    print(f"Processed {len(processed)} resumes and saved to {output_path}")