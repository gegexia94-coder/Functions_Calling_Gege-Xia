import json
import os
from datetime import datetime

import chainlit as cl
from dotenv import load_dotenv
from openai import OpenAI

from design_assistant.tools import (
    DesignServiceTool,
    MaterialSuggestionTool,
    ConsultationBookingTool,
)

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

service_tool = DesignServiceTool()
material_tool = MaterialSuggestionTool()
booking_tool = ConsultationBookingTool()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_design_service_info",
            "description": "Ottiene informazioni su una consulenza per una stanza.",
            "parameters": {
                "type": "object",
                "properties": {
                    "room_type": {
                        "type": "string",
                        "description": "Tipo di stanza: camera, soggiorno o cucina",
                    }
                },
                "required": ["room_type"],
            },
        },
    },
]

TOOLS.append({
    "type": "function",
    "function": {
        "name": "suggest_materials",
        "description": "Suggerisce materiali in base allo stile di interior design.",
        "parameters": {
            "type": "object",
            "properties": {
                "style": {
                    "type": "string",
                    "description": "Stile richiesto: japandi, moderno caldo o minimal",
                }
            },
            "required": ["style"],
        },
    },
})

TOOLS.append({
    "type": "function",
    "function": {
        "name": "book_consultation",
        "description": "Prenota una consulenza con un designer.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Data formato YYYY-MM-DD"},
                "time": {"type": "string", "description": "Ora formato HH:MM"},
                "designer_id": {"type": "string", "description": "ID designer opzionale"},
            },
            "required": ["date", "time"],
        },
    },
})

def handle_tool_call(tool_call) -> str:
    args = json.loads(tool_call.function.arguments)
    name = tool_call.function.name

    print("FUNCTION NAME:", name)
    print("FUNCTION ARGS:", args)

    if name == "get_design_service_info":
        return service_tool.get_service_info(**args)

    if name == "suggest_materials":
        return material_tool.suggest_materials(**args)

    if name == "book_consultation":
        return booking_tool.book_consultation(**args)

    return "Tool non riconosciuto."

def ask_llm(messages):
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

@cl.on_chat_start
def on_chat_start():
    today = datetime.today().strftime("%Y-%m-%d")

    cl.user_session.set("messages", [
        {
            "role": "developer",
            "content": (
                "Sei un assistente per consulenze di interior design. "
                f"Oggi è il {today}. "
                "Usa i tool quando servono dati su servizi, materiali o prenotazioni."
            ),
        }
    ])

@cl.on_message
async def main(message: cl.Message):
    messages = cl.user_session.get("messages")
    messages.append({"role": "user", "content": message.content})

    while True:
        completion = ask_llm(messages)
        response_message = completion.choices[0].message

        if response_message.content:
            messages.append(response_message)
            break

        tool_calls = response_message.tool_calls

        if tool_calls:
            messages.append(response_message)

            for tool_call in tool_calls:
                result = handle_tool_call(tool_call)

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": result,
                })

    cl.user_session.set("messages", messages)

    await cl.Message(
        author="Design Assistant",
        content=messages[-1].content,
    ).send()
