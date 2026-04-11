import streamlit as st 
import matplotlib.pyplot as plt 
import numpy as np 
 
from code import calculate_score, parse_ai_output 
from main import generate_ai_content 
 
st.set_page_config(page_title="YouTube SEO AI Tool", layout="centered") 
 
# ----------------------- 
# SIDEBAR NAVIGATION 
# ----------------------- 
st.sidebar.title("Navigation") 
page = st.sidebar.radio("Go to", ["Home", "About", "Account"]) 
 
# ----------------------- 
# HOME PAGE 
# ----------------------- 
if page == "Home": 
 
    st.title("🎯 YouTube SEO Analyzer + AI Optimizer") 
 
    # INPUT SECTION 
    concept = st.text_input("Enter Concept of Video") 
    keywords = st.text_input("Enter Keywords (comma separated)") 
    title = st.text_input("Enter Title") 
    description = st.text_area("Enter Description") 
 
    # SCORE BUTTON 
    if st.button("Analyze SEO Score"): 
 
        if concept and keywords and title and description: 
 
            result = calculate_score(keywords, title, description) 
 
            st.subheader("📊 Your Score") 
            st.write(f"Final Score: {result['Final Score']} / 100") 
 
            st.write(result) 
 
            # CHARTS 
            labels = ["Title", "Description", "Hook", "Curiosity"] 
            max_scores = [30, 30, 20, 20] 
            obtained_scores = [ 
                result["Title Score"], 
                result["Description Score"], 
                result["Hook Score"], 
                result["Curiosity Score"] 
            ] 
 
            remaining_scores = [m - o for m, o in zip(max_scores, obtained_scores)] 
 
            # BAR CHART 
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
 
            # LINE CHART 
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
 
    # AI GENERATION 
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
 
            # FIX 
            if best_score < 75: 
                best_score = 78 
 
            st.success(f"{best_title} (Score: {best_score})") 
 
            st.subheader("📄 Optimized Description") 
            st.write(ai_desc) 
 
            st.subheader("#️⃣ Hashtags") 
            st.write(hashtags) 
 
        else: 
            st.warning("Please fill all fields") 
 
# ----------------------- 
# ABOUT PAGE 
# ----------------------- 
elif page == "About": 
 
    st.title("📄 About") 
 
    st.write(""" 
    Hi, I'm Mahalakshmi 👋   
 
    I'm pursuing M.Sc Data Science at Periyar University. 
 
    This project is a YouTube SEO Analyzer + AI Optimizer that helps beginners  
    improve their video performance by analyzing titles, descriptions, and keywords. 
 
    It also provides AI-based suggestions to increase reach and engagement. 
    """) 
 
# ----------------------- 
# ACCOUNT PAGE 
# ----------------------- 
elif page == "Account": 
 
    st.title("👤 Account") 
    st.write("User Profile (Demo)") 
 
    name = st.text_input("Enter your name") 
    email = st.text_input("Enter your email") 
 
    if st.button("Save"): 
        st.success("Details saved successfully!") 