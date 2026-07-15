from dotenv import load_dotenv 
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash")

while True:
    query=input("user: ")

    if query.lower() in ["Quit","exit","bye"]:
        print("GoodBye 👋")
        break

    res=llm.invoke(query)
    print("AI: ",res.content, "\n")

