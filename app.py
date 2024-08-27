import streamlit as st
import subprocess

def generate_text(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral", prompt], #ollama command in local pc
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode == 0:
            #Remove console mode errors for some reason they keep showing up
            output = result.stdout.strip()
            if "failed to get console mode" in output:
                output = "\n".join(
                    line for line in output.splitlines() if "failed to get console mode" not in line
                )
            return output
        else:
            # Handle any errors that occur
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"


def main():
    st.title("Ollama on Streamlit")
    
    #Chat history start
    if "messages" not in st.session_state:
        st.session_state.messages = []

    #Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input using st.chat_input
    if prompt := st.chat_input("Enter your prompt:"):
        with st.chat_message("user"): #user message
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt}) ##history

        #Generate response using the model
        with st.spinner("Thinking..."):
            generated_text = generate_text(prompt)
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(generated_text)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": generated_text})

if __name__ == "__main__":
    main()
