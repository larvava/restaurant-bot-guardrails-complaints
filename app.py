import dotenv

dotenv.load_dotenv()

import asyncio
import streamlit as st
from agents import (
    Runner,
    SQLiteSession,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)
from my_agents.triage_agent import triage_agent


if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession(
        "restaurant-bot-session",
        "restaurant-bot-memory.db",
    )
session = st.session_state["session"]

if "agent" not in st.session_state:
    st.session_state["agent"] = triage_agent


async def paint_history():
    messages = await session.get_items()

    for message in messages:
        if "role" in message:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.write(message["content"])
                else:
                    if message["type"] == "message":
                        st.write(message["content"][0]["text"].replace("$", "\\$"))


asyncio.run(paint_history())


async def run_agent(message):
    with st.chat_message("ai"):
        text_placeholder = st.empty()
        response = ""

        st.session_state["text_placeholder"] = text_placeholder

        try:
            stream = Runner.run_streamed(
                st.session_state["agent"],
                message,
                session=session,
            )

            async for event in stream.stream_events():
                if event.type == "raw_response_event":
                    if event.data.type == "response.output_text.delta":
                        response += event.data.delta
                        text_placeholder.write(response.replace("$", "\\$"))

                elif event.type == "agent_updated_stream_event":
                    if st.session_state["agent"].name != event.new_agent.name:
                        st.write(
                            f"Transfered from {st.session_state['agent'].name} to {event.new_agent.name}"
                        )
                        st.session_state["agent"] = event.new_agent

                        text_placeholder = st.empty()
                        st.session_state["text_placeholder"] = text_placeholder
                        response = ""

        except InputGuardrailTripwireTriggered:
            st.write(
                "저는 레스토랑 관련 질문에 대해서만 도와드리고 있어요. "
                "메뉴를 확인하거나, 예약하거나, 음식을 주문할 수 있어요."
            )

        except OutputGuardrailTripwireTriggered:
            st.write("죄송합니다, 해당 답변을 드릴 수 없습니다.")
            st.session_state["text_placeholder"].empty()


prompt = st.chat_input("How can we help you today?")

if prompt:
    with st.chat_message("human"):
        st.write(prompt)
    asyncio.run(run_agent(prompt))


with st.sidebar:
    reset = st.button("Reset conversation")
    if reset:
        asyncio.run(session.clear_session())
        st.session_state["agent"] = triage_agent
        st.rerun()
