import openai
import os

# Define your OpenAI API key
api_key = 'MY_API_KEY'
openai.api_key = api_key

def generate_and_execute_code(instruction, previous_code=""):
    try:
        # Combine the instruction and previous code
        if previous_code:
            code_to_execute = previous_code + f"\n# Instruction: {instruction}\n"
        else:
            code_to_execute = f"# Instruction: {instruction}\n"

        # Generate code based on the user's instruction using OpenAI API
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Translate the following instruction into a Python code:\n\"{instruction}\"\nCode:",
            max_tokens=3500,
            temperature=0,
        )

        generated_code = response.choices[0].text.strip()

        # Combine the generated code with the existing code
        code_to_execute += generated_code

        # Create a Python .py file and write the combined code to it
        with open("generated_code.py", "w") as file:
            file.write(code_to_execute)

        # Execute the combined code
        exec(code_to_execute, globals())

        result = "Code executed successfully."
    except Exception as e:
        # Delete the existing code file
        if os.path.exists("generated_code.py"):
            os.remove("generated_code.py")

        # If there's an error, send the error message to the API to request a fix
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Fix the following Python code:\n\"{code_to_execute}\"\nError: {str(e)}\nCode:",
            max_tokens=3500,
            temperature=0,
        )
        fixed_code = response.choices[0].text.strip()
        result = f"Error: {str(e)}\nSuggested Fix:\n{fixed_code}"

        # Apply the suggested fix and relaunch
        if fixed_code:
            print("Applying the suggested fix...")
            code_to_execute = fixed_code
            result = generate_and_execute_code(instruction, code_to_execute)

    return result, code_to_execute

def main():
    code_to_execute = ""

    while True:
        user_instruction = input("Enter a programming instruction (or type 'stop' to exit): ")

        if user_instruction.lower() == 'stop':
            break

        result, code_to_execute = generate_and_execute_code(user_instruction, code_to_execute)
        print(result)

    print("Editor stopped.")

if __name__ == "__main__":
    main()
