import re
import matplotlib.pyplot as plt
import numpy as np
from main import generate_ai_content

# -------------------------------
# SCORING FUNCTION
# -------------------------------
def calculate_score(keyword_input, title, description):

    keywords = [k.strip().lower() for k in keyword_input.split(",") if k.strip()]
    title_l = title.lower()
    desc_l = description.lower()

    total_keywords = len(keywords)

    title_matches = sum(1 for k in keywords if k in title_l)
    title_ratio = title_matches / total_keywords if total_keywords else 0
    title_score = 30 if title_ratio >= 0.7 else int(title_ratio * 30)

    desc_matches = sum(1 for k in keywords if k in desc_l)
    desc_ratio = desc_matches / total_keywords if total_keywords else 0
    desc_score = 30 if desc_ratio >= 0.9 else int(desc_ratio * 30)

    power_words = ["what if", "secret", "shocking", "amazing", "unexpected", "truth"]
    hook_score = sum(5 for word in power_words if word in title_l)
    hook_score = min(hook_score, 20)

    curiosity_score = 0
    if "?" in title:
        curiosity_score += 10
    if re.search(r"\bvs\b|\bmeet\b|\bstory\b|\bjourney\b", title_l):
        curiosity_score += 10
    curiosity_score = min(curiosity_score, 20)

    final_score = title_score + desc_score + hook_score + curiosity_score

    return {
        "Title Score": title_score,
        "Description Score": desc_score,
        "Hook Score": hook_score,
        "Curiosity Score": curiosity_score,
        "Final Score": final_score
    }

# -------------------------------
# CHART FUNCTION (WITH LABELS)
# -------------------------------
def show_charts(result):

    labels = ["Title", "Description", "Hook", "Curiosity"]
    max_scores = [30, 30, 20, 20]
    obtained_scores = [
        result["Title Score"],
        result["Description Score"],
        result["Hook Score"],
        result["Curiosity Score"]
    ]

    remaining_scores = [m - o for m, o in zip(max_scores, obtained_scores)]

    base_colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
    light_colors = ["lightblue", "moccasin", "lightgreen", "lightcoral"]

    # BAR CHART
    plt.figure()
    x = np.arange(len(labels))

    plt.bar(x, obtained_scores, color=base_colors)
    plt.bar(x, remaining_scores, bottom=obtained_scores, color=light_colors)

    plt.xticks(x, labels)
    plt.title("Score vs Max Score")

    for i in range(len(labels)):
        plt.text(i, max_scores[i] + 1,
                 f"{obtained_scores[i]}/{max_scores[i]}",
                 ha='center', fontweight='bold')

    # LINE CHART
    plt.figure()

    plt.plot(x, max_scores, marker='o', linestyle='--', label='Max Score')
    plt.plot(x, obtained_scores, marker='o', linewidth=3, label='Achieved Score')

    plt.xticks(x, labels)
    plt.title("Performance Comparison")

    for i in range(len(labels)):
        plt.text(i, obtained_scores[i] + 1,
                 f"{obtained_scores[i]}/{max_scores[i]}",
                 ha='center', fontweight='bold')

    plt.legend()
    plt.grid(True)

    plt.show()

# -------------------------------
# PARSE AI OUTPUT
# -------------------------------
def parse_ai_output(text):

    titles = re.findall(r"Title \d: (.*)", text)
    description_match = re.search(r"Description:\n([\s\S]*?)\n\nHashtags:", text)
    hashtags_match = re.search(r"Hashtags:\n([\s\S]*)", text)

    description = description_match.group(1).strip() if description_match else ""
    hashtags = hashtags_match.group(1).strip() if hashtags_match else ""

    return titles, description, hashtags