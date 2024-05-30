import time
from logger import logger

from openai import OpenAI

CODE_FILL_TAG = "<CODE>"
ERRORS_FILL_TAG = "<ERRORS>"

def build_prompt(prompt_template, snippet, errors):
    code_start_index = prompt_template.find(CODE_FILL_TAG)
    code_end_index = code_start_index + len(CODE_FILL_TAG)
    prompt = prompt_template[0:code_start_index] + snippet + prompt_template[code_end_index:]

    errors_start_index = prompt.find(ERRORS_FILL_TAG)
    prompt = prompt[:errors_start_index] + errors

    return prompt

def prompt_llm(prompt):
    #client = OpenAI()
    chat_completion = {
        "created": 121214148798,
        "model": "3eheheh",
        "usage": {
            "prompt_tokens": 21,
            "completion_tokens": 2,
            "total_tokens": 23
        },
        "choices": [
            {
                "message": {
                    "content": "hi"
                }
            }
        ]
    }

    #input()
    '''
    start_time = time.time()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4"
    )

    gen_time = time.time() - start_time
    logger.info(f"LLM answered in {gen_time}")
    '''
    gen_time = 2
    logger.debug(chat_completion)

    return chat_completion, gen_time
