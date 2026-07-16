"""Streamlit user interface for Hey Buddy."""

import streamlit as st

from chat_service import get_response


st.set_page_config(page_title="Hey Buddy")
st.title("Hey Buddy")
st.caption("A multi-turn Q&A assistant powered by LangChain and Google Gemini.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask me anything")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = get_response(st.session_state.messages[:-1], question)
            except ValueError as error:
                st.error(error)
            except Exception:
                st.error("Sorry, I could not reach the assistant. Please try again.")
            else:
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
