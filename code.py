import re
import matplotlib.pyplot as plt
import numpy as np

def calculate_score(keyword_input, title, description):

    keywords = [k.strip().lower() for k in keyword_input.split(",") if k.strip()]
    title_l = title.lower()
    desc_l = description.lower()

    total_keywords = len(keywords)

    title_matches = sum(1 for k in keywords if k in title_l)
    title_score = int((title_matches / total_keywords) * 30) if total_keywords else 0

    desc_matches = sum(1 for k in keywords if k in desc_l)
    desc_score = int((desc_matches / total_keywords) * 30) if total_keywords else 0

    hook_score = 10 if "?" in title else 0
    curiosity_score = 10 if "how" in title_l else 0

    final_score = title_score + desc_score + hook_score + curiosity_score

    return {
        "Title Score": title_score,
        "Description Score": desc_score,
        "Hook Score": hook_score,
        "Curiosity Score": curiosity_score,
        "Final Score": final_score
    }

def parse_ai_output(text):

    titles = re.findall(r"Title \d: (.*)", text)
    description_match = re.search(r"Description:\n([\s\S]*?)\n\nHashtags:", text)
    hashtags_match = re.search(r"Hashtags:\n([\s\S]*)", text)

    description = description_match.group(1).strip() if description_match else ""
    hashtags = hashtags_match.group(1).strip() if hashtags_match else ""

    return titles, description, hashtags