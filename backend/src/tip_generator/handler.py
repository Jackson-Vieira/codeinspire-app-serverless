import os
import asyncio
import boto3

from datetime import date
from openai import AsyncOpenAI, OpenAIError

from botocore.exceptions import ClientError

import time

def get_secret():
    return "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"

OPENAI_API_KEY = get_secret()

PROMPT_SYSTEM = """
Act as a programming language tip expert generator for curios peoples
"""

PROMPT_USER_TEMPLATE = """
Generate a daily tip for the following programming language, return a JSON. 
The tip should be concise and practical, focusing on a specific concept or feature of the language.

JSON expected keys: key_tip, description and code_example

include all necessary imports   the example and use code best practices.
"""

def put_tip(language, tip):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_NAME'])
    try:
        response = table.put_item(
            Item={
                'tip_language': language,
                'tip_date': str(date.today()),
                'tip': tip
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    return response

async def generate_tip(language: str):
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    result = None
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
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
        result = response.choices[0].message.content.strip()
    except OpenAIError as e:
        print(f"Error: {e}")
        return None
    finally:
        await client.close()
    return language, result

async def generate_tips():
    return await asyncio.gather(generate_tip("Python"), generate_tip("Javascript"), generate_tip("Go"))

def run(event, context):
    start_time = time.time()
    print("Start processing tips")

    tips = asyncio.run(generate_tips())

    print(f"Results: {tips}")
    for language, tip in tips:
        put_tip(language, tip)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Finish processing tips {total_time}s")