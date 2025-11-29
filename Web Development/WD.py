#An API (Application Programming Interface) is a set of rules that allows one piece of software
#to interact with another. Essentially, it allows different software systems to communicate with 
# each other.

import json

# Python dictionary
person_data = {
    "name": "John",
    "age": 30,
    "is_student": False
}

# Convert Python dictionary to JSON string
person_json = json.dumps(person_data)

print(person_json)#https://pokeapi.co/ 

#A virtual environment is an isolated Pythonenvironment that allows you to manage dependencies
#for a project without affecting other projects or the system-wide packages.
#It allows different projects to have their own dependencies, making it easier to avoid conflicts 
#between packages and versions.

#commands for windows: 
#python -m venv venv
#venv\Scripts\activate
#pip install <packages you need>
