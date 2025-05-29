import streamlit as st
import openai
import random

# Set page config
st.set_page_config(page_title="Pharma Prep", page_icon="💊", layout="centered")

# Title and description
st.markdown("""
    <h1 style='text-align: center;'>💊 Pharma Prep</h1>
    <p style='text-align: center;'>UK Pharmacy Exam Revision Tool - Based on NICE & BNF</p>
    <hr>
""", unsafe_allow_html=True)

# Sidebar for settings
st.sidebar.title("Settings")
topic = st.sidebar.selectbox("Choose a topic:", [
    "Cardiovascular", "Musculoskeletal", "Respiratory", "Endocrine",
    "Gastrointestinal", "Infections", "Renal", "Neurology", "Calculations"
])

qtype = st.sidebar.selectbox("Choose question type:", [
    "Short Answer", "Multiple Choice", "Flashcard"
])

# Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Build the dynamic prompt
prompt = f"""
You are a UK pharmacy exam assistant. Create one {qtype.lower()} pharmacy question based on the topic: {topic}.

- Ensure the question is clinically specific and reflects UK practice.
- Use NICE or BNF as the source.
- For example, instead of generic 'What treats hypertension?', say:
  'According to NICE NG136, what is the first-line treatment for hypertension in adults over 55 or of African/Caribbean origin?'
- The answer should be concise (1–2 words for Short Answer).
- At the end, cite the source (e.g. NICE NG136, BNF 2.5)
- Do not include explanations in the answer unless it's a Flashcard.
- For Flashcards, include a brief explanation after the answer.
- Always include this disclaimer:
  'This tool is for revision purposes only and is not affiliated with any official regulatory body.'
"""

# Main app interaction
if st.button("Generate Question"):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful UK pharmacy exam assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )

        content = response.choices[0].message.content

        # Display the question
        st.markdown("### 🧪 Question")
        question, *rest = content.split("Answer:")
        st.markdown(question.strip())

        # Capture user answer
        user_answer = st.text_input("Your Answer:")

        if user_answer and rest:
            correct_answer_section = rest[0].strip()

            # Handle flashcard explanation if present
            if qtype == "Flashcard" and "Explanation:" in correct_answer_section:
                correct_answer, explanation = correct_answer_section.split("Explanation:")
            else:
                correct_answer, explanation = correct_answer_section, ""

            correct_answer = correct_answer.split("Source:")[0].strip()
            source = correct_answer_section.split("Source:")[-1].strip()

            # Display feedback
            st.markdown("### ✅ Feedback")
            if user_answer.lower().strip() == correct_answer.lower():
                st.success("Correct! ✅")
            else:
                st.error(f"Incorrect. ❌ The correct answer is: **{correct_answer}**")

            if explanation:
                st.markdown(f"**Explanation:** {explanation.strip()}")

            st.markdown(f"**Source:** 📘 {source}")
            st.markdown("---")
            st.markdown(
                "<small>This tool is for revision purposes only and is not affiliated with any official regulatory body.</small>",
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")
