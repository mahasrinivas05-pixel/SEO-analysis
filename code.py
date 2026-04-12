import re

# -------------------------------
# FLEXIBLE KEYWORD MATCH
# -------------------------------
def keyword_match_score(text, keyword):
    text = text.lower()
    keyword = keyword.lower()

    # Exact match
    if keyword in text:
        return 1.0

    # Partial match (split words)
    parts = keyword.split()
    matches = sum(1 for p in parts if p in text)

    return matches / len(parts) if parts else 0


# -------------------------------
# SCORING FUNCTION
# -------------------------------
def calculate_score(keyword_input, title, description):

    keywords = [k.strip().lower() for k in keyword_input.split(",") if k.strip()]
    title_l = title.lower()
    desc_l = description.lower()

    total_keywords = len(keywords)

    # TITLE SCORE (Flexible)
    title_match_score = sum(keyword_match_score(title_l, k) for k in keywords)
    title_ratio = title_match_score / total_keywords if total_keywords else 0
    title_score = int(title_ratio * 30)

    # DESCRIPTION SCORE (Flexible)
    desc_match_score = sum(keyword_match_score(desc_l, k) for k in keywords)
    desc_ratio = desc_match_score / total_keywords if total_keywords else 0
    desc_score = int(desc_ratio * 30)

    # HOOK SCORE (More forgiving)
    power_words = ["what if", "secret", "shocking", "amazing", "unexpected", "truth"]
    hook_score = 0

    for word in power_words:
        if word in title_l:
            hook_score += 6

    if hook_score == 0 and any(w in title_l for w in ["best", "top", "guide", "tips"]):
        hook_score = 8  # fallback hook

    hook_score = min(hook_score, 20)

    # CURIOSITY SCORE (More natural)
    curiosity_score = 0

    if "?" in title:
        curiosity_score += 10

    if re.search(r"\bvs\b|\bmeet\b|\bstory\b|\bjourney\b|\bwhy\b|\bhow\b", title_l):
        curiosity_score += 10

    if curiosity_score == 0:
        curiosity_score = 8  # fallback curiosity

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
# PARSE AI OUTPUT
# -------------------------------
def parse_ai_output(text):

    titles = re.findall(r"Title \d: (.*)", text)
    description_match = re.search(r"Description:\n([\s\S]*?)\n\nHashtags:", text)
    hashtags_match = re.search(r"Hashtags:\n([\s\S]*)", text)

    description = description_match.group(1).strip() if description_match else ""
    hashtags = hashtags_match.group(1).strip() if hashtags_match else ""

    return titles, description, hashtags