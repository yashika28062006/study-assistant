
import streamlit as st
import assistant_core

st.set_page_config(
    page_title="Study Planner Assistant",
    page_icon="📚"
)

st.title("📚 Study Planner Assistant")
st.caption("Your personal AI study planner. Bring your own Gemini API key.")

api_key = st.sidebar.text_input(
    "Your Gemini API key",
    type="password",
    help="Get a free key at aistudio.google.com."
)

if st.sidebar.button("Clear chat"):
    st.session_state.pop("chat", None)
    st.session_state.pop("history", None)

if not api_key:
    st.info("Paste your Gemini API key in the sidebar to start.")
    st.stop()

if "chat" not in st.session_state:
    st.session_state.chat = []
    st.session_state.history = []

for role, message, used in st.session_state.chat:
    with st.chat_message(role):
        st.write(message)

        if used:
            with st.expander("Tools used"):
                for item in used:
                    st.markdown(f"**{item['tool']}**")
                    st.caption(f"Result: {item['result'][:300]}")

question = st.chat_input("Ask your study planner...")

if question:
    st.session_state.chat.append(("user", question, None))

    try:
        llm = assistant_core.make_llm(api_key)

        answer, used, st.session_state.history = (
            assistant_core.run_turn(
                llm,
                st.session_state.history,
                question
            )
        )

    except Exception as e:
        answer = (
            f"Something went wrong ({type(e).__name__}). "
            "Check your key and try again."
        )
        used = []

    st.session_state.chat.append(("assistant", answer, used))
    st.rerun()
