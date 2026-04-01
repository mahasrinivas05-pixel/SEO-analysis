import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from code import calculate_score, parse_ai_output
from main import generate_ai_content

st.set_page_config(page_title="Maha's SEO Analyzer", layout="wide")

# -----------------------
# CUSTOM CSS (PROFESSIONAL WHITE UI)
# -----------------------
st.markdown("""
<style>
/* General */
body {
    font-family: 'Segoe UI', sans-serif;
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 30px;
    border-bottom: 1px solid #eee;
}

.nav-links {
    display: flex;
    gap: 20px;
}

.nav-links a {
    text-decoration: none;
    color: #333;
    font-weight: 500;
}

.nav-button {
    padding: 8px 18px;
    border-radius: 8px;
    background: #000;
    color: #fff !important;
}

/* Hero */
.hero {
    text-align: center;
    padding: 60px 20px;
}

.hero h1 {
    font-size: 40px;
    font-weight: bold;
}

.hero p {
    font-size: 18px;
    color: #555;
}

.cta-btn {
    margin-top: 20px;
    padding: 12px 25px;
    background: black;
    color: white;
    border-radius: 10px;
    text-decoration: none;
    display: inline-block;
}

/* Sections */
.section {
    padding: 50px 20px;
    text-align: center;
}

.section h2 {
    margin-bottom: 20px;
}

.card {
    background: #f9f9f9;
    padding: 20px;
    border-radius: 10px;
    margin: 10px;
}

/* Analyzer */
.analyzer-box {
    background: #fafafa;
    padding: 30px;
    border-radius: 12px;
    border: 1px solid #eee;
}

/* Responsive */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 28px;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# NAVBAR
# -----------------------
st.markdown("""
<div class="navbar">
    <h3>Maha's SEO Analyzer</h3>
    <div class="nav-links">
        <a href="#">Home</a>
        <a href="#">About</a>
        <a class="nav-button" href="#">Analyzer</a>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------
# HERO SECTION
# -----------------------
st.markdown("""
<div class="hero">
    <h1>🚀 AI-Powered YouTube SEO Optimizer</h1>
    <p>Turn your video ideas into high-performing titles, descriptions, and hashtags — instantly.</p>
    <a class="cta-btn">Try the Tool Now</a>
</div>
""", unsafe_allow_html=True)

# -----------------------
# ABOUT TOOL
# -----------------------
st.markdown("""
<div class="section">
    <h2>Why This Tool Exists</h2>
    <p>Creating YouTube content is easy. Getting views is not.</p>
    <p>This AI-powered tool analyzes your title and description, scores your SEO performance, and suggests optimized content to improve visibility and engagement.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------
# HOW IT WORKS
# -----------------------
st.markdown("""
<div class="section">
    <h2>How It Works</h2>
    <p>Enter your video concept, keywords, title, and description</p>
    <p>Get an instant SEO score</p>
    <p>View insights with charts</p>
    <p>Generate high-CTR AI content</p>
</div>
""", unsafe_allow_html=True)

# -----------------------
# ANALYZER UI (WRAPPED)
# -----------------------
st.markdown('<div class="section"><h2>🔍 Analyzer</h2></div>', unsafe_allow_html=True)

st.markdown('<div class="analyzer-box">', unsafe_allow_html=True)

concept = st.text_input("Enter Concept of Video")
keywords = st.text_input("Enter Keywords (comma separated)")
title = st.text_input("Enter Title")
description = st.text_area("Enter Description")

# -----------------------
# SCORE BUTTON (UNCHANGED)
# -----------------------
if st.button("Analyze SEO Score"):

    if concept and keywords and title and description:

        result = calculate_score(keywords, title, description)

        st.subheader("📊 Your Score")
        st.write(f"Final Score: {result['Final Score']} / 100")

        st.write(result)

        labels = ["Title", "Description", "Hook", "Curiosity"]
        max_scores = [30, 30, 20, 20]
        obtained_scores = [
            result["Title Score"],
            result["Description Score"],
            result["Hook Score"],
            result["Curiosity Score"]
        ]

        remaining_scores = [m - o for m, o in zip(max_scores, obtained_scores)]

        fig1, ax1 = plt.subplots()
        x = np.arange(len(labels))

        ax1.bar(x, obtained_scores)
        ax1.bar(x, remaining_scores, bottom=obtained_scores)

        ax1.set_xticks(x)
        ax1.set_xticklabels(labels)
        ax1.set_title("Score vs Max Score")

        for i in range(len(labels)):
            ax1.text(i, max_scores[i] + 1,
                     f"{obtained_scores[i]}/{max_scores[i]}",
                     ha='center', fontweight='bold')

        st.pyplot(fig1)

        fig2, ax2 = plt.subplots()

        ax2.plot(x, max_scores, marker='o', linestyle='--', label='Max Score')
        ax2.plot(x, obtained_scores, marker='o', linewidth=3, label='Achieved Score')

        ax2.set_xticks(x)
        ax2.set_xticklabels(labels)
        ax2.set_title("Performance Comparison")

        for i in range(len(labels)):
            ax2.text(i, obtained_scores[i] + 1,
                     f"{obtained_scores[i]}/{max_scores[i]}",
                     ha='center', fontweight='bold')

        ax2.legend()
        ax2.grid(True)

        st.pyplot(fig2)

    else:
        st.warning("Please fill all fields")

# -----------------------
# AI GENERATION (UNCHANGED)
# -----------------------
if st.button("Generate AI Suggestions"):

    if concept and keywords and title and description:

        with st.spinner("Generating AI content..."):

            ai_output = generate_ai_content(concept, keywords, title, description)

        st.subheader("🧠 AI Suggestions")
        st.text(ai_output)

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

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# ABOUT SECTION
# -----------------------
st.markdown("""
<div class="section">
    <h2>About</h2>
    <p>Hi, I’m Mahalakshmi S, pursuing M.Sc. Data Science at Periyar University.</p>
    <p>This platform helps creators improve YouTube performance using simple, practical strategies.</p>
</div>
""", unsafe_allow_html=True)