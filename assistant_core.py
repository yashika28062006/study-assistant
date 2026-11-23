
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage
)
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import TOOLS


CHAT_MODEL = "gemini-3.8-flash"

MAX_HISTORY = 10
MAX_STEPS = 4


SYSTEM_PROMPT = """
You are Study Planner Assistant, a helpful AI assistant
designed for students preparing for exams.

Your main responsibilities are:

1. Help students create realistic study plans.
2. Calculate the number of days remaining until an exam.
3. Divide available study hours between subjects.
4. Give simple and practical study suggestions.
5. Remember details shared earlier in the conversation.

Rules:

- Use available tools whenever calculations or date
  information are needed.
- Never guess dates or calculation results.
- Ask for missing information before making a study plan.
- Keep answers clear, friendly and easy to understand.
- Give practical suggestions that students can follow.
- Remember information shared earlier in the conversation.
- If a question is unrelated to studying or exam preparation,
  politely explain that it is outside your purpose.
- If you cannot complete a request, honestly explain why.
"""


def make_llm(api_key):
    return ChatGoogleGenerativeAI(
        model=CHAT_MODEL,
        temperature=0.3,
        google_api_key=api_key
    )


def text_of(content):
    """Convert Gemini response content into readable text."""

    if isinstance(content, str):
        return content

    return "".join(
        p.get("text", "") if isinstance(p, dict) else str(p)
        for p in content
    )


def run_turn(llm, history, question, system_prompt=SYSTEM_PROMPT):
    """Answer one question using conversation memory and available tools."""

    by_name = {t.name: t for t in TOOLS}

    llm_with_tools = llm.bind_tools(TOOLS)

    messages = (
        [SystemMessage(content=system_prompt)]
        + history[-MAX_HISTORY:]
        + [HumanMessage(content=question)]
    )

    used = []
    answer = ""

    for _ in range(MAX_STEPS):

        ai = llm_with_tools.invoke(messages)

        messages.append(ai)

        if not ai.tool_calls:
            answer = text_of(ai.content)
            break

        for call in ai.tool_calls:

            tool = by_name.get(call["name"])

            if tool is None:
                result = ToolMessage(
                    content="No such tool.",
                    tool_call_id=call["id"],
                    name=call["name"]
                )

            else:
                try:
                    result = tool.invoke(call)

                except Exception as e:
                    result = ToolMessage(
                        content=f"Tool error: {e}",
                        tool_call_id=call["id"],
                        name=call["name"]
                    )

            used.append({
                "tool": call["name"],
                "args": call["args"],
                "result": str(result.content)
            })

            messages.append(result)

    if not answer:
        answer = (
            "I could not finish that request. "
            "Please try asking in a simpler way."
        )

    new_history = (
        history + [
            HumanMessage(content=question),
            AIMessage(content=answer)
        ]
    )[-MAX_HISTORY:]

    return answer, used, new_history
