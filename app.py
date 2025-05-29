import streamlit as st
import openai
import random

# Set OpenAI API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---------- UI SETUP ----------

st.set_page_config(page_title="Pharma Prep", layout="centered")
st.title("💊 Pharma Prep")
st.markdown("""
Welcome to **Pharma Prep**, your intelligent pharmacy revision assistant for GPhC and UK-based pharmacy exams.

Select a topic and question type to begin. All content is based on **UK resources only**, such as **BNF**, **NICE**, and **MHRA**.

---
""")

# ---------- Sidebar Inputs ----------

st.sidebar.header("🧠 Customize Your Practice")
topic = st.sidebar.selectbox("Choose a topic", [
    "Cardiovascular",
    "Musculoskeletal",
    "Infection",
    "Endocrine",
    "Respiratory",
    "Gastrointestinal",
    "Genito-urinary",
    "Nervous System",
    "Cancer/Immuno",
    "Eye/Ear/Nose/Skin",
    "Nutrition/Blood",
    "Vaccination",
    "Emergency Meds",
    "Pharmacy Law & Ethics",
    "Calculations"
])

question_type = st.sidebar.selectbox("Question Type", [
    "Multiple Choice",
    "Short Answer",
    "Flashcard",
    "Calculation"
])

# ---------- Prompt Setup ----------

def generate_prompt(topic, question_type):
    if question_type == "Calculation":
        style = "Generate a pharmacy calculation question based on UK BNF/NICE guidelines with the correct answer and source. No explanation."
    elif question_type == "Flashcard":
        style = "Generate a flashcard-style question and answer using UK NICE/BNF guidelines."
    elif question_type == "Multiple Choice":
        style = "Generate a multiple choice pharmacy exam question with 4 options and one correct answer. Use only NICE or BNF UK guidelines. Label the correct option and cite the source."
    else:
        style = "Generate a short-answer pharmacy exam question that requires a 1–2 word answer. Cite the UK guideline source."

    return f"""
You are a pharmacy exam tutor helping students revise for UK pharmacy exams (GPhC, pre-reg, etc.).

Topic: {topic}

{style}
Only show one question. Include the correct answer and cite the NICE, BNF, or MHRA guideline (e.g. BNF Chapter 2.5, NICE NG28).

Do not create US content. Use UK guidelines only.
"""

# ---------- OpenAI Call ----------

def get_question(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

# ---------- Main App ----------

if st.button("🎯 Generate Question"):
    with st.spinner("Generating..."):
        prompt = generate_prompt(topic, question_type)
        result = get_question(prompt)
        st.markdown("### 📝 Question")
        st.markdown(result)

        st.markdown("---")
        st.markdown("💬 **Was this helpful?**")
        feedback = st.radio("Your feedback:", ["👍 Yes", "👎 No"], key=random.randint(0, 10000))
        if feedback:
            st.success("Thanks for your feedback!")

# ---------- Disclaimer ----------

st.markdown("""
---
📌 **Disclaimer:**  
This tool is for revision purposes only. It is not regulated by the GPhC or any official body. All medical information is based on publicly available UK guidelines such as the **BNF**, **NICE**, and **MHRA**.

Always refer to official sources when in doubt.
""")

