import os
import asyncio
import boto3
import json

from datetime import date
from openai import AsyncOpenAI, OpenAIError
from botocore.exceptions import ClientError

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


PROMPT_SYSTEM = """
You are a professional and creative programming code tip generator. You always return just the JSON
with no addiotional description or context.
"""


PROMPT_USER_TEMPLATE = """
Generate a tip for the following programming language
The tip must be useful or related to some daily task of a common programmer.

Please give the response in a proper JSON format

Here is a template JSON output:
{"key": "key of tip", "code": "def hello_world():\n    print('Hello, world!')\n\nhello_world()", "description": "tip description"}

input: 
"""


def put_tip(language: str, tip: dict):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE_NAME"])

    response = None
    try:
        response = table.put_item(
            Item={
                "tip_language": language,
                "tip_date": str(date.today()), 
                "tip": tip
            }
        )
    except ClientError as e:
        print(e.response["Error"]["Message"])

    return response


def get_openai_client():
    return AsyncOpenAI(api_key=OPENAI_API_KEY)


async def generate_tip(language: str):
    client = get_openai_client()

    result = None
    try:
        response = await client.chat.completions.create(
            # TODO: change this to gpt-3.5-turbo only and learn how to handle JSON.
            model="gpt-3.5-turbo-1106",
            response_format={"type":"json_object"},
            frequency_penalty=0.2,
            presence_penalty=0.2,
            temperature=0.5,
            top_p=0.5,
            max_tokens=1200,
            timeout=15,
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
        print("result", json.loads(result))
    except OpenAIError as e:
        print(f"Error: {e}")
        return None
    finally:
        await client.close()
    return language, json.loads(result)


async def generate_tips(langs: list):
    return await asyncio.gather(*[generate_tip(lang) for lang in langs])


def insert_tips(tips):
    for language, tip in tips:
        put_tip(language, tip)


def run(event, context):
    langs = ["Python", "Javascript"]
    tips = asyncio.run(generate_tips(langs))
    insert_tips(tips)
