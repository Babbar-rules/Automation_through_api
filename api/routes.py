from fastapi import APIRouter, HTTPException, Body, Request, Depends
from typing import Dict, Any, List, Optional
import time

from app.rag.embeddings import get_embedding_generator
from app.core.code_generator import CodeGenerator
from app.function_registry.functions import function_mapping
from app.utils.logger import log_info, log_error, log_function_execution

router = APIRouter()

# Store chat history for context
chat_sessions = {}

@router.post("/execute")
async def execute_function(request_data: Dict[str, Any] = Body(...)):
    """
    Execute a function based on user prompt
    """
    prompt = request_data.get("prompt")
    session_id = request_data.get("session_id", "default")
    params = request_data.get("params", {})
    
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    try:
        # Initialize or retrieve chat history for this session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        # Add this prompt to chat history
        chat_sessions[session_id].append({"role": "user", "content": prompt})
        
        # Get the embedding generator
        embedding_gen = get_embedding_generator()
        
        log_info(f"Received prompt: {prompt}")
        
        # Find matching function based on the prompt
        matches = embedding_gen.find_matching_function(prompt, k=1)
        
        if not matches:
            log_error(f"No matching function found for prompt: {prompt}")
            return {"error": "No matching function found"}
        
        best_match = matches[0]
        function_name = best_match["name"]
        
        log_info(f"Matched function: {function_name}")
        
        # Generate code for the function
        code = CodeGenerator.generate_code(function_name, params)
        
        # Execute the function
        start_time = time.time()
        error = None
        result = None
        
        try:
            if function_name in function_mapping:
                func = function_mapping[function_name]
                
                # Handle parameters based on function requirements
                if params:
                    result = func(**params)
                else:
                    result = func()
            else:
                error = f"Function {function_name} not found in registry"
        except Exception as e:
            error = str(e)
            log_error(f"Error executing function {function_name}: {e}")
        
        execution_time = time.time() - start_time
        
        # Log the execution
        log_entry = log_function_execution(
            function_name, params, result, error, execution_time
        )
        
        # Add response to chat history
        response_content = {
            "function": function_name,
            "result": result if not error else None,
            "error": error
        }
        chat_sessions[session_id].append({"role": "system", "content": response_content})
        
        return {
            "function": function_name,
            "code": code,
            "result": result,
            "error": error,
            "execution_time": execution_time
        }
        
    except Exception as e:
        log_error(f"Error in execute_function: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/multi-execute")
async def execute_multiple_functions(request_data: Dict[str, Any] = Body(...)):
    """
    Execute multiple functions based on user prompt and context
    """
    prompt = request_data.get("prompt")
    session_id = request_data.get("session_id", "default")
    num_functions = request_data.get("num_functions", 3)
    params_list = request_data.get("params_list", [])
    
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    try:
        # Initialize or retrieve chat history for this session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        # Add this prompt to chat history
        chat_sessions[session_id].append({"role": "user", "content": prompt})
        
        # Get the embedding generator
        embedding_gen = get_embedding_generator()
        
        log_info(f"Received multi-execute prompt: {prompt}")
        
        # Find multiple matching functions based on the prompt
        matches = embedding_gen.find_matching_function(prompt, k=num_functions)
        
        if not matches:
            log_error(f"No matching functions found for prompt: {prompt}")
            return {"error": "No matching functions found"}
        
        function_names = [match["name"] for match in matches]
        
        log_info(f"Matched functions: {function_names}")
        
        # Generate code for multiple functions
        code = CodeGenerator.generate_multi_function_code(function_names, params_list)
        
        # Execute the functions
        start_time = time.time()
        errors = {}
        results = {}
        
        for i, function_name in enumerate(function_names):
            try:
                if function_name in function_mapping:
                    func = function_mapping[function_name]
                    
                    # Get parameters for this function if available
                    params = params_list[i] if i < len(params_list) else {}
                    
                    # Handle parameters based on function requirements
                    if params:
                        results[function_name] = func(**params)
                    else:
                        results[function_name] = func()
                else:
                    errors[function_name] = f"Function {function_name} not found in registry"
            except Exception as e:
                errors[function_name] = str(e)
                log_error(f"Error executing function {function_name}: {e}")
        
        execution_time = time.time() - start_time
        
        # Log the executions
        for function_name in function_names:
            result = results.get(function_name)
            error = errors.get(function_name)
            params = params_list[function_names.index(function_name)] if function_names.index(function_name) < len(params_list) else None
            
            log_function_execution(
                function_name, params, result, error, execution_time / len(function_names)
            )
        
        # Add response to chat history
        response_content = {
            "functions": function_names,
            "results": results,
            "errors": errors
        }
        chat_sessions[session_id].append({"role": "system", "content": response_content})
        
        return {
            "functions": function_names,
            "code": code,
            "results": results,
            "errors": errors,
            "execution_time": execution_time
        }
        
    except Exception as e:
        log_error(f"Error in multi_execute_function: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat-history/{session_id}")
async def get_chat_history(session_id: str):
    """
    Get chat history for a session
    """
    if session_id not in chat_sessions:
        return {"history": []}
    
    return {"history": chat_sessions[session_id]}

@router.delete("/chat-history/{session_id}")
async def clear_chat_history(session_id: str):
    """
    Clear chat history for a session
    """
    if session_id in chat_sessions:
        chat_sessions[session_id] = []
    
    return {"message": f"Chat history cleared for session {session_id}"}
