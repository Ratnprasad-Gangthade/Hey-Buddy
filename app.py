from dotenv import load_dotenv 
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash")

response=llm.invoke("what is self attention")
print(response.content)