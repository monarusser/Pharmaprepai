import streamlit as st
import random

st.set_page_config(page_title="Pharma Prep AI", layout="centered")

# Disclaimer
disclaimer = """
⚠️ **Disclaimer:** This app is not regulated by the GPhC or any official regulatory body. It is intended only as a revision aid, based on UK guidelines such as NICE, BNF, and MHRA.
"""

# Sample Questions
topics = {
    "Cardiovascular": {
        "Hypertension": [
            {
                "question": "Which drug class is first-line for treating hypertension in a patient over 55 or of Black African/Caribbean descent?",
                "answer": "Calcium channel blocker",
                "type": "short",
                "source": "NICE NG136"
            },
            {
                "question": "What is the first-line antihypertensive drug for a Black adult over 55?",
                "options": ["ACE inhibitor", "Beta-blocker", "Calcium channel blocker", "Thiazide diuretic"],
                "answer": 2,
                "type": "mcq",
                "source": "NICE NG136"
            }
        ],
        "Heart Failure": [
            {
                "question": "Which drug is first-line for heart failure with reduced ejection fraction (HFrEF)?",
                "answer": "ACE inhibitor",
                "type": "short",
                "source": "NICE NG106"
            }
        ]
    },
    "Central Nervous System": {
        "Epilepsy": [
            {
                "question": "Which antiepileptic is first-line for tonic-clonic seizures?",
                "answer": "Sodium valproate",
                "type": "short",
                "source": "BNF CNS Chapter"
            }
        ],
        "Parkinson's Disease": [
            {
                "question": "Which class of drugs is commonly used first-line in Parkinson’s disease under age 65?",
                "answer": "Dopamine agonists",
                "type": "short",
                "source": "NICE NG71"
            }
        ]
    }
}

# App title
st.title("Pharma Prep AI - UK Pharmacy Exam Revision")
st.markdown("Welcome! Please select a main topic to start revising. All questions are based on UK guidelines (NICE, BNF, MHRA).")
st.markdown(disclaimer)

# Topic selection
main_topic = st.selectbox("Choose a Main Topic:", list(topics.keys()))

if main_topic:
    subtopics = list(topics[main_topic].keys())
    subtopic = st.selectbox("Choose a Subtopic:", subtopics)

    if subtopic:
        question_type = st.radio("Choose Question Type:", ["Multiple Choice", "Short Answer"])

        if st.button("Get Question"):
            data_pool = [
                q for q in topics[main_topic][subtopic]
                if (q["type"] == "mcq" and question_type == "Multiple Choice")
                or (q["type"] == "short" and question_type == "Short Answer")
            ]

            if data_pool:
                data = random.choice(data_pool)

                st.subheader("📝 Question:")
                st.markdown(data["question"])

                if data["type"] == "mcq":
                    user_answer = st.radio("Select your answer:", data["options"], key="mcq")
                    if st.button("Submit Answer", key="submit_mcq"):
                        correct = data["options"][data["answer"]]
                        if user_answer == correct:
                            st.success("Correct ✅")
                        else:
                            st.error(f"Incorrect ❌. Correct answer: {correct}\nSource: {data['source']}")
                elif data["type"] == "short":
                    user_input = st.text_input("Enter your answer:", key="short")
                    if st.button("Submit Answer", key="submit_short"):
                        if user_input.strip().lower() == data["answer"].lower():
                            st.success("Correct ✅")
                        else:
                            st.error(f"Incorrect ❌. Correct answer: {data['answer']}\nSource: {data['source']}")
            else:
                st.warning("No questions available for this type yet.")
