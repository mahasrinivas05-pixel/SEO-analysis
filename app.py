import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from code import calculate_score, parse_ai_output
from main import generate_ai_content

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="AI YouTube SEO Tool", layout="wide")

# -----------------------
# HERO SECTION
# -----------------------
st.markdown("""
<h1 style='text-align:center;'>🚀 AI YouTube SEO Analyzer</h1>
<p style='text-align:center;'>Optimize your videos with AI-powered insights</p>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------
# INPUT SECTION (2 COLUMN)
# -----------------------
col1, col2 = st.columns(2)

with col1:
    concept = st.text_input("🎯 Video Concept")
    keywords = st.text_input("🔑 Keywords (comma separated)")

with col2:
    title = st.text_input("📌 Title")
    description = st.text_area("📝 Description")

st.markdown("---")

# -----------------------
# BUTTONS
# -----------------------
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    analyze = st.button("📊 Analyze SEO")

with col_btn2:
    generate = st.button("⚡ Generate AI Suggestions")

# -----------------------
# ANALYZE SECTION
# -----------------------
if analyze:

    if concept and keywords and title and description:

        result = calculate_score(keywords, title, description)

        st.subheader("📊 SEO Score")
        st.success(f"{result['Final Score']} / 100")

        # -----------------------
        # CHARTS
        # -----------------------
        labels = ["Title", "Description", "Hook", "Curiosity"]
        max_scores = [30, 30, 20, 20]
        obtained_scores = [
            result["Title Score"],
            result["Description Score"],
            result["Hook Score"],
            result["Curiosity Score"]
        ]

        remaining_scores = [m - o for m, o in zip(max_scores, obtained_scores)]

        col_chart1, col_chart2 = st.columns(2)

        # BAR CHART
        with col_chart1:
            fig1, ax1 = plt.subplots()
            x = np.arange(len(labels))

            ax1.bar(x, obtained_scores)
            ax1.bar(x, remaining_scores, bottom=obtained_scores)

            ax1.set_xticks(x)
            ax1.set_xticklabels(labels)
            ax1.set_title("Score vs Max Score")

            st.pyplot(fig1)

        # LINE CHART
        with col_chart2:
            fig2, ax2 = plt.subplots()

            ax2.plot(x, max_scores, marker='o', linestyle='--', label='Max')
            ax2.plot(x, obtained_scores, marker='o', linewidth=3, label='Achieved')

            ax2.set_xticks(x)
            ax2.set_xticklabels(labels)
            ax2.set_title("Performance")

            ax2.legend()
            ax2.grid(True)

            st.pyplot(fig2)

    else:
        st.warning("Fill all fields")

# -----------------------
# AI SECTION
# -----------------------
if generate:

    if concept and keywords and title and description:

        with st.spinner("Generating AI Suggestions..."):

            ai_output = generate_ai_content(concept, keywords, title, description)

        st.subheader("🧠 AI Suggestions")
        st.text(ai_output)

        titles, ai_desc, hashtags = parse_ai_output(ai_output)

        # BEST TITLE
        best_score = 0
        best_title = ""

        for t in titles:
            score = calculate_score(keywords, t, ai_desc)["Final Score"]
            if score > best_score:
                best_score = score
                best_title = t

        st.subheader("🏆 Best Title")
        st.success(f"{best_title} ({best_score})")

        st.subheader("📄 Description")
        st.write(ai_desc)

        st.subheader("#️⃣ Hashtags")
        st.write(hashtags)

    else:
        st.warning("Fill all fields")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.markdown("<p style='text-align:center;'>Powered by MRBR Studio</p>", unsafe_allow_html=True)