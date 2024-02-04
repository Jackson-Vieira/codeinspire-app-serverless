import logging
import asyncio

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_secret():
    return "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"


OPENAI_API_KEY = get_secret()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

PROMPT_SYSTEM = """
Act as a programming language tip expert generator for curios peoples
"""

PROMPT_USER_TEMPLATE = """
Generate a daily tip for the following programming language, return a JSON. 
The tip should be concise and practical, focusing on a specific concept or feature of the language.

JSON expected keys: key_tip, description and code_example

include all necessary imports   the example and use code best practices.
"""


async def generate_tip(language: str):
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        frequency_penalty=0.2,
        presence_penalty=0.2,
        temperature=0.5,
        top_p=0.5,
        max_tokens=1200,
        stop=None,
        messages=[
            {
                "role": "system",
                "content": PROMPT_SYSTEM,
            },
            {"role": "user", "content": PROMPT_USER_TEMPLATE + language},
        ],
    )
    result = response.choices[0].message.content
    logger.info(f"Tip Result: {result}")
    return result


async def generate_tips():
    results = await asyncio.gather(generate_tip("Python"))
    logger.info(f"Tip Results {results}")


def run(event, context):
    asyncio.run(generate_tips())
