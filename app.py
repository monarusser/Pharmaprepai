import streamlit as st

# === DATA STRUCTURE ===

TOPICS = {
    "Cardiovascular": {
        "Hypertension": {
            "revision_summary": [
                "First-line drug class for adults under 55 is ACE inhibitors or ARBs.",
                "First-line drug class for Black adults over 55 is Calcium channel blockers.",
                "Lifestyle changes are essential in managing hypertension.",
            ],
            "mcq_drug_class": [
                {
                    "question": "Which drug class is first-line for adults under 55 with hypertension?",
                    "options": ["Calcium channel blockers", "ACE inhibitors", "Beta blockers", "Diuretics"],
                    "answer": 1,
                    "source": "NICE NG136"
                },
            ],
            "mcq_specific_drug": [
                {
                    "question": "Which specific drug is first-line for hypertension in Black adults over 55?",
                    "options": ["Amlodipine", "Lisinopril", "Bisoprolol", "Hydrochlorothiazide"],
                    "answer": 0,
                    "source": "NICE NG136"
                },
            ],
            "short_answer_drug_class": [
                {
                    "question": "Name the first-line drug class for hypertension in adults under 55.",
                    "answer": "ACE inhibitors",
                    "source": "NICE NG136"
                },
            ],
            "short_answer_specific_drug": [
                {
                    "question": "Name the first-line drug for hypertension in Black adults over 55.",
                    "answer": "Amlodipine",
                    "source": "NICE NG136"
                },
            ],
            "calculations": [
                {
                    "question": "Calculate the daily dose if 5mg is taken twice daily for 14 days.",
                    "answer": "10",
                    "working": "5mg x 2 times = 10mg daily",
                    "source": "BNF Chapter 2.4"
                }
            ]
        },
        "Heart Failure": {
            "revision_summary": [
                "ACE inhibitors and beta blockers are first-line treatments.",
                "Spironolactone may be added in advanced cases.",
            ],
            "mcq_drug_class": [
                {
                    "question": "Which drug class is first-line in heart failure management?",
                    "options": ["ACE inhibitors", "Calcium channel blockers", "Beta blockers", "Diuretics"],
                    "answer": 0,
                    "source": "NICE NG106"
                }
            ],
            "mcq_specific_drug": [
                {
                    "question": "Which beta blocker is licensed for heart failure treatment?",
                    "options": ["Atenolol", "Bisoprolol", "Propranolol", "Metoprolol"],
                    "answer": 1,
                    "source": "NICE NG106"
                }
            ],
            "short_answer_drug_class": [
                {
                    "question": "Name the drug class used first-line in heart failure.",
                    "answer": "ACE inhibitors",
                    "source": "NICE NG106"
                }
            ],
            "short_answer_specific_drug": [
                {
                    "question": "Name a beta blocker used in heart failure.",
                    "answer": "Bisoprolol",
                    "source": "NICE NG106"
                }
            ],
            "calculations": []
        }
    },
    "Gastrointestinal": {
        "IBD": {
            "revision_summary": [
                "5-ASA compounds are first-line for mild to moderate ulcerative colitis.",
                "Biologics are used for moderate to severe disease.",
            ],
            "mcq_drug_class": [
                {
                    "question": "Which drug class is first-line for mild ulcerative colitis?",
                    "options": ["Corticosteroids", "5-ASA compounds", "Biologics", "Antibiotics"],
                    "answer": 1,
                    "source": "NICE CG166"
                }
            ],
            "mcq_specific_drug": [
                {
                    "question": "Name a common 5-ASA drug used in ulcerative colitis.",
                    "options": ["Mesalazine", "Prednisolone", "Infliximab", "Azathioprine"],
                    "answer": 0,
                    "source": "NICE CG166"
                }
            ],
            "short_answer_drug_class": [
                {
                    "question": "Name the drug class used first-line in mild ulcerative colitis.",
                    "answer": "5-ASA compounds",
                    "source": "NICE CG166"
                }
            ],
            "short_answer_specific_drug": [
                {
                    "question": "Name a 5-ASA drug used in ulcerative colitis.",
                    "answer": "Mesalazine",
                    "source": "NICE CG166"
                }
            ],
            "calculations": []
        }
    },
    "Central Nervous System": {
        "Epilepsy": {
            "revision_summary": [
                "Sodium valproate is contraindicated in women of childbearing age.",
                "Lamotrigine and carbamazepine are commonly used AEDs.",
            ],
            "mcq_drug_class": [
                {
                    "question": "Which drug class is commonly used as anti-epileptic drugs?",
                    "options": ["Calcium channel blockers", "AEDs", "Beta blockers", "Diuretics"],
                    "answer": 1,
                    "source": "NICE CG137"
                }
            ],
            "mcq_specific_drug": [
                {
                    "question": "Name an anti-epileptic drug used in focal seizures.",
                    "options": ["Carbamazepine", "Propranolol", "Amlodipine", "Ramipril"],
                    "answer": 0,
                    "source": "NICE CG137"
                }
            ],
            "short_answer_drug_class": [
                {
                    "question": "Name a common class of drugs used for epilepsy.",
                    "answer": "Antiepileptic drugs",
                    "source": "NICE CG137"
                }
            ],
            "short_answer_specific_drug": [
                {
                    "question": "Name a drug used for focal seizures.",
                    "answer": "Carbamazepine",
                    "source": "NICE CG137"
                }
            ],
            "calculations": []
        },
        "Parkinson's Disease": {
            "revision_summary": [
                "Levodopa is the most effective treatment.",
                "Dopamine agonists may be used as initial therapy in younger patients.",
            ],
            "mcq_drug_class": [
                {
                    "question": "Which drug class is first-line in Parkinson’s disease?",
                    "options": ["Levodopa", "Dopamine agonists", "MAO-B inhibitors", "Anticholinergics"],
                    "answer": 0,
                    "source": "NICE NG71"
                }
            ],
            "mcq_specific_drug": [
                {
                    "question": "Name the most effective drug for Parkinson’s disease.",
                    "options": ["Levodopa", "Pramipexole", "Selegiline", "Benztropine"],
                    "answer": 0,
                    "source": "NICE NG71"
                }
            ],
            "short_answer_drug_class": [
                {
                    "question": "Name the primary drug used in Parkinson’s disease treatment.",
                    "answer": "Levodopa",
                    "source": "NICE NG71"
                }
            ],
            "short_answer_specific_drug": [
                {
                    "question": "Name the most effective drug for Parkinson’s disease.",
                    "answer": "Levodopa",
                    "source": "NICE NG71"
                }
            ],
            "calculations": []
        }
    }
}

