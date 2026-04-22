from agents import (
    Agent,
    input_guardrail,
    Runner,
    RunContextWrapper,
    GuardrailFunctionOutput,
)
from models import InputGuardRailOutput


input_guardrail_agent = Agent(
    name="Input Guardrail Agent",
    instructions="""
    Check whether the user's message is appropriate for a restaurant chatbot.

    Return is_off_topic=true if the message is NOT related to the restaurant
    (menu, ingredients, allergies, ordering, reservations, complaints about dining experience, general greetings).

    Return is_inappropriate=true if the message contains profanity, hate speech, harassment, or sexually explicit language.

    You may allow small talk and greetings at the beginning of the conversation.
    """,
    output_type=InputGuardRailOutput,
)


@input_guardrail
async def restaurant_input_guardrail(
    wrapper: RunContextWrapper,
    agent: Agent,
    input: str,
):
    result = await Runner.run(
        input_guardrail_agent,
        input,
    )

    validation = result.final_output

    triggered = validation.is_off_topic or validation.is_inappropriate

    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered,
    )
