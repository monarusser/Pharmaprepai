import streamlit as st
import openai
import random
import re

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set page configuration
st.set_page_config(page_title="Pharma Prep", page_icon="💊", layout="centered")

# Topic revision summaries
topics = {
    "Cardiovascular": "Review of hypertension, lipid management, heart failure, anticoagulation...",
    "Musculoskeletal": "Key treatments for arthritis, osteoporosis, gout...",
    "Infection": "Antibiotic stewardship, common infections, resistance...",
    "Endocrine": "Diabetes management, thyroid disorders, adrenal insufficiency...",
    "Respiratory": "Asthma, COPD, inhaler techniques...",
    "Gastrointestinal": "Peptic ulcer disease, IBS, liver pathology...",
    "Genito-urinary": "UTIs, contraception, prostate disorders...",
    "Nervous System": "Epilepsy, Parkinson’s disease, migraine management...",
    "Cancer/Immuno": "Chemotherapy fundamentals, immunosuppressants...",
    "Eye/Ear/Nose/Skin": "Common eye infections, dermatitis, ENT conditions...",
    "Nutrition/Blood": "Anaemia, vitamin deficiencies, anticoagulant dosing...",
    "Vaccination": "UK immunisation schedule, vaccine types...",
    "Emergency Meds": "Anaphylaxis management, overdose protocols, emergency drugs...",
    "Pharmacy Law & Ethics": "GPhC standards, prescribing legislation, ethical scenarios...",
    "Calculations": "Dose calculations, unit conversions, IV infusion rates..."
}

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = None
if 'raw_text' not in st.session_state:
    st.session_state.raw_text = None

# UI: Homepage
def show_homepage():
    st.title("💊 Pharma Prep")
    st.markdown("""
    Welcome to **Pharma Prep**, your UK pharmacy exam revision assistant.

    Select a topic to review and practice.
    """)
    cols = st.columns(3)
    for i, topic in enumerate(topics.keys()):
        if cols[i % 3].button(topic):
            st.session_state.selected_topic = topic
            st.session_state.page = 'summary'

# UI: Revision Summary
def show_summary():
    topic = st.session_state.selected_topic
    st.header(f"Revision Summary: {topic}")
    st.write(topics[topic])
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Questions"):
            st.session_state.page = 'quiz'
    with col2:
        if st.button("Back to Topics"):
            st.session_state.page = 'home'
            st.session_state.selected_topic = None

# Prompt generation
def generate_prompt(topic, question_type):
    if question_type == "Calculation":
        style = (
            "Generate a pharmacy calculation question based on UK BNF/NICE guidelines. "
            "Include the question, the correct numeric answer, and a step-by-step working out explanation. Cite the guideline source."
        )
    elif question_type == "Flashcard":
        style = "Generate a flashcard-style question and answer using UK NICE/BNF guidelines."
    elif question_type == "Multiple Choice":
        style = (
            "Generate a multiple choice pharmacy exam question with 4 options and one correct answer. "
            "Use only NICE or BNF UK guidelines. Label the correct option and cite the source."
        )
    else:
        style = "Generate a short-answer pharmacy exam question that requires a 1–2 word answer. Cite the UK guideline source."
    return f"""
You are a pharmacy exam tutor helping students revise for UK pharmacy exams (GPhC, pre-reg, etc.).

Topic: {topic}

{style}

Only show one question. Cite the NICE, BNF, or MHRA guideline (e.g. BNF Chapter 2.5, NICE NG28).

Do not create US content. Use UK guidelines only.
"""

# OpenAI call
def get_openai_response(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

# Parsing functions
def parse_mcq(text):
    lines = text.split('\n')
    question, options, answer, source = "", {}, None, None
    for line in lines:
        if line.startswith("Question:"):
            question = line.split("Question:")[1].strip()
        elif any(line.startswith(f"{c})") for c in ['A','B','C','D']):
            letter = line[0]
            options[letter] = line.split(f"{letter})")[1].strip()
        elif line.startswith("Answer:"):
            answer = line.split("Answer:")[1].strip()
        elif line.startswith("Source:"):
            source = line.split("Source:")[1].strip()
    return question, options, answer, source

def parse_calculation(text):
    lines = text.split('\n')
    question, answer, working_out, source = None, None, [], None
    in_work = False
    for line in lines:
        if line.startswith("Question:"):
            question = line.split("Question:")[1].strip()
        elif line.startswith("Answer:"):
            answer = line.split("Answer:")[1].strip()
        elif line.startswith("Working out:"):
            in_work = True
            working_out.append(line.split("Working out:")[1].strip())
        elif line.startswith("Source:"):
            in_work = False
            source = line.split("Source:")[1].strip()
        elif in_work:
            working_out.append(line.strip())
    return question, answer, "\n".join(working_out), source

# UI: Quiz page
def show_quiz():
    st.header(f"Questions on {st.session_state.selected_topic}")
    question_type = st.selectbox("Question Type:", ["Multiple Choice","Short Answer","Flashcard","Calculation"])

    if st.button("🎯 Generate Question"):
        prompt = generate_prompt(st.session_state.selected_topic, question_type)
        st.session_state.raw_text = get_openai_response(prompt)

    raw = st.session_state.raw_text
    if raw:
        st.text_area("### Raw AI response", raw, height=200)

        if question_type == "Multiple Choice":
            if "mcq_data" not in st.session_state:
                q, opts, ans, src = parse_mcq(raw)
                st.session_state.mcq_data = {"question": q, "options": opts, "answer": ans, "source": src}
            data = st.session_state.mcq_data
            st.markdown(f"**{data['question']}**")
            choice = st.radio("Select your answer:", list(data['options'].values()), key="mcq_choice")
            if st.button("Submit Answer", key="mcq_submit"):
                sel = next(k for k,v in data['options'].items() if v==choice)
                if sel == data['answer']:
                    st.success(f"Correct! ✅\nSource: {data['source']}")
                else:
                    st.error(f"Incorrect. ❌ The correct answer is {data['answer']}) {data['options'][data['answer']]}\nSource: {data['source']}")

        elif question_type == "Calculation":
            if "calc_data" not in st.session_state:
                q,a,wo,src = parse_calculation(raw)
                st.session_state.calc_data = {"question": q, "answer": a, "working_out": wo, "source": src}
            data = st.session_state.calc_data
            st.markdown(f"**{data['question']}**")
            user_ans = st.text_input("Enter your numeric answer:", key="calc_input")
            if st.button("Submit Answer", key="calc_submit"):
                try:
                    u = float(user_ans.strip())
                    c = float(re.findall(r"[-+]?\d*\.\d+|\d+", data['answer'])[0])
                    if abs(u-c) < 0.01:
                        st.success(f"Correct! ✅\nWorking out:\n{data['working_out']}\nSource: {data['source']}")
                    else:
                        st.error(f"Incorrect. ❌ The correct answer is {data['answer']}\nWorking out:\n{data['working_out']}\nSource: {data['source']}")
                except:
                    st.error("Please enter a valid numeric answer.")

        else:
            st.markdown(f"**Question & Answer**")
            st.markdown(raw)

# Main navigation
if st.session_state.page == 'home':
    show_homepage()
elif st.session_state.page == 'summary':
    show_summary()
elif st.session_state.page == 'quiz':
    show_quiz()

# Disclaimer
st.markdown("""
---
📌 **Disclaimer:**
This tool is for revision only and is not regulated by the GPhC or any official body.
Information is sourced from **UK NICE**, **BNF**, and **MHRA** guidelines only.
Always verify from official materials.
""", unsafe_allow_html=True)


