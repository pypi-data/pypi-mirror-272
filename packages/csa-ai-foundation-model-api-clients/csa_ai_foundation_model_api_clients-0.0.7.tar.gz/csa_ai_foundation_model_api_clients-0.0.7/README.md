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

## Examples:

```
#!/usr/bin/env python3

import os

from foundation_model_api_clients import FoundationModelAPIClient

def main():
    model_name = 'claude'
    api_key = os.getenv('ANTHROPIC_CLAUDE_API_KEY')

    client = FoundationModelAPIClient(model_name, api_key)

    system_prompt = "You are a helpful assistant."
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


