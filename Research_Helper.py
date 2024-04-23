import streamlit as st
import openai

from openai import AsyncOpenAI
from openai import OpenAI
import os
import time

client = AsyncOpenAI(  
    api_key=os.getenv("API_key"),
)

class ChatHistory:
    def __init__(self):
       self.history = []

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

    def get_history_text(self):
        history_text = ""
        for message in self.history:
           history_text += f"{message['role']}: {message['content']}\n"
        return history_text.strip()
  
chat_history = ChatHistory()

async def generate_response(question, context):
    model = "gpt-4-0125-preview"

    # Convert chat history to a list of dictionaries
    chat_history_list = [{"role": message["role"], "content": message["content"]} for message in chat_history.history]

    # Add user question and previous context to history (list format)
    chat_history_list.append({"role": "user", "content": question})

    # Include full chat history in the prompt
    prompt = context + "\n" + question

    # monitor what's going on (optional)
    print(prompt)

    completion = await client.chat.completions.create(model=model, messages=chat_history_list)
    # Update context with system response
    context = completion.choices[0].message.content
    chat_history.add_message("system", context)
    return context

async def app():
    st.subheader("Resaeach Topic Helper")

    text = """Prof. Louie F. Cervantes, M. Eng. (Information Engineering) \n
    CCS 229 - Intelligent Systems
    Department of Computer Science
    College of Information and Communications Technology
    West Visayas State University"""
    st.text(text)

    st.image("teach-copilot.png", caption="Replace image and caption")

    text = """Replace this text with a brief description of the Research Helper App."""
    st.write(text)

    context = """You are a research co-pilot designed to assist students in finding reaarch problems for their undergraduate thesis. 
    When responding to prompts, prioritize providing resources and strategies that directly the student researcher.
    Remember, your primary function is to improve the quality of research."""

    # Prompt user for course input
    course = st.text_input("Enter your course:", key="course")

    # Display the entered course (optional)
    if course:
        st.write("Your course:", course)
        prompt = f"Give me a list of research areas in the course{course}. Provide the list as individual items enclosed in quotation marks and separated by commas."
        research_areas = await generate_response(prompt, context)
    else:
        st.warning("Please enter your course.") 
        return

    # Create the combobox (selectbox) with a descriptive label
    selected_option = st.selectbox(
        label="Choose the research area:",
        options=research_areas.split(",")  # Split the string into a list of options
        index=0  # Optionally set a default selected index
    )

    question = f"For the course {course} and the research area {selected_option}, give me 3 research problems.  Provide the title, abstract and research objectives for each research problem."

    # Create a checkbox and store its value
    checkbox_value = st.checkbox("Check this box if you want to input your own prompt.")

    # Display whether the checkbox is checked or not
    if checkbox_value:
        # Ask the user to input text
        question = st.text_input("Please input a custom prompt: ")

    # Button to generate response
    if st.button("Generate Response"):
    progress_bar = st.progress(0, text="The AI teacher co-pilot is processing the request, please wait...")
    if question:
        response = await generate_response(question, context)
        st.write("Response:")
        st.write(response)
    else:
        st.error("Please enter a prompt.")

    # update the progress bar
    for i in range(100):
        # Update progress bar value
        progress_bar.progress(i + 1)
        # Simulate some time-consuming task (e.g., sleep)
        time.sleep(0.01)
    # Progress bar reaches 100% after the loop completes
    st.success("AI teacher co-pilot task completed!") 

#run the app
if __name__ == "__main__":
  import asyncio
  asyncio.run(app())