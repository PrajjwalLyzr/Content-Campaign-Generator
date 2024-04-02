import os
from PIL import Image
import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.pipelines.linear_sync_pipeline  import  LinearSyncPipeline
from lyzr_automata import Logger
from dotenv import load_dotenv; load_dotenv()

# Setup your config
st.set_page_config(
    page_title="Content Campaign Generator",
    layout="centered",   
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png"
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Content Campaign Generator by Lyzr")
st.markdown("### Welcome to the Content Campaign Generator!")
st.markdown("Content Campaign Generator provides a comprehensive 3-5 month of content roadmap.!!!")

# Custom function to style the app
def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# Content Campaign Generator

# replace this with your openai api key or create an environment variable for storing the key.
API_KEY = os.getenv('OPENAI_API_KEY')

 

open_ai_model_text = OpenAIModel(
    api_key= API_KEY,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.5,
        "max_tokens": 1500,
    },
)

def content_campaign_generator(campaign_goal, target_audience):
    
    digital_marketer_agent = Agent(
        prompt_persona="""You are an expert Digital Marketer and as a Digital Marketer expert, your mission is to craft and execute innovative digital marketing strategies that elevate brand visibility and drive customer engagement. Utilize your expertise in data analysis, SEO optimization, social media management, and content creation to create compelling campaigns that resonate with target audiences and propel brands to new heights in the digital landscape.""",
        role="Digital Marketer", 
    )

    campaign_generator =  Task(
        name="Campaign Generator",
        agent=digital_marketer_agent,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions=f"Use the description provided Outline a content roadmap with key topics and formats for a 5-month content marketing campaign, the Campaign Goal : {campaign_goal} for the Target Audience: {target_audience}. [IMPORTANT!] Setup the events in a detailed manner",
        log_output=True,
        enhance_prompt=False,
        default_input=campaign_goal
    )


    logger = Logger()
    

    main_output = LinearSyncPipeline(
        logger=logger,
        name="Content Campaign Generator",
        completion_message="App Generated all things!",
        tasks=[
            campaign_generator,
        ],
    ).run()

    return main_output


if __name__ == "__main__":
    style_app() 
    campaign = st.text_area("Campaign Goal")
    audience = st.text_area('Targeted Audience')

    button=st.button('Submit')
    if (button==True):
        generated_output = content_campaign_generator(campaign_goal=campaign, target_audience=audience)
        title_output = generated_output[0]['task_output']
        st.write(title_output)
        st.markdown('---')
   
    with st.expander("ℹ️ - About this App"):
        st.markdown("""
        This app uses Lyzr Automata Agent to create the book title, chapters, cover image and also providing the writing tips. For any inquiries or issues, please contact Lyzr.
        
        """)
        st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)