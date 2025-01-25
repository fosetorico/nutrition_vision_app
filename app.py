import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv() # load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini And get response
def get_gemini_repsonse(input_prompt,image):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
# initialize streamlit app
st.set_page_config(page_title="Nutritional App for Calories")
st.header("Nutritional App for Calories")
# input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

submit = st.button("Tell me the total calories")

# Input Prompt
input_prompt="""
    You are an expert in nutritionist where you need to see the food items from the image
    and calculate the total calories, also provide the details of every food items with calories intake
    is below format

        1. Item 1 - no of calories
        2. Item 2 - no of calories
        ----
        ----
    Finally, you can also mention if the food is healthy or not with proper reason why, 
    and also mention the percentage split of the ratio of carbohydrates, fats, fibers, sugars and
    other important information required in our diet
"""

# If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_repsonse(input_prompt,image_data)
    st.subheader("The Response is")
    st.write(response)
