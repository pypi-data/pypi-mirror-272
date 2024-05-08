# llmprototyping

`llmprototyping` is a Python package designed to provide easy and uniform access to various large language model (LLM) and embedding APIs, along with basic functionality for building small-scale artificial intelligence applications.

## Features

- **Uniform API Access**: Simplify your interactions with different LLM and embedding APIs using a single interface.
- **Basic AI Application Tools**: Get started quickly with tools designed to support the development of AI applications.

## License

Apache License Version 2.0

## Compatibility

python 3.9+

## Installation

```bash
pip install llmprototyping
```

## Usage

```python
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

import llmprototyping as llmp
factory = llmp.LLMChatCompletionFactory
model = factory.build('groq/Llama3-70b-8192', {'api_key': groq_api_key})
msg = llmp.Message(content="De qué color es el caballo blanco de Santiago? Responde en json.")
resp = model.query([msg], json_response=True, temperature=0)
resp.show()
```
