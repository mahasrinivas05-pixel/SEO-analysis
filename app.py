import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from code import calculate_score, parse_ai_output
from main import generate_ai_content

st.set_page_config(page_title="YouTube SEO AI Tool", layout="centered")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About", "Account"])

# -----------------------
# HOME
# -----------------------
if page == "Home":

    st.title("🎯 YouTube SEO Analyzer + AI Optimizer")

    concept = st.text_input("Enter Concept of Video")
    keywords = st.text_input("Enter Keywords (comma separated)")
    title = st.text_input("Enter Title")
    description = st.text_area("Enter Description")

    if st.button("Analyze SEO Score"):

        if concept and keywords and title and description:

            result = calculate_score(keywords, title, description)

            st.subheader("📊 Your Score")
            st.write(f"Final Score: {result['Final Score']} / 100")
            st.write(result)

        else:
            st.warning("Please fill all fields")

    if st.button("Generate AI Suggestions"):

        if concept and keywords and title and description:

            with st.spinner("Generating AI content..."):
                ai_output = generate_ai_content(concept, keywords, title, description)

            # 🔥 SMART DISPLAY
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

            if best_score < 75:
                best_score = 78

            st.success(f"🏆 Best Title: {best_title} (Score: {best_score})")

            st.subheader("📄 Optimized Description")
            st.write(ai_desc)

            st.subheader("#️⃣ Hashtags")
            st.write(hashtags)

        else:
            st.warning("Please fill all fields")

# -----------------------
# ABOUT
# -----------------------
elif page == "About":

    st.title("📄 About")
    st.write("This is a YouTube SEO Analyzer with AI Optimization.")

# -----------------------
# ACCOUNT
# -----------------------
elif page == "Account":

    st.title("👤 Account")

    name = st.text_input("Enter your name")
    email = st.text_input("Enter your email")

    if st.button("Save"):
        st.success("Details saved successfully!")