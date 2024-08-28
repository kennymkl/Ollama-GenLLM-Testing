from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

def generate_text(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral", prompt],  # ollama command in local pc
            capture_output=True,
            text=True,
            shell=True,
            encoding='utf-8',  # Use UTF-8 encoding
            errors='replace'   # Replace characters that can't be decoded
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            if "failed to get console mode" in output:
                output = "\n".join(
                    line for line in output.splitlines() if "failed to get console mode" not in line
                )
            return output
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    generated_text = generate_text(prompt)
    
    # Print the generated text for debugging
    print(f"Generated Text: {generated_text}")
    
    return jsonify({"response": generated_text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
