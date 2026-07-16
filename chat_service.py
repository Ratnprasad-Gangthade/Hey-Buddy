"""Gemini and LangChain functions used by the Streamlit app."""

import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_response(messages, question):
    """Send the current question and previous chat messages to Gemini."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Please add GOOGLE_API_KEY to the .env file.")

    history = []
    for message in messages:
        if message["role"] == "user":
            history.append(HumanMessage(content=message["content"]))
        elif message["role"] == "assistant":
            history.append(AIMessage(content=message["content"]))

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are Hey Buddy, a helpful and friendly Q&A assistant. "
                "Give clear and accurate answers. Use the previous conversation "
                "when it is useful.",
            ),
            MessagesPlaceholder("history"),
            ("human", "{question}"),
        ]
    )

    llm = ChatGoogleGenerativeAI(
        model=os.getenv("MODEL_NAME", "gemini-3.5-flash"),
        google_api_key=api_key,
        temperature=0.4,
    )

    chain = prompt | llm
    response = chain.invoke({"history": history, "question": question})
    return response.text