# === APP LOGIC ===

def main():
    st.title("Pharma Prep AI - UK Pharmacy Exam Revision")

    if "page" not in st.session_state:
        st.session_state.page = "home"
        st.session_state.topic = None
        st.session_state.subtopic = None
        st.session_state.question_type = None
        st.session_state.question_index = 0

    if st.session_state.page == "home":
        show_homepage()
    elif st.session_state.page == "topics":
        show_subtopics()
    elif st.session_state.page == "question_type":
        show_question_types()
    elif st.session_state.page == "quiz":
        show_question()
    elif st.session_state.page == "summary":
        show_revision_summary()

def show_homepage():
    st.header("Select a Main Topic")
    for topic in TOPICS.keys():
        if st.button(topic):
            st.session_state.topic = topic
            st.session_state.page = "topics"
            st.session_state.subtopic = None
            st.session_state.question_type = None
            st.session_state.question_index = 0
            st.experimental_rerun()

def show_subtopics():
    st.header(f"Select a Subtopic in {st.session_state.topic}")
    subtopics = TOPICS[st.session_state.topic]
    for sub in subtopics.keys():
        if st.button(sub):
            st.session_state.subtopic = sub
            st.session_state.page = "summary"
            st.session_state.question_type = None
            st.session_state.question_index = 0
            st.experimental_rerun()
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.experimental_rerun()

