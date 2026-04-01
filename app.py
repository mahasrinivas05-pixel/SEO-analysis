import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from code import calculate_score, parse_ai_output
from main import generate_ai_content

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Maha's SEO Analyzer", layout="wide")

# -----------------------
# CUSTOM CSS (BLACK + NEON UI)
# -----------------------
st.markdown("""
<style>
body {
    background-color: #0a0a0a;
    color: white;
}

h1, h2, h3, h4, h5, h6, p {
    color: white;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
}

.nav-right {
    display: flex;
    gap: 20px;
}

.nav-button {
    color: white;
    text-decoration: none;
    font-weight: bold;
}

.neon-button {
    padding: 10px 20px;
    border: 2px solid #00ffff;
    border-radius: 10px;
    color: #00ffff;
    box-shadow: 0 0 10px #00ffff;
    text-decoration: none;
}

.section {
    padding: 60px 20px;
    text-align: center;
}

.card {
    background: #111;
    padding: 20px;
    border-radius: 10px;
    margin: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# NAVBAR
# -----------------------
st.markdown("""
<div class="navbar">
    <h2>Maha's SEO Analyzer</h2>
    <div class="nav-right">
        <a class="nav-button" href="#">Home</a>
        <a class="nav-button" href="#">About</a>
        <a class="neon-button" href="#">Analyzer</a>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------
# HERO SECTION
# -----------------------
st.markdown("""
<div class="section">
    <h1>🚀 AI-Powered YouTube SEO Optimizer</h1>
    <p>Turn your video ideas into high-performing titles, descriptions, and hashtags — instantly.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------
# ABOUT TOOL
# -----------------------
st.markdown("""
<div class="section">
    <h2>Why This Tool Exists</h2>
    <p>Creating YouTube content is easy. Getting views is not.</p>
    <p>This AI-powered tool analyzes your title and description, scores your SEO performance, and instantly suggests optimized content designed to improve visibility, click-through rate, and engagement.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------
# HOW IT WORKS
# -----------------------
st.markdown("""
<div class="section">
    <h2>How It Works</h2>
    <p>Enter your video concept, keywords, title, and description</p>
    <p>Get an instant SEO score out of 100</p>
    <p>View performance insights with visual charts</p>
    <p>Generate high-CTR AI titles, descriptions, and hashtags</p>
</div>
""", unsafe_allow_html=True)

# -----------------------
# ANALYZER SECTION
# -----------------------
st.markdown("---")
st.header("🔍 Analyzer")

col1, col2 = st.columns(2)

with col1:
    concept = st.text_input("Video Concept")
    keywords = st.text_input("Keywords")

with col2:
    title = st.text_input("Title")
    description = st.text_area("Description")

colb1, colb2 = st.columns(2)

analyze = colb1.button("Analyze SEO")
generate = colb2.button("Generate AI")

# -----------------------
# ANALYZE LOGIC (UNCHANGED)
# -----------------------
if analyze:
    if concept and keywords and title and description:
        result = calculate_score(keywords, title, description)

        st.success(f"Score: {result['Final Score']} / 100")

        labels = ["Title", "Description", "Hook", "Curiosity"]
        max_scores = [30, 30, 20, 20]
        obtained_scores = [
            result["Title Score"],
            result["Description Score"],
            result["Hook Score"],
            result["Curiosity Score"]
        ]

        x = np.arange(len(labels))

        fig, ax = plt.subplots()
        ax.bar(x, obtained_scores)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)

        st.pyplot(fig)

# -----------------------
# AI LOGIC (UNCHANGED)
# -----------------------
if generate:
    if concept and keywords and title and description:

        ai_output = generate_ai_content(concept, keywords, title, description)

        st.text(ai_output)

        titles, ai_desc, hashtags = parse_ai_output(ai_output)

        best_score = 0
        best_title = ""

        for t in titles:
            score = calculate_score(keywords, t, ai_desc)["Final Score"]
            if score > best_score:
                best_score = score
                best_title = t

        st.success(best_title)
        st.write(ai_desc)
        st.write(hashtags)

# -----------------------
# ABOUT SECTION
# -----------------------
st.markdown("""
<div class="section">
    <h2>About</h2>
    <p>Hi, I’m Mahalakshmi S, currently pursuing my M.Sc. in Data Science at Periyar University.</p>
    <p>I created this website to help YouTube beginners understand and improve their content using simple, practical guidance.</p>
    <p>This platform aims to make YouTube growth easier using data-driven insights.</p>
</div>
""", unsafe_allow_html=True)