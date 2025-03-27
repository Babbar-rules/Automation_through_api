# Automation API Service

A Python-based API service that dynamically retrieves and executes automation functions using LLM + RAG (Retrieval-Augmented Generation). The system processes user prompts, maps them to predefined automation functions, and generates executable Python code for function invocation.

## Features

- **Function Registry**: Collection of common automation functions including application control, system monitoring, and command execution
- **LLM + RAG for Function Retrieval**: Uses sentence transformers and FAISS vector database for semantic search
- **Dynamic Code Generation**: Generates structured and executable Python scripts based on retrieved functions
- **Context Maintenance**: Session-based memory with chat history for context-aware responses
- **API Service**: FastAPI implementation for fast and easy deployment

## Project Structure

```
automation/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── code_generator.py
│   ├── function_registry/
│   │   ├── __init__.py
│   │   └── functions.py
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   └── vector_store.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py
│   ├── __init__.py
│   └── main.py
├── logs/
├── vector_db/
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Babbar-rules/Automation_through_api.git
cd automation
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the API server

```bash
fastapi dev main.py
```

The server will start on http://localhost:8000 by default.

### API Endpoints

#### Execute a Function

```http
POST /api/execute
```

Request body:
```json
{
  "prompt": "Open calculator",
  "session_id": "user123",
  "params": {}
}
```

Response:
```json
{
  "function": "open_calculator",
  "code": "from app.function_registry.functions import open_calculator\n\ndef main():\n    try:\n        result = open_calculator()\n        print(f\"Function executed successfully.\")\n        print(f\"Result: {result}\")\n        return result\n    except Exception as e:\n        print(f\"Error executing function: {e}\")\n        return {\"error\": str(e)}\n\nif __name__ == \"__main__\":\n    main()\n",
  "result": null,
  "error": null,
  "execution_time": 0.123
}
```

#### Execute Multiple Functions

```http
POST /api/multi-execute
```

Request body:
```json
{
  "prompt": "Check system resources",
  "session_id": "user123",
  "num_functions": 3,
  "params_list": []
}
```

#### Get Chat History

```http
GET /api/chat-history/{session_id}
```

#### Clear Chat History

```http
DELETE /api/chat-history/{session_id}
```

## Function Registry

The system includes various types of automation functions:

1. **Application Control**:
   - Opening browsers, calculators, text editors, file explorers

2. **System Monitoring**:
   - CPU usage, memory usage, disk usage, battery status

3. **Command Execution**:
   - Run shell commands, list files, read/write files

## Extending the System

### Adding New Functions

To add new functions to the registry:

1. Add the function implementation in `app/function_registry/functions.py`
2. Add function metadata to the `function_metadata` list in the same file
3. Add the function to the `function_mapping` dictionary

Example:
```python
def my_new_function(param1, param2="default"):
    """My new function description"""
    # Implementation
    return result

# Add to metadata
function_metadata.append({
    "name": "my_new_function",
    "description": "Description of what the function does",
    "keywords": ["keyword1", "keyword2"],
    "category": "category_name",
    "parameters": ["param1", "param2"]
})

# Add to mapping
function_mapping["my_new_function"] = my_new_function
```

4. Rebuild the vector database by deleting the `vector_db` directory (it will be recreated on next startup)