def show_revision_summary():
    st.header(f"Revision Summary: {st.session_state.subtopic}")
    summary = TOPICS[st.session_state.topic][st.session_state.subtopic].get("revision_summary", [])
    for point in summary:
        st.write(f"- {point}")

    if st.button("Start Questions"):
        st.session_state.page = "question_type"
        st.session_state.question_index = 0
        st.experimental_rerun()
    if st.button("Back to Subtopics"):
        st.session_state.page = "topics"
        st.experimental_rerun()

def show_question_types():
    st.header("Select Question Type")
    question_types = {
        "Multiple Choice - Drug Class": "mcq_drug_class",
        "Multiple Choice - Specific Drug": "mcq_specific_drug",
        "Short Answer - Drug Class": "short_answer_drug_class",
        "Short Answer - Specific Drug": "short_answer_specific_drug",
        "Calculations": "calculations"
    }
    choice = st.radio("Choose question type:", list(question_types.keys()))

    if st.button("Start Quiz"):
        st.session_state.question_type = question_types[choice]
        st.session_state.question_index = 0
        st.session_state.page = "quiz"
        st.experimental_rerun()

    if st.button("Back to Summary"):
        st.session_state.page = "summary"
        st.experimental_rerun()

def show_question():
    topic = st.session_state.topic
    subtopic = st.session_state.subtopic
    qtype = st.session_state.question_type
    idx = st.session_state.question_index

    questions = TOPICS[topic][subtopic].get(qtype, [])
    if not questions:
        st.write("No questions available for this type.")
        if st.button("Back to Question Types"):
            st.session_state.page = "question_type"
            st.experimental_rerun()
        return

    question_data = questions[idx]
    st.header(f"Question {idx + 1} of {len(questions)}")

    st.write(f"**Question:** {question_data['question']}")

    # Different input for MCQ vs Short answer vs Calculation
    if qtype.startswith("mcq"):
        options = question_data["options"]
        choice = st.radio("Select your answer:", options)

        if st.button("Submit"):
            correct_index = question_data["answer"]
            if options.index(choice) == correct_index:
                st.success("Correct! ✅")
            else:
                st.error(f"Incorrect ❌\nCorrect answer: {options[correct_index]}\nSource: {question_data['source']}")
            if st.button("Next Question"):
                if idx + 1 < len(questions):
                    st.session_state.question_index += 1
                    st.experimental_rerun()
                else:
                    st.info("You have completed all questions.")
                    if st.button("Back to Question Types"):
                        st.session_state.page = "question_type"
                        st.experimental_rerun()
            if st.button("Back to Question Types"):
                st.session_state.page = "question_type"
                st.experimental_rerun()

    elif qtype.startswith("short_answer") or qtype == "calculations":
        user_answer = st.text_input("Type your answer here:")

        if st.button("Submit"):
            correct_answer = question_data["answer"].lower().strip()
            if user_answer.lower().strip() == correct_answer:
                st.success("Correct! ✅")
            else:
                st.error(f"Incorrect ❌\nCorrect answer: {question_data['answer']}\nSource: {question_data['source']}")
                if qtype == "calculations" and "working" in question_data:
                    st.write(f"Working out: {question_data['working']}")

            if st.button("Next Question"):
                if idx + 1 < len(questions):
                    st.session_state.question_index += 1
                    st.experimental_rerun()
                else:
                    st.info("You have completed all questions.")
                    if st.button("Back to Question Types"):
                        st.session_state.page = "question_type"
                        st.experimental_rerun()

        if st.button("Back to Question Types"):
            st.session_state.page = "question_type"
            st.experimental_rerun()

if __name__ == "__main__":
    main()


