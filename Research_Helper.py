import streamlit as st
import openai

from openai import AsyncOpenAI
from openai import OpenAI
import os
import time

client = AsyncOpenAI(  
    api_key=os.getenv("API_key"),
)

context = """You are a research co-pilot designed to assist students in finding reaarch 
    problems for their undergraduate thesis. When responding to prompts, prioritize 
    providing resources and strategies that directly the student researcher. Remember, 
    your primary function is to improve the quality of research."""

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

# Use session state to track the current form
if "current_form" not in st.session_state:
    st.session_state["current_form"] = 1    

if "course" not in st.session_state:
    st.session_state["course"] = ""


async def app():
    st.session_state["current_form"] = 1
    form1 = st.form("Introduction")
    form1.subheader("Reseach Topic Helper")

    text = """Prof. Louie F. Cervantes, M. Eng. (Information Engineering) \n
    CCS 229 - Intelligent Systems
    Department of Computer Science
    College of Information and Communications Technology
    West Visayas State University"""
    form1.text(text)
    form1.image("research_helper.png", caption="Researdh Helper App", use_column_width=True)
    text = """Replace this text with a brief description of the Research Helper App."""
    form1.write(text)
    # Prompt user for course input
    course = form1.text_input("Enter your course:", key="course")

    submit1 = form1.form_submit_button("Submit")
    if submit1:
        if course:
            st.session_state["course"] = course
            st.session_state["current_form"] = 2
            display_form2()
        else:
            st.warning("Please enter your course.")        

async def display_form2():
    course = st.session_state["course"]
    st.session_state["current_form"] = 2
    form2 = st.form("Uaer Input")
    prompt = f"Give me a list of research areas in the course{course}. Provide the list as individual items separated by commas. Provide only the list on the required format and do not include any additional information."
    research_areas = await generate_response(prompt, context)
    options = split_comma_separated_string(research_areas)
      
    # Create the combobox (selectbox) with a descriptive label
    selected_option = form2.selectbox(
        label="Choose the research area:",
        options=options,
    )
    # Create a checkbox and store its value
    checkbox_value = form2.checkbox("Check this box if you want to input your own prompt.")

    submit2 = form2.form_submit_button("Get Research Problems")
    if submit2:
        question = f"For the course {course} and the research area {selected_option}, give me 3 research problems.  Provide the title, abstract and research objectives for each research problem."
        # Display whether the checkbox is checked or not
        if checkbox_value:
            # Ask the user to input text
            question = st.text_input("Please input a custom prompt: ")
        
        #save the data to the session state
        st.session_state["question"] = question
        st.session_state["research_area"] = selected_option

        display_form3()

async def display_form3():
    st.session_state["current_form"] = 3
    question = st.session_state["question"]

    form3 = st.form("Research Problems")
    progress_bar = form3.progress(0, text="The AI teacher co-pilot is processing the request, please wait...")
    if question:
        response = await generate_response(question, context)
        form3.write("Response:")
        form3.write(response)
    else:
        form3.error("Please enter a prompt.")

    # update the progress bar
    for i in range(100):
        # Update progress bar value
        progress_bar.progress(i + 1)
        # Simulate some time-consuming task (e.g., sleep)
        time.sleep(0.01)
    # Progress bar reaches 100% after the loop completes
    form3.success("AI teacher co-pilot task completed!") 

#run the app
if __name__ == "__main__":
    import asyncio
    asyncio.run(app())