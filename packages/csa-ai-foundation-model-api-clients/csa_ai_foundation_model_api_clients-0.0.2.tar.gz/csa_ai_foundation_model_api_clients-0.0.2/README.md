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
