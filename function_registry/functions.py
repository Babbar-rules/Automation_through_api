import os
import webbrowser
import subprocess
import platform
import sys
import psutil

# Application Control Functions
def open_chrome():
    """Open Google Chrome browser."""
    if platform.system() == "Windows":
        try:
            webbrowser.get("chrome").open("https://www.google.com")
        except:
            webbrowser.open("https://www.google.com")  # Fallback
    else:
        webbrowser.open("https://www.google.com")

def open_calculator():
    """Open the system calculator application."""
    if platform.system() == "Windows":
        os.system("calc")
    elif platform.system() == "Darwin":  # macOS
        os.system("open -a Calculator")
    else:  # Linux
        os.system("gnome-calculator")

def open_notepad():
    """Open the system notepad/text editor."""
    if platform.system() == "Windows":
        os.system("notepad")
    elif platform.system() == "Darwin":  # macOS
        os.system("open -a TextEdit")
    else:  # Linux
        os.system("gedit")

def open_file_explorer():
    """Open the system file explorer."""
    if platform.system() == "Windows":
        os.system("explorer")
    elif platform.system() == "Darwin":  # macOS
        os.system("open .")
    else:  # Linux
        os.system("xdg-open .")

# System Monitoring Functions
def get_cpu_usage():
    """Get current CPU usage percentage."""
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    """Get current RAM usage information."""
    memory = psutil.virtual_memory()
    return {
        "total": f"{memory.total / (1024**3):.2f} GB",
        "available": f"{memory.available / (1024**3):.2f} GB",
        "percent_used": f"{memory.percent}%",
        "used": f"{memory.used / (1024**3):.2f} GB"
    }

def get_disk_usage():
    """Get disk usage information for the main disk."""
    disk = psutil.disk_usage('/')
    return {
        "total": f"{disk.total / (1024**3):.2f} GB",
        "used": f"{disk.used / (1024**3):.2f} GB",
        "free": f"{disk.free / (1024**3):.2f} GB",
        "percent_used": f"{disk.percent}%"
    }

def get_battery_status():
    """Get battery status if available."""
    if not hasattr(psutil, "sensors_battery"):
        return {"error": "Battery status not available on this system"}
    
    battery = psutil.sensors_battery()
    if battery is None:
        return {"error": "No battery detected"}
    
    return {
        "percent": f"{battery.percent}%",
        "power_plugged": battery.power_plugged,
        "time_left": f"{battery.secsleft / 60:.2f} minutes" if battery.secsleft != -1 else "Unlimited"
    }

# Command Execution Functions
def run_shell_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return {"success": True, "output": result.stdout, "error": result.stderr}
    except subprocess.CalledProcessError as e:
        return {"success": False, "output": e.stdout, "error": e.stderr}

def list_files_in_directory(directory="."):
    """List all files in the specified directory."""
    try:
        files = os.listdir(directory)
        return {"success": True, "files": files}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_system_info():
    """Get basic system information."""
    return {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version
    }

def create_file(filename, content=""):
    """Create a new file with optional content."""
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return {"success": True, "message": f"File {filename} created successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def read_file(filename):
    """Read the contents of a file."""
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return {"success": True, "content": content}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Function Metadata for RAG
function_metadata = [
    {
        "name": "open_chrome",
        "description": "Opens Google Chrome web browser",
        "keywords": ["chrome", "browser", "web", "google", "internet", "open", "launch", "start"],
        "category": "application_control"
    },
    {
        "name": "open_calculator",
        "description": "Opens the system calculator application",
        "keywords": ["calculator", "calc", "math", "open", "launch", "start"],
        "category": "application_control"
    },
    {
        "name": "open_notepad",
        "description": "Opens the system text editor or notepad",
        "keywords": ["notepad", "text editor", "editor", "text", "notes", "open", "launch", "start"],
        "category": "application_control"
    },
    {
        "name": "open_file_explorer",
        "description": "Opens the system file explorer or file manager",
        "keywords": ["file explorer", "explorer", "file manager", "files", "browse", "open", "launch", "start"],
        "category": "application_control"
    },
    {
        "name": "get_cpu_usage",
        "description": "Returns the current CPU usage percentage",
        "keywords": ["cpu", "processor", "usage", "load", "performance", "monitoring", "system", "stats"],
        "category": "system_monitoring"
    },
    {
        "name": "get_memory_usage",
        "description": "Returns information about RAM usage",
        "keywords": ["memory", "ram", "usage", "monitoring", "system", "performance", "stats"],
        "category": "system_monitoring"
    },
    {
        "name": "get_disk_usage",
        "description": "Returns information about disk space usage",
        "keywords": ["disk", "storage", "drive", "space", "usage", "monitoring", "system", "stats"],
        "category": "system_monitoring"
    },
    {
        "name": "get_battery_status",
        "description": "Returns battery status information if available",
        "keywords": ["battery", "power", "status", "charge", "monitoring", "system", "laptop"],
        "category": "system_monitoring"
    },
    {
        "name": "run_shell_command",
        "description": "Executes a shell command and returns the output",
        "keywords": ["shell", "command", "cmd", "terminal", "console", "execute", "run"],
        "category": "command_execution",
        "parameters": ["command"]
    },
    {
        "name": "list_files_in_directory",
        "description": "Lists all files in a specified directory",
        "keywords": ["list", "files", "directory", "folder", "contents", "ls", "dir"],
        "category": "command_execution",
        "parameters": ["directory"]
    },
    {
        "name": "get_system_info",
        "description": "Returns basic system information",
        "keywords": ["system", "info", "information", "details", "specs", "specifications", "os", "platform"],
        "category": "system_monitoring"
    },
    {
        "name": "create_file",
        "description": "Creates a new file with optional content",
        "keywords": ["create", "file", "new", "make", "write"],
        "category": "command_execution",
        "parameters": ["filename", "content"]
    },
    {
        "name": "read_file",
        "description": "Reads the contents of a file",
        "keywords": ["read", "file", "content", "open", "view"],
        "category": "command_execution",
        "parameters": ["filename"]
    }
]

# Function mapping for easy access
function_mapping = {
    "open_chrome": open_chrome,
    "open_calculator": open_calculator,
    "open_notepad": open_notepad,
    "open_file_explorer": open_file_explorer,
    "get_cpu_usage": get_cpu_usage,
    "get_memory_usage": get_memory_usage,
    "get_disk_usage": get_disk_usage,
    "get_battery_status": get_battery_status,
    "run_shell_command": run_shell_command,
    "list_files_in_directory": list_files_in_directory,
    "get_system_info": get_system_info,
    "create_file": create_file,
    "read_file": read_file
}
