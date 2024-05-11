#!/usr/bin/env python3

import google.generativeai as genai
from google.generativeai import types
import datetime

def generate_response(model_name, api_key, system_prompt, user_prompt, **kwargs):
    TIME_START = datetime.datetime.now().isoformat()

    genai.configure(api_key=api_key)

    gemini_model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_prompt
        )

    temperature = kwargs.get('temperature', 1)
    max_tokens = kwargs.get('max_tokens', 4096)

    config = types.GenerationConfig(
        candidate_count=1,
        max_output_tokens=max_tokens,
        temperature=temperature
    )

    response = gemini_model.generate_content(user_prompt, generation_config=config)

    TIME_FINISHED = datetime.datetime.now().isoformat()

    time_start = datetime.datetime.fromisoformat(TIME_START)
    time_complete = datetime.datetime.fromisoformat(TIME_FINISHED)

    duration = time_complete - time_start
    TIME_TO_RUN = duration.total_seconds()

    ai_output = {
        "$id": "csa-ai-toolkit-google-gemini1.5-JSON-v1_00",
        "metadata": {
            "system": system_prompt,
            "user-prompt": user_prompt,
            "user-data": kwargs.get('user_data'),
            "output": kwargs.get('output_file'),
            "model_name": model_name,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "time_start": TIME_START,
            "time_complete": TIME_FINISHED,
            "time_to_run": TIME_TO_RUN
        },
        "extracted_data": response.text
    }

    ai_output = {key: value for key, value in ai_output.items() if value is not None}

    return ai_output
