import streamlit as st
import openai
import os

st.set_page_config(page_title="PharmaPrep AI", page_icon="💊")

st.title("PharmaPrep AI - Pharmacy Exam Assistant")

# Get OpenAI API key from Streamlit secrets
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    openai.api_key = api_key

    q_type = st.selectbox(
        "Select question type",
        ["Flashcard", "Multiple Choice", "Short Answer", "Calculation"]
    )

    if st.button("Generate Question"):
        prompt = (
            f"Create a {q_type} pharmacy exam question with a one or two-word answer. "
            "Provide the question, the correct answer, and cite the guideline source "
            "(e.g., NICE NG30 or BNF chapter). Include a short disclaimer about this being a revision aid."
        )

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful pharmacy exam assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7,
            )

            answer = response.choices[0].message.content
            st.markdown("### Question & Answer")
            st.write(answer)

            st.markdown("---")
            st.markdown(
                "**Disclaimer:** This app is a revision aid only and is not regulated by any healthcare authority. "
                "Always verify information using official sources."
            )
        except Exception as e:
            st.error(f"Error: {e}")

else:
    st.warning("API key not found. Please add your OpenAI API key to Streamlit secrets.")
