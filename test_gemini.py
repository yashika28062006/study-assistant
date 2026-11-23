
from getpass import getpass
from langchain_google_genai import ChatGoogleGenerativeAI

api_key = getpass("Paste your Gemini API key: ")

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=api_key,
        temperature=0.3
    )

    response = llm.invoke("Say hello in one sentence.")
    print("\nSUCCESS!")
    print(response.content)

except Exception as e:
    print("\nFAILED!")
    print("Error type:", type(e).__name__)
    print("Full error:", str(e))

