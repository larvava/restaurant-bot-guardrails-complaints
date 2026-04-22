import streamlit as st
from agents import (
    Agent,
    RunContextWrapper,
    handoff,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.extensions import handoff_filters
from models import HandoffData
from input_guardrails import restaurant_input_guardrail
from my_agents.menu_agent import menu_agent
from my_agents.order_agent import order_agent
from my_agents.reservation_agent import reservation_agent
from my_agents.complaints_agent import complaints_agent


def handle_handoff(
    wrapper: RunContextWrapper,
    input_data: HandoffData,
):
    with st.sidebar:
        st.write(
            f"""
            Handing off to {input_data.to_agent_name}
            Reason: {input_data.reason}
            Issue Type: {input_data.issue_type}
            Description: {input_data.issue_description}
            """
        )


def make_handoff(agent):
    return handoff(
        agent=agent,
        on_handoff=handle_handoff,
        input_type=HandoffData,
        input_filter=handoff_filters.remove_all_tools,
    )


triage_agent = Agent(
    name="Triage Agent",
    instructions=f"""
    {RECOMMENDED_PROMPT_PREFIX}

    You are the front desk greeter at our restaurant.

    YOUR ROLE: Understand what the customer needs and connect them to the right specialist.

    ROUTING RULES:
    - Menu questions (dishes, ingredients, allergies, dietary options) -> Menu Agent
    - Ordering food or drinks -> Order Agent
    - Table reservations (booking, changing, canceling) -> Reservation Agent
    - Complaints, dissatisfaction, bad experiences -> Complaints Agent

    BEHAVIOR:
    - Greet the customer warmly
    - Quickly identify their need
    - Hand off to the appropriate agent with a brief explanation
    - If unclear, ask a clarifying question before routing
    - Do NOT try to answer menu, order, reservation, or complaint questions yourself
    """,
    input_guardrails=[restaurant_input_guardrail],
    handoffs=[
        make_handoff(menu_agent),
        make_handoff(order_agent),
        make_handoff(reservation_agent),
        make_handoff(complaints_agent),
    ],
)
