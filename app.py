import streamlit as st
from code import calculate_score, parse_ai_output
from main import generate_ai_content

st.set_page_config(page_title="YouTube SEO AI Tool", layout="centered")

st.title("🎯 YouTube SEO Analyzer + AI Optimizer")

# -----------------------
# INPUT SECTION
# -----------------------
concept = st.text_input("Enter Concept of Video")
keywords = st.text_input("Enter Keywords (comma separated)")
title = st.text_input("Enter Title")
description = st.text_area("Enter Description")

# -----------------------
# SCORE BUTTON
# -----------------------
if st.button("Analyze SEO Score"):

    if concept and keywords and title and description:

        result = calculate_score(keywords, title, description)

        st.subheader("📊 Your Score")
        st.write(f"Final Score: {result['Final Score']} / 100")

        st.write(result)

    else:
        st.warning("Please fill all fields")

# -----------------------
# AI GENERATION
# -----------------------
if st.button("Generate AI Suggestions"):

    if concept and keywords and title and description:

        with st.spinner("Generating AI content..."):

            ai_output = generate_ai_content(concept, keywords, title, description)

        st.subheader("🧠 AI Suggestions")
        st.text(ai_output)

        # Parse output
        titles, ai_desc, hashtags = parse_ai_output(ai_output)

        st.subheader("🏆 Best Title")

        best_score = 0
        best_title = ""

        for t in titles:
            score = calculate_score(keywords, t, ai_desc)["Final Score"]

            if score > best_score:
                best_score = score
                best_title = t

        st.success(f"{best_title} (Score: {best_score})")

        st.subheader("📄 Optimized Description")
        st.write(ai_desc)

        st.subheader("#️⃣ Hashtags")
        st.write(hashtags)

    else:
        st.warning("Please fill all fields")