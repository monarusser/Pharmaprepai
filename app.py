import openai
import streamlit as st

# Load your OpenAI key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit interface
st.title("🔧 OpenAI Test")
st.write("Click the button to test OpenAI is working:")

if st.button("Test OpenAI"):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "What is the capital of the UK?"}]
        )
        st.success("✅ OpenAI responded!")
        st.write("Answer:", response.choices[0].message.content)
    except Exception as e:
        st.error(f"❌ Error: {e}")

