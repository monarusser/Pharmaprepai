import streamlit as st
import openai
import os

# Load OpenAI API key from secrets or environment
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# Data structure for topics, subtopics, and sample questions
TOPICS = {
    "Cardiovascular": {
        "Hypertension": [
            {
                "question": "What is the first-line antihypertensive for a Black adult over 55?",
                "answer": "Calcium channel blockers",
                "source": "NICE NG136",
                "type": "short_answer"
            },
            {
                "question": "Which drug is NOT a first-line antihypertensive?",
                "options": ["Amlodipine", "Lisinopril", "Propranolol", "Thiazide diuretics"],
                "answer": "Propranolol",
                "source": "BNF Chapter 2.5",
                "type": "mcq"
            }
        ],
        "Heart Failure": [
            # Add questions here
        ]
    },
    "Central Nervous System": {
        "Epilepsy": [
            {
                "question": "What is the first-line treatment for newly diagnosed focal epilepsy?",
                "answer": "Lamotrigine",
                "source": "NICE NG217",
                "type": "short_answer"
            }
        ],
        "Parkinson's Disease": [
            # Add questions here
        ],
        "Dementia": [
            # Add questions here
        ]
    },
    # Add more main topics and subtopics...
}

def show_homepage():
    st.title("Pharma Prep: UK Pharmacy Exam Revision")
    st.markdown("""
    Welcome! Select a topic to start revising based strictly on UK guidelines (NICE, BNF, MHRA).
    """)

    topic = st.selectbox("Select a Topic", list(TOPICS.keys()))
    if topic:
        st.session_state['selected_topic'] = topic
        st.session_state['page'] = "subtopic"

def show_subtopic_page():
    topic = st.session_state.get('selected_topic')
    st.header(f"Topic: {topic}")
    subtopics = list(TOPICS[topic].keys())
    subtopic = st.selectbox("Select a Subtopic", subtopics)
    if subtopic:
        st.session_state['selected_subtopic'] = subtopic
        st.session_state['page'] = "quiz"

    if st.button("Back to Topics"):
        st.session_state['page'] = "home"

def ask_openai(prompt):
    """Call OpenAI chat completion for detailed explanations (optional)."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error with OpenAI API: {e}"

def show_quiz():
    topic = st.session_state.get('selected_topic')
    subtopic = st.session_state.get('selected_subtopic')

    st.header(f"Quiz: {topic} → {subtopic}")

    questions = TOPICS[topic][subtopic]
    if 'current_q' not in st.session_state:
        st.session_state['current_q'] = 0
        st.session_state['score'] = 0

    q_idx = st.session_state['current_q']
    if q_idx >= len(questions):
        st.success(f"Quiz completed! Your score: {st.session_state['score']} / {len(questions)}")
        if st.button("Restart Quiz"):
            st.session_state['current_q'] = 0
            st.session_state['score'] = 0
        if st.button("Back to Subtopics"):
            st.session_state['page'] = "subtopic"
        return

    data = questions[q_idx]

    st.markdown(f"**Question {q_idx + 1}:**")
    st.markdown(data['question'])

    user_answer = None

    if data['type'] == "mcq":
        options = data['options']
        user_answer = st.radio("Select your answer:", options)
    elif data['type'] == "short_answer":
        user_answer = st.text_input("Type your answer here:")

    if st.button("Submit Answer"):
        correct_answer = data['answer'].lower().strip()
        if user_answer is None or user_answer.strip() == "":
            st.warning("Please enter or select an answer.")
            return

        if user_answer.lower().strip() == correct_answer:
            st.success(f"Correct! 🎉\n\nSource: {data['source']}")
            st.session_state['score'] += 1
        else:
            st.error(f"Incorrect. ❌ The correct answer is: **{data['answer']}**\n\nSource: {data['source']}")

        if st.button("Next Question"):
            st.session_state['current_q'] += 1
            st.experimental_rerun()

    if st.button("Back to Subtopics"):
        st.session_state['page'] = "subtopic"
        st.experimental_rerun()

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = "home"

    if st.session_state['page'] == "home":
        show_homepage()
    elif st.session_state['page'] == "subtopic":
        show_subtopic_page()
    elif st.session_state['page'] == "quiz":
        show_quiz()

    # Disclaimer footer
    st.markdown("---")
    st.markdown(
        "⚠️ **Disclaimer:** This app is not regulated by the GPhC or any regulatory body. It is a revision aid only, based on UK guidelines like NICE and BNF."
    )


if __name__ == "__main__":
    main()


       

