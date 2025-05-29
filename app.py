import streamlit as st
import openai
import re

# OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Topics and revision summaries
topics = {
    "Cardiovascular": "Review of hypertension, lipid management, heart failure, anticoagulation...",
    "Musculoskeletal": "Key treatments for arthritis, osteoporosis, gout...",
    "Infection": "Antibiotics stewardship, common infections, resistance...",
    "Endocrine": "Diabetes management, thyroid disorders, adrenal insufficiency...",
    "Respiratory": "Asthma, COPD, inhaler techniques...",
    "Gastrointestinal": "Peptic ulcers, IBS, liver diseases...",
    "Genito-urinary": "UTIs, contraception, prostate disorders...",
    "Nervous System": "Epilepsy, Parkinson’s, migraine management...",
    "Cancer/Immuno": "Chemotherapy basics, immunosuppressants...",
    "Eye/Ear/Nose/Skin": "Common eye infections, dermatitis, ENT conditions...",
    "Nutrition/Blood": "Anaemia, vitamin deficiencies, anticoagulants...",
    "Vaccination": "UK immunisation schedule, vaccine types...",
    "Emergency Meds": "Anaphylaxis, overdose, emergency protocols...",
    "Pharmacy Law & Ethics": "GPhC standards, prescription regulations...",
    "Calculations": "Dose calculations, conversions, IV drip rates..."
}

# Session state setup
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = None

# ------------------- UI Functions --------------------

def show_homepage():
    st.title("💊 Pharma Prep")
    st.write("Select a topic to start revising:")
    cols = st.columns(3)
    for i, topic in enumerate(topics.keys()):
        if cols[i % 3].button(topic):
            st.session_state.selected_topic = topic
            st.session_state.page = 'summary'

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

def generate_prompt(topic, question_type):
    if question_type == "Calculation":
        style = ("Generate a pharmacy calculation question based on UK BNF/NICE guidelines. "
                 "Include the question, the correct numeric answer, and a step-by-step working out "
                 "explanation. Cite the guideline source.")
    elif question_type == "Flashcard":
        style = "Generate a flashcard-style question and answer using UK NICE/BNF guidelines."
    elif question_type == "Multiple Choice":
        style = ("Generate a multiple choice pharmacy exam question with 4 options and one correct answer. "
                 "Use only NICE or BNF UK guidelines. Label the correct option and cite the source.")
    else:
        style = "Generate a short-answer pharmacy exam question that requires a 1–2 word answer. Cite the UK guideline source."

    return f"""
You are a pharmacy exam tutor helping students revise for UK pharmacy exams (GPhC, pre-reg, etc.).

Topic: {topic}

{style}

Only show one question. Cite the NICE, BNF, or MHRA guideline (e.g. BNF Chapter 2.5, NICE NG28).

Do not create US content. Use UK guidelines only.
"""

def get_openai_response(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

def parse_mcq(question_text):
    lines = question_text.split('\n')
    question = ""
    options = {}
    answer = None
    source = None
    option_letters = ['A', 'B', 'C', 'D']

    for line in lines:
        if line.startswith("Question:"):
            question = line[len("Question:"):].strip()
        elif any(line.startswith(f"{opt})") for opt in option_letters):
            for opt in option_letters:
                if line.startswith(f"{opt})"):
                    options[opt] = line[len(f"{opt})"):].strip()
        elif line.startswith("Answer:"):
            answer = line[len("Answer:"):].strip()
        elif line.startswith("Source:"):
            source = line[len("Source:"):].strip()

    return question, options, answer, source

def parse_calculation(text):
    question = None
    answer = None
    working_out = None
    source = None

    lines = text.split('\n')
    temp_working_lines = []
    in_working_out = False

    for line in lines:
        if line.startswith("Question:"):
            question = line[len("Question:"):].strip()
        elif line.startswith("Answer:"):
            answer = line[len("Answer:"):].strip()
        elif line.startswith("Working out:"):
            in_working_out = True
            temp_working_lines.append(line[len("Working out:"):].strip())
        elif line.startswith("Source:"):
            in_working_out = False
            source = line[len("Source:"):].strip()
        else:
            if in_working_out:
                temp_working_lines.append(line.strip())

    working_out = "\n".join(temp_working_lines).strip()
    return question, answer, working_out, source

def show_quiz():
    topic = st.session_state.selected_topic
    st.header(f"Questions on {topic}")

    question_type = st.selectbox("Choose question type:", ["Multiple Choice", "Short Answer", "Flashcard", "Calculation"])

    if st.button("🎯 Generate Question"):
        with st.spinner("Generating question..."):
            prompt = generate_prompt(topic, question_type)
            raw_text = get_openai_response(prompt)

        if "Error" in raw_text:
            st.error(raw_text)
            return

        # Debug: Show raw AI response for transparency
        st.text_area("### Raw AI response", raw_text, height=200)

        if question_type == "Multiple Choice":
            question, options, answer, source = parse_mcq(raw_text)
            st.markdown(f"### 📝 {question}")
            user_choice = st.radio("Select your answer:", list(options.values()), key="mcq_radio")

            if st.button("Submit Answer", key="mcq_submit"):
                selected_opt = None
                for opt, val in options.items():
                    if val == user_choice:
                        selected_opt = opt
                        break
                if selected_opt == answer:
                    st.success(f"Correct! ✅\n\nSource: {source}")
                else:
                    st.error(f"Incorrect. ❌ The correct answer is {answer}) {options[answer]}\n\nSource: {source}")

        elif question_type == "Calculation":
            question, correct_answer, working_out, source = parse_calculation(raw_text)
            st.markdown(f"### 📝 {question}")

            user_input = st.text_input("Enter your numeric answer:", key="calc_input")

            if st.button("Submit Answer", key="calc_submit"):
                try:
                    user_val = float(user_input.strip())
                    correct_val = float(re.findall(r"[-+]?\d*\.\d+|\d+", correct_answer)[0])
                    if abs(user_val - correct_val) < 0.01:
                        st.success(f"Correct! ✅\n\nWorking out:\n{working_out}\n\nSource: {source}")
                    else:
                        st.error(f"Incorrect. ❌ The correct answer is {correct_answer}\n\nWorking out:\n{working_out}\n\nSource: {source}")
                except Exception:
                    st.error("Please enter a valid numeric answer.")

        else:
            # For Short Answer and Flashcard just display the AI response
            st.markdown("### 📝 Question & Answer")
            st.markdown(raw_text)

# Main app navigation
def main():
    if st.session_state.page == 'home':
        show_homepage()
    elif st.session_state.page == 'summary':
        show_summary()
    elif st.session_state.page == 'quiz':
        show_quiz()

    # Disclaimer always at bottom
    st.markdown("""
---
📌 **Disclaimer:**  
This tool is for revision only and is not regulated by the GPhC or any official body.  
Information is sourced from **UK NICE**, **BNF**, and **MHRA** guidelines only.  
Always verify from official materials.
""")

if __name__ == "__main__":
    main()

