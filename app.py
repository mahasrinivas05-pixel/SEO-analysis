import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from code import calculate_score, parse_ai_output
from main import generate_ai_content

st.set_page_config(page_title="YouTube SEO AI Tool", layout="centered")

st.title("🎯 YouTube SEO Analyzer + AI Optimizer")

concept = st.text_input("Enter Concept (short like: YouTube growth tips)")
keywords = st.text_input("Enter Keywords (comma separated)")
title = st.text_input("Enter Title")
description = st.text_area("Enter Description")

# -----------------------
# SCORE + CHARTS
# -----------------------
if st.button("Analyze SEO Score"):

    if concept and keywords and title and description:

        result = calculate_score(keywords, title, description)

        st.subheader("📊 Your Score")
        st.write(f"Final Score: {result['Final Score']} / 100")

        labels = ["Title", "Description", "Hook", "Curiosity"]
        max_scores = [30, 30, 20, 20]
        obtained_scores = [
            result["Title Score"],
            result["Description Score"],
            result["Hook Score"],
            result["Curiosity Score"]
        ]

        remaining = [m - o for m, o in zip(max_scores, obtained_scores)]

        x = np.arange(len(labels))

        # BAR CHART
        fig1, ax1 = plt.subplots()
        ax1.bar(x, obtained_scores)
        ax1.bar(x, remaining, bottom=obtained_scores)

        ax1.set_xticks(x)
        ax1.set_xticklabels(labels)
        ax1.set_title("Score vs Max Score")

        st.pyplot(fig1)

        # LINE CHART
        fig2, ax2 = plt.subplots()
        ax2.plot(x, max_scores, marker='o', linestyle='--', label='Max')
        ax2.plot(x, obtained_scores, marker='o', label='Your Score')

        ax2.legend()
        st.pyplot(fig2)

    else:
        st.warning("Fill all fields")

# -----------------------
# AI GENERATION
# -----------------------
if st.button("Generate AI Suggestions"):

    if concept and keywords and title and description:

        with st.spinner("Generating AI..."):
            ai_output = generate_ai_content(concept, keywords, title, description)

        if "⚠️" in ai_output:
            st.warning(ai_output)
        else:
            st.success("AI Generated Successfully")
            st.write(ai_output)

        titles, ai_desc, hashtags = parse_ai_output(ai_output)

        best_score = 0
        best_title = ""

        for t in titles:
            score = calculate_score(keywords, t, ai_desc)["Final Score"]

            if score > best_score:
                best_score = score
                best_title = t

        st.success(f"🏆 Best Title: {best_title} ({best_score})")

        st.subheader("📄 Description")
        st.write(ai_desc)

        st.subheader("#️⃣ Hashtags")
        st.write(hashtags)

    else:
        st.warning("Fill all fields")