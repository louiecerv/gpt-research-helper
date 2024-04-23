import streamlit as st
import openai

from openai import AsyncOpenAI
from openai import OpenAI
import os
import time

client = AsyncOpenAI(  
    api_key=os.getenv("API_key"),
)

def split_comma_separated_string(string):
    """Splits a string containing comma-separated items into a list.

    Args:
        string: The string to split.

    Returns:
        A list containing the individual items from the string.
    """

    # Split the string by comma, handling potential spaces around commas
    return string.split(", ")

async def generate_response(question, context):
    model = "gpt-4-0125-preview"

    completion = await client.chat.completions.create(model=model, 
        messages=[{"role": "user", "content": question}, 
                {"role": "system", "content": context}])
    return completion.choices[0].message.content

async def app():
    st.subheader("Reseach Topic Helper")

    text = """Prof. Louie F. Cervantes, M. Eng. (Information Engineering) \n
    CCS 229 - Intelligent Systems
    Department of Computer Science
    College of Information and Communications Technology
    West Visayas State University"""
    st.text(text)

    st.image("research_helper.png", caption="Researdh Helper App", use_column_width=True)

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
        prompt = f"Give me a list of research areas in the course{course}. Provide the list as individual items separated by commas. Provide only the list on the required format and do not include any additional information."
        research_areas = await generate_response(prompt, context)
        st.write("Research areas:", research_areas)

        # Create the combobox (selectbox) with a descriptive label
        selected_option = st.selectbox(
            label="Choose the research area:",
            options=split_comma_separated_string(research_areas),
            index=0  # Optionally set a default selected index
        )

    else:
        st.warning("Please enter your course.") 
        return


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