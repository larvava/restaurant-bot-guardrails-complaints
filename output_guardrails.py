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


REFERRAL_RULE = """
    IMPORTANT: Briefly acknowledging an out-of-scope request and offering to
    redirect the customer to the appropriate specialist is ALLOWED and should
    NOT be flagged. Only flag responses where the agent actually performs the
    out-of-scope task (e.g., confirming an order with items and totals,
    booking a specific table/time, issuing a refund or discount).
"""


menu_output_guardrail_agent = Agent(
    name="Menu Output Guardrail",
    instructions=f"""
    Analyze the Menu specialist's response to check if it inappropriately contains:

    - Order taking (actually confirming items, quantities, summarizing or finalizing orders)
    - Reservation details (actually booking a specific table, time, or guest count)
    - Internal info
    {INTERNAL_INFO_DEFINITION}
    {REFERRAL_RULE}

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

    - Reservation details (actually booking a specific table, date, or guest count)
    - Complaint handling (actually issuing refunds, discounts, or scheduling manager callbacks)
    - Internal info
    {INTERNAL_INFO_DEFINITION}
    {REFERRAL_RULE}

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

    - Order taking (actually confirming dishes, drinks, or quantities)
    - Complaint handling (actually issuing refunds, discounts, or scheduling manager callbacks)
    - Internal info
    {INTERNAL_INFO_DEFINITION}
    {REFERRAL_RULE}

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

    - Order taking (actually confirming new food/drink orders)
    - Reservation details (actually booking a specific table or date)
    - Internal info
    {INTERNAL_INFO_DEFINITION}
    {REFERRAL_RULE}

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
