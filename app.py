import streamlit as st
import subprocess


model_options = {
    "Llama3.1": "llama3.1",
    "Mistral": "mistral",
    #other models
}

st.sidebar.title("Model Selection")
selected_model = st.sidebar.selectbox("Choose a Generative LLM", list(model_options.keys()))


model = model_options[selected_model]

def generate_text(prompt):
    try:
        # Use subprocess with stdin to pass the prompt
        process = subprocess.Popen(
            ["ollama", "run", model], #ollama command in local PC
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
            encoding='utf-8'
        )
        stdout, stderr = process.communicate(input=prompt)
        
        if process.returncode == 0:
            #Remove console mode errors for some reason they keep showing up
            output = stdout.strip()
            if "failed to get console mode" in output:
                output = "\n".join(
                    line for line in output.splitlines() if "failed to get console mode" not in line
                )
            return output
        else:
            #Handle any errors that occur
            return f"Error: {stderr.strip()}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"


def main():
    st.title("SimpleChat: Ollama Models Chatbot")
    
    #Chat history start
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input using st.chat_input
    if prompt := st.chat_input("Enter your prompt:"):
        with st.chat_message("user"):  # user message
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})  ##history

        # Generate response using the model
        with st.spinner("Thinking..."):
            generated_text = generate_text(prompt)
            #Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(generated_text)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": generated_text})

if __name__ == "__main__":
    main()
