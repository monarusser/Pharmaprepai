import streamlit as st
import openai
import os

openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

TOPICS = {
    "Cardiovascular": {
        "Hypertension": {
            "revision_summary": [
                "First-line drug class for adults under 55 is ACE inhibitors.",
                "First-line drug class for Black adults over 55 is Calcium channel blockers.",
                "Common first-line drugs include Lisinopril and Amlodipine.",
                "Always consider patient demographics as per NICE NG136 guidelines."
            ],
            "mcq_drug_class": [
                {
                    "question": "Which drug class is the first-line antihypertensive for a Black adult over 55?",
                    "options": ["Calcium channel blockers", "ACE inhibitors", "Beta blockers", "Diuretics"],
                    "answer": "Calcium channel blockers",
                    "source": "NICE NG136"
                }
            ],
            "mcq_specific_drug": [
                {
                    "question": "Which drug is the first-line antihypertensive for a Black adult over 55?",
                    "options": ["Amlodipine", "Lisinopril", "Propranolol", "Hydrochlorothiazide"],
                    "answer": "Amlodipine",
                    "source": "NICE NG136"
                }
            ],
            "short_answer_drug_class": [
                {
                    "question": "Name the first-line drug class used to treat hypertension in adults under 55.",
                    "answer": "ACE inhibitors",
                    "source": "NICE NG136"
                }
            ],
            "short_answer_specific_drug": [
                {
                    "question": "Name a first-line ACE inhibitor used for hypertension.",
                    "answer": "Lisinopril",
                    "source": "BNF Chapter 2.5"
                }
            ]
        }
        # add more subtopics...
    },
    # add more topics...
}

def reset_quiz_state():
    st.session_state['current_question_idx'] = 0
    st.session_state['score'] = 0

def show_home():
    st.title("Pharma Prep AI - UK Pharmacy Exam Revision")
    st.markdown(
        "Welcome! Please select a main topic to start revising. All questions are based on UK guidelines (NICE, BNF, MHRA)."
    )
    topic = st.selectbox("Choose a Main Topic:", options=list(TOPICS.keys()))
    if topic:
        st.session_state['selected_topic'] = topic
        st.session_state['page'] = 'subtopic'
        reset_quiz_state()

def show_subtopic():
    topic = st.session_state.get('selected_topic')
    st.header(f"Topic: {topic}")
    subtopics = list(TOPICS[topic].keys())
    subtopic = st.selectbox("Choose a Subtopic:", options=subtopics)
    if subtopic:
        st.session_state['selected_subtopic'] = subtopic
        st.session_state['page'] = 'revision_summary'
        reset_quiz_state()

    if st.button("Back to Topics"):
        st.session_state['page'] = 'home'

def show_revision_summary():
    topic = st.session_state.get('selected_topic')
    subtopic = st.session_state.get('selected_subtopic')

    st.header(f"Revision Summary for {subtopic}")
    summary = TOPICS[topic][subtopic].get('revision_summary', ["No summary available."])
    for point in summary:
        st.markdown(f"- {point}")

    if st.button("Start Quiz"):
        st.session_state['page'] = 'question_type'

    if st.button("Back to Subtopics"):
        st.session_state['page'] = 'subtopic'

def show_question_type():
    topic = st.session_state.get('selected_topic')
    subtopic = st.session_state.get('selected_subtopic')
    st.header(f"Topic: {topic} → {subtopic}")

    # Show only keys that are question types (exclude revision_summary)
    question_types = [k for k in TOPICS[topic][subtopic].keys() if k != 'revision_summary']
    q_type = st.selectbox("Select Question Type:", options=question_types)

    if q_type:
        st.session_state['selected_qtype'] = q_type
        st.session_state['page'] = 'quiz'
        reset_quiz_state()

    if st.button("Back to Revision Summary"):
        st.session_state['page'] = 'revision_summary'

def show_quiz():
    topic = st.session_state.get('selected_topic')
    subtopic = st.session_state.get('selected_subtopic')
    qtype = st.session_state.get('selected_qtype')
    st.header(f"Quiz - {topic} → {subtopic} → {qtype}")

    questions = TOPICS[topic][subtopic][qtype]
    if not questions:
        st.info("No questions available for this selection yet.")
        if st.button("Back to Question Type"):
            st.session_state['page'] = 'question_type'
        return

    idx = st.session_state.get('current_question_idx', 0)
    question_data = questions[idx]

    st.markdown(f"**Question {idx + 1} of {len(questions)}:**")
    st.markdown(question_data['question'])

    user_answer = None

    if 'mcq' in qtype:
        user_answer = st.radio("Select your answer:", question_data['options'])
    else:
        user_answer = st.text_input("Type your answer:")

    if st.button("Submit Answer"):
        if not user_answer:
            st.warning("Please answer the question before submitting.")
            return

        correct_answer = question_data['answer'].strip().lower()
        if user_answer.strip().lower() == correct_answer:
            st.success(f"Correct! 🎉\nSource: {question_data['source']}")
            st.session_state['score'] = st.session_state.get('score', 0) + 1
        else:
            st.error(f"Incorrect. ❌ Correct answer: **{question_data['answer']}**\nSource: {question_data['source']}")

        if idx + 1 < len(questions):
            if st.button("Next Question"):
                st.session_state['current_question_idx'] = idx + 1
                st.experimental_rerun()
        else:
            st.success(f"Quiz complete! Your score: {st.session_state.get('score',0)} / {len(questions)}")
            if st.button("Restart Quiz"):
                reset_quiz_state()
                st.experimental_rerun()
            if st.button("Back to Question Type"):
                st.session_state['page'] = 'question_type'
                st.experimental_rerun()

    if st.button("Back to Question Type"):
        st.session_state['page'] = 'question_type'
        st.experimental_rerun()

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'

    page = st.session_state['page']

    if page == 'home':
        show_home()
    elif page == 'subtopic':
        show_subtopic()
    elif page == 'revision_summary':
        show_revision_summary()
    elif page == 'question_type':
        show_question_type()
    elif page == 'quiz':
        show_quiz()

    # Disclaimer
    st.markdown("---")
    st.markdown(
        "⚠️ **Disclaimer:** This app is not regulated by the GPhC or any regulatory body. It is a revision aid only, based on UK guidelines like NICE and BNF."
    )

if __name__ == "__main__":
    main()

