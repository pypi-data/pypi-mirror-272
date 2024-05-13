# Cloud Security Alliance AI Foundation Model API Clients

This Python library (csa_ai_foundation_model_api_clients) provides API access to text completions for:

* Anthropic Claude 3
* Google Gemini 1.5
* OpenAI ChatGPT 4

and has plans to add:

* OpenAI ChatGPT 4 batch mode

You can set the following options:

* system prompt (aka developer prompt, persona)
* user prompt (aka instructions)
* user data (as part of the user prompt)
* temperature
* max_tokens

and has plans to add:

* top_p
* top_k
* model specific paramaters

Please note this code does not have tests, or good error handling, but it works. Also with respect to handling rate
limiting that is on the todo, but currently if you use this tool put a sleep statement to slow it down.

The code will be looking for the API key as an env variable:

* ANTHROPIC_CLAUDE_API_KEY
* GOOGLE_GEMINI_API_KEY
* OPENAI_CHATGPT_API_KEY

## Examples:

Using this as a library:

```
#!/usr/bin/env python3

import os

from csa_ai_foundation_model_api_clients import FoundationModelAPIClient

def main():
    model_name = 'claude' # or "claude-haiku" or "chatgpt" or "gemini"
    api_key = "SECRET_API_KEY_VALUE" # You can remove api_key here if the env variable is set 

    client = FoundationModelAPIClient(model_name, api_key) # You can remove api_key here if the env variable is set 

    system_prompt = "You are a helpful assistant who speaks in rhymes."
    user_prompt = "What is the capital of France?"
    user_data = None
    output_file = 'response.json'

    response = client.generate_response(
        system_prompt,
        user_prompt,
        user_data,
        temperature=0.7,
        max_tokens=100,
        output_file=output_file
    )

if __name__ == '__main__':
    main()
```

Using this as a command line tool (you must be in the directory where csa_ai_foundation_model_api_clients.py is because of a relative import path):

```
./csa_ai_foundation_model_api_clients.py \
    --model chatgpt \
    --system system-prompt.txt \
    --user-prompt user-prompt.txt \
    --user-data user-data.txt \
    --output output.json \
    --temperature 0.9 \
    --max_tokens 2000
```

