from typing import Dict, Any, List, Optional
import inspect
from app.function_registry.functions import function_mapping

class CodeGenerator:
    """
    Generates executable Python code for the matched functions
    """
    
    @staticmethod
    def generate_code(function_name: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate executable Python code for a given function
        
        Args:
            function_name: Name of the function to generate code for
            params: Optional parameters for the function
            
        Returns:
            Executable Python code as a string
        """
        if function_name not in function_mapping:
            return f"# Error: Function '{function_name}' not found in the registry."
        
        # Get the actual function object
        func = function_mapping[function_name]
        
        # Get function signature to handle parameters properly
        sig = inspect.signature(func)
        param_names = [param.name for param in sig.parameters.values()]
        
        # Import statement
        code = f"from app.function_registry.functions import {function_name}\n\n"
        
        # Main function
        code += "def main():\n"
        code += "    try:\n"
        
        # Function call with parameters if needed
        if params and param_names:
            # Filter params to only include those that are in the function signature
            valid_params = {k: v for k, v in params.items() if k in param_names}
            
            if valid_params:
                param_str = ", ".join([f"{k}={repr(v)}" for k, v in valid_params.items()])
                code += f"        result = {function_name}({param_str})\n"
            else:
                code += f"        result = {function_name}()\n"
        else:
            code += f"        result = {function_name}()\n"
        
        # Print result
        code += "        print(f\"Function executed successfully.\")\n"
        code += "        print(f\"Result: {result}\")\n"
        code += "        return result\n"
        code += "    except Exception as e:\n"
        code += "        print(f\"Error executing function: {e}\")\n"
        code += "        return {\"error\": str(e)}\n\n"
        
        # Call main when script is run directly
        code += "if __name__ == \"__main__\":\n"
        code += "    main()\n"
        
        return code
    
    @staticmethod
    def generate_multi_function_code(function_names: List[str], params_list: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Generate code that calls multiple functions in sequence
        
        Args:
            function_names: List of function names to call
            params_list: Optional list of parameter dictionaries for each function
            
        Returns:
            Executable Python code as a string
        """
        if not function_names:
            return "# Error: No functions provided."
        
        # Ensure params_list has the same length as function_names
        if params_list is None:
            params_list = [None] * len(function_names)
        else:
            # Pad with None if params_list is shorter
            params_list.extend([None] * (len(function_names) - len(params_list)))
        
        # Import statement
        imports = [f"from app.function_registry.functions import {name}" for name in function_names]
        code = "\n".join(imports) + "\n\n"
        
        # Main function
        code += "def main():\n"
        code += "    results = {}\n"
        code += "    try:\n"
        
        # Function calls
        for i, (func_name, params) in enumerate(zip(function_names, params_list)):
            if func_name not in function_mapping:
                code += f"        # Warning: Function '{func_name}' not found in the registry.\n"
                continue
                
            # Get the actual function object
            func = function_mapping[func_name]
            
            # Get function signature to handle parameters properly
            sig = inspect.signature(func)
            param_names = [param.name for param in sig.parameters.values()]
            
            # Function call with parameters if needed
            if params and param_names:
                # Filter params to only include those that are in the function signature
                valid_params = {k: v for k, v in params.items() if k in param_names}
                
                if valid_params:
                    param_str = ", ".join([f"{k}={repr(v)}" for k, v in valid_params.items()])
                    code += f"        results['{func_name}'] = {func_name}({param_str})\n"
                else:
                    code += f"        results['{func_name}'] = {func_name}()\n"
            else:
                code += f"        results['{func_name}'] = {func_name}()\n"
                
            code += f"        print(f\"Function '{func_name}' executed successfully.\")\n"
        
        # Print results and return
        code += "        print(f\"All functions executed successfully.\")\n"
        code += "        return results\n"
        code += "    except Exception as e:\n"
        code += "        print(f\"Error executing functions: {e}\")\n"
        code += "        return {\"error\": str(e), \"partial_results\": results}\n\n"
        
        # Call main when script is run directly
        code += "if __name__ == \"__main__\":\n"
        code += "    main()\n"
        
        return code
    
    @staticmethod
    def create_executable_script(function_name: str, params: Optional[Dict[str, Any]] = None, output_path: Optional[str] = None) -> str:
        """
        Create an executable Python script for a function and optionally save it to a file
        
        Args:
            function_name: Name of the function to generate code for
            params: Optional parameters for the function
            output_path: Optional path to save the script to
            
        Returns:
            The generated code
        """
        code = CodeGenerator.generate_code(function_name, params)
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(code)
        
        return code
