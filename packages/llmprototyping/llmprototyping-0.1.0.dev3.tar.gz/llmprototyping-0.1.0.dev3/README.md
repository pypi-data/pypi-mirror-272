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

### Simple chat completion call

```python
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

import llmprototyping as llmp
factory = llmp.LLMChatCompletionFactory
model = factory.build('groq/llama3-70b-8192', {'api_key': groq_api_key})
msg = llmp.Message(content="De qué color es el caballo blanco de Santiago? Responde en json.")
resp = model.query([msg], json_response=True, temperature=0)
resp.show()
```

### List available models

```python
import llmprototyping as llmp

print('chat completion models:')
for model_name in llmp.LLMChatCompletionFactory.available_models:
    print(f"  {model_name}")

print('embedding models:')
for model_name in llmp.EmbeddingComputerFactory.available_models:
    print(f"  {model_name}")
```

### Embeddings example

```python
knowledge_list = [
    "Rome was founded in 753 BCE according to tradition, by Romulus and Remus.",
    "The Roman Republic was established in 509 BCE after overthrowing the last Etruscan kings.",
    "Julius Caesar became the perpetual dictator in 44 BCE, shortly before his assassination.",
    "The Roman Empire officially began when Octavian received the title of Augustus in 27 BCE.",
    "At its peak, the Roman Empire extended from Hispania to Mesopotamia.",
    "The capital of the Empire was moved to Constantinople by Constantine I in 330.",
    "The fall of Rome occurred in 476 CE when the last Western Roman emperor, Romulus Augustulus, was deposed.",
    "Roman culture greatly influenced law, politics, language, and architecture in the Western world.",
    "The expansion of Christianity as the official religion was promoted by Constantine after the Battle of the Milvian Bridge in 312.",
    "Roman society was heavily stratified between patricians, plebeians, and slaves."
]

question = "When was the Roman Empire founded?"

import os
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

import llmprototyping as llmp

import shelve
db = shelve.open('test_embeddings.db')

def get_embedding(text, computer):
    if text in db:
        json = db[text]
        return llmp.EmbeddingVector.from_json(json)

    print(f'computing embedding for "{text}"')
    em = computer.get_embedding(text)
    db[text] = em.to_json()

    return em

factory = llmp.EmbeddingComputerFactory
computer = factory.build('openai/text-embedding-3-small', {'api_key': openai_api_key})        

entry_table = dict()

for entry_id, entry_text in enumerate(knowledge_list):
    em = get_embedding(entry_text, computer)
    entry_table[entry_id] = em
    assert knowledge_list[entry_id] == entry_text

em_question = get_embedding(question, computer)

vdb = llmp.FAISSDatabase(embedding_type=computer.model_name, embedding_size=computer.vector_size)
vdb.put_records(entry_table)

print(f"query: {question}")
results = vdb.search(em_question)
for distance, entry_id in results:
    print(f"{distance:.3f} {entry_id} {knowledge_list[entry_id]}")
```