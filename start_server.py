import subprocess
import sys
import os
from colorama import init, Fore, Back, Style

# Initialize Colorama for colors
init(autoreset=True)

def check_python():
    print(Fore.BLUE + "Checking if Python is installed...")
    try:
        # Check if Python is installed
        result = subprocess.run(["python", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(Fore.GREEN + "Python is installed: " + result.stdout.strip())
            return True
        else:
            print(Fore.RED + "Error: Python is not installed.")
            return False
    except FileNotFoundError:
        print(Fore.RED + "Error: Python is not installed.")
        return False

def check_requirements():
    print(Fore.BLUE + "Checking for dependencies installation...")
    if os.path.exists("requirements.txt"):
        try:
            # Check if packages are already installed
            subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
            print(Fore.GREEN + "Dependencies have been installed successfully.")
        except subprocess.CalledProcessError:
            print(Fore.RED + "Error during the installation of dependencies.")
    else:
        print(Fore.RED + "Error: requirements.txt not found.")

def check_node():
    print(Fore.BLUE + "Checking if Node.js is installed...")
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(Fore.GREEN + "Node.js is installed: " + result.stdout.strip())
            return True
        else:
            print(Fore.RED + "Error: Node.js is not installed.")
            return False
    except FileNotFoundError:
        print(Fore.RED + "Error: Node.js is not installed.")
        return False

def check_node_modules():
    print(Fore.BLUE + "Checking if Node.js modules are installed...")
    if os.path.exists("static/node_modules"):
        print(Fore.GREEN + "Node.js modules are already installed.")
    else:
        print(Fore.YELLOW + "Node.js modules not found. Installing...")
        try:
            subprocess.run(["npm", "install"], cwd="static", check=True)
            print(Fore.GREEN + "Node.js modules have been installed successfully.")
        except subprocess.CalledProcessError:
            print(Fore.RED + "Error during the installation of Node.js modules.")
            
def start_server():
    print(Fore.BLUE + "Starting server...")
    try:
        subprocess.run (["python", "app.py"], check=True)
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error starting server.")

def main():
    if check_python():
        check_requirements()
        
    if check_node():
        check_node_modules()
        
    start_server()
        

if __name__ == "__main__":
    main()