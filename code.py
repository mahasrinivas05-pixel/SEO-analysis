import re

# -------------------------------
# KEYWORD MATCH (SIMPLE COUNT)
# -------------------------------
def count_keywords_used(text, keywords):
    text = text.lower()
    return sum(1 for k in keywords if k in text)


# -------------------------------
# SCORING FUNCTION
# -------------------------------
def calculate_score(keyword_input, title, description):

    keywords = [k.strip().lower() for k in keyword_input.split(",") if k.strip()]
    title_l = title.lower()
    desc_l = description.lower()

    total_keywords = len(keywords)

    # -------------------------------
    # TITLE SCORE (30)
    # -------------------------------
    used_keywords = count_keywords_used(title_l, keywords)

    if total_keywords > 0:
        usage_ratio = used_keywords / total_keywords

        if usage_ratio >= 0.6:
            title_score = 30
        else:
            title_score = int(usage_ratio * 30)
    else:
        title_score = 0

    # -------------------------------
    # DESCRIPTION SCORE (30) - UPDATED
    # -------------------------------
    desc_score = 0

    # (A) Keyword Coverage (10 marks)
    desc_matches = sum(1 for k in keywords if k in desc_l)
    desc_ratio = desc_matches / total_keywords if total_keywords else 0

    if desc_ratio >= 0.9:
        desc_score += 10
    else:
        desc_score += int(desc_ratio * 10)

    # (B) Length Optimization (10 marks)
    desc_length = len(description)
    word_count = len(description.split())

    if 800 <= desc_length <= 1300:
        desc_score += 10
    else:
        # proportional scoring based on closeness
        if desc_length < 800:
            desc_score += int((desc_length / 800) * 10)
        elif desc_length > 1300:
            desc_score += int((1300 / desc_length) * 10)

    # (C) Minimum 5 Keywords Usage (10 marks)
    if desc_matches >= 5:
        desc_score += 10
    else:
        desc_score += int((desc_matches / 5) * 10)

    desc_score = min(desc_score, 30)

    # -------------------------------
    # HOOK SCORE (20)
    # -------------------------------
    power_words = [
        "what if", "secret", "shocking", "amazing", "unexpected", "truth",
        "best", "top", "guide", "tips",
        "brutal", "untold", "illegal", "dangerous", "rare", "instant",
        "proven", "exposed", "insider", "ultimate"
    ]

    hook_score = 0

    # 10 marks for power word
    if any(word in title_l for word in power_words):
        hook_score += 10

    # 10 marks for title length (40–60 chars)
    title_length = len(title)

    if 40 <= title_length <= 60:
        hook_score += 10
    else:
        if title_length < 40:
            hook_score += int((title_length / 40) * 10)
        elif title_length > 60:
            hook_score += int((60 / title_length) * 10)

    hook_score = min(hook_score, 20)

    # -------------------------------
    # CURIOSITY SCORE (20)
    # -------------------------------
    curiosity_words = [
        "secret", "shocking", "truth", "hidden", "revealed", "unknown",
        "mystery", "exposed", "insane", "unbelievable", "crazy",
        "unexpected", "surprising", "mind-blowing", "forbidden",
        "now", "before", "last chance", "finally", "must watch"
    ]

    matches = sum(1 for w in curiosity_words if w in title_l)

    curiosity_score = 0

    # 15 marks for curiosity words
    if matches >= 2:
        curiosity_score += 15
    elif matches == 1:
        curiosity_score += 8

    # 5 marks for grammar/sentence formation
    if len(title.split()) >= 4:
        curiosity_score += 5
    else:
        curiosity_score += 2

    curiosity_score = min(curiosity_score, 20)

    # -------------------------------
    # FINAL SCORE
    # -------------------------------
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