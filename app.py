import streamlit as st
import openai
import random
import re

# Set OpenAI API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# UI Setup
st.set_page_config(page_title="Pharma Prep", layout="centered")
st.title("💊 Pharma Prep")
st.markdown("""
Welcome to **Pharma Prep**, your UK pharmacy exam revision assistant.

Choose a topic and question type. Questions are based strictly on UK guidelines (NICE, BNF, MHRA).

---
""")

# Sidebar Inputs
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

# Generate prompt to OpenAI
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

# Parse MCQ question into parts
def parse_mcq(question_text):
    # Expected format:
    # Question: ...
    # A) ...
    # B) ...
    # C) ...
    # D) ...
    # Answer: B
    # Source: NICE NG28
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

# Parse calculation question parts
def parse_calculation(text):
    # Expect question, answer and working out separated by lines
    # For simplicity, we can expect:
    # Question: ...
    # Answer: ...
    # Working out: ...
    # Source: ...
    question = None
    answer = None
    working_out = None
    source = None

    # Try to extract with simple regexes or line starts
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

# Main app logic
if st.button("🎯 Generate Question"):
    with st.spinner("Generating question..."):
        prompt = generate_prompt(topic, question_type)
        raw_text = get_openai_response(prompt)

        if "Error" in raw_text:
            st.error(raw_text)
        else:
            if question_type == "Multiple Choice":
                question, options, answer, source = parse_mcq(raw_text)
                st.markdown(f"### 📝 {question}")
                user_choice = st.radio("Select your answer:", list(options.values()))

                if st.button("Submit Answer", key="mcq_submit"):
                    # Find which option user selected
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

                user_input = st.text_input("Enter your numeric answer:")

                if st.button("Submit Answer", key="calc_submit"):
                    # Basic numeric comparison, ignoring whitespace, and float casting
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
                # For Flashcard and Short Answer, just show text
                st.markdown("### 📝 Question & Answer")
                st.markdown(raw_text)

# Disclaimer
st.markdown("""
---
📌 **Disclaimer:**  
This tool is for revision only and is not regulated by the GPhC or any official body.  
Information is sourced from **UK NICE**, **BNF**, and **MHRA** guidelines only.  
Always verify from official materials.
""")


