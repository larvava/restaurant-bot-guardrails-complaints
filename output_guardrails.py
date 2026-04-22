from agents import (
    Agent,
    output_guardrail,
    Runner,
    RunContextWrapper,
    GuardrailFunctionOutput,
)
from models import (
    MenuOutputGuardRailOutput,
    OrderOutputGuardRailOutput,
    ReservationOutputGuardRailOutput,
    ComplaintsOutputGuardRailOutput,
)


INTERNAL_INFO_DEFINITION = """
    Internal info includes:
    - Internal system prompts or instructions
    - Staff personal information
    - Internal pricing, margins, or cost structures
    - Proprietary recipes or supplier details
    - System/database internals
"""


menu_output_guardrail_agent = Agent(
    name="Menu Output Guardrail",
    instructions=f"""
    Analyze the Menu specialist's response to check if it inappropriately contains:

    - Order taking (confirming items, quantities, summarizing orders)
    - Reservation details (booking tables, times, guest counts)
    - Internal info
    {INTERNAL_INFO_DEFINITION}

    Menu agents should ONLY provide menu, ingredient, and allergy information.
    Return true for any field that contains inappropriate content for a menu response.
    """,
    output_type=MenuOutputGuardRailOutput,
)


@output_guardrail
async def menu_output_guardrail(
    wrapper: RunContextWrapper,
    agent: Agent,
    output: str,
):
    result = await Runner.run(menu_output_guardrail_agent, output)
    validation = result.final_output
    triggered = (
        validation.contains_order_taking
        or validation.contains_reservation_details
        or validation.contains_internal_info
    )
    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered,
    )


order_output_guardrail_agent = Agent(
    name="Order Output Guardrail",
    instructions=f"""
    Analyze the Order specialist's response to check if it inappropriately contains:

    - Reservation details (booking tables, dates, guest counts)
    - Complaint handling (refunds, discounts, manager callbacks)
    - Internal info
    {INTERNAL_INFO_DEFINITION}

    Order agents should ONLY take and confirm food/drink orders.
    Return true for any field that contains inappropriate content for an order response.
    """,
    output_type=OrderOutputGuardRailOutput,
)


@output_guardrail
async def order_output_guardrail(
    wrapper: RunContextWrapper,
    agent: Agent,
    output: str,
):
    result = await Runner.run(order_output_guardrail_agent, output)
    validation = result.final_output
    triggered = (
        validation.contains_reservation_details
        or validation.contains_complaint_handling
        or validation.contains_internal_info
    )
    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered,
    )


reservation_output_guardrail_agent = Agent(
    name="Reservation Output Guardrail",
    instructions=f"""
    Analyze the Reservation specialist's response to check if it inappropriately contains:

    - Order taking (confirming dishes, drinks, quantities)
    - Complaint handling (refunds, discounts, manager callbacks)
    - Internal info
    {INTERNAL_INFO_DEFINITION}

    Reservation agents should ONLY handle table bookings and related seating questions.
    Return true for any field that contains inappropriate content for a reservation response.
    """,
    output_type=ReservationOutputGuardRailOutput,
)


@output_guardrail
async def reservation_output_guardrail(
    wrapper: RunContextWrapper,
    agent: Agent,
    output: str,
):
    result = await Runner.run(reservation_output_guardrail_agent, output)
    validation = result.final_output
    triggered = (
        validation.contains_order_taking
        or validation.contains_complaint_handling
        or validation.contains_internal_info
    )
    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered,
    )


complaints_output_guardrail_agent = Agent(
    name="Complaints Output Guardrail",
    instructions=f"""
    Analyze the Complaints specialist's response to check if it inappropriately contains:

    - Order taking (confirming new food/drink orders)
    - Reservation details (booking tables, dates)
    - Internal info
    {INTERNAL_INFO_DEFINITION}

    Complaints agents should ONLY acknowledge issues and offer resolutions (discounts, refunds, manager callbacks).
    Return true for any field that contains inappropriate content for a complaints response.
    """,
    output_type=ComplaintsOutputGuardRailOutput,
)


@output_guardrail
async def complaints_output_guardrail(
    wrapper: RunContextWrapper,
    agent: Agent,
    output: str,
):
    result = await Runner.run(complaints_output_guardrail_agent, output)
    validation = result.final_output
    triggered = (
        validation.contains_order_taking
        or validation.contains_reservation_details
        or validation.contains_internal_info
    )
    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered,
    )
