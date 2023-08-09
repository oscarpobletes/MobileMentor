# Óscar Poblete Sáenz
# École de Technologie Supérieure
import os # Operating System 
import random # Make random choices
from apikey import apikey # Use OpenAI API key
import streamlit as st # Build the app
from profanity_check import predict # Detect profanity
from langchain.llms import OpenAI # Build LLM workflow
from langchain.prompts import PromptTemplate # Make specific prompts
from langchain.chains import LLMChain, SequentialChain # Chain prompt templates 

# Set API key
os.environ['OPENAI_API_KEY'] = apikey

# Configuration
st.set_page_config(
    page_title="Mobile Mentor",
    page_icon="🤓",
)

# Helper functions
def get_success_phrase():
    success_phrases = [
        "I've got just the information you need!🫰",
        "Voila! Your answer is right here. 🎩",
        "Here's what you're looking for. ✅",
        "Take a look at this. 👀",
        "Ta-da! Your answer is right in front of you. 🎉",
        "Your answer has materialized. 🧞‍♂️",
        "Your wish is my command! Check this out. 💫",
        "I've got your back! Here's some useful information. 🤝",
        "Let me help you with that. 🙌",
        "I'm on it! Here's the information you need. 📝",
        "Take a peek at this. 🔍"
    ]
    return random.choice(success_phrases)

def get_error_phrase():
    error_phrases = [
        "I can't help you with that. 😶",
        "I don't have an answer for that. 🥴",
        "I don't have the answer you're looking for. 🙃",
        "I'm unable to assist with that. 🧐",
        "I don't have the information you need. 😣",
        "I can't provide a response for that. 🚫",
        "I'm not able to answer that at the moment. 🤔",
        "I'm unable to help with that. ❌",
        "I don't have the knowledge for that. 🤕",
        "I don't have a suitable answer for that. 😕"
    ]
    return random.choice(error_phrases)

# Prompt templates
validation_template = PromptTemplate(
    input_variables=['description'],
    template="""
    If this description has no context, is inappropriate, sensitive, or offensive just say "FLAG" 
    DESCRIPTION: {description}
    """
)

context_template = PromptTemplate(
    input_variables=['description'],
    template="""
    Give me a very brief summary of what you understand from the following description of a mobile application  
    DESCRIPTION: {description}
    """
)

names_template = PromptTemplate(
    input_variables=['context'],
    template="""
    Give me a list of name ideas for a mobile app based on the following context 
    CONTEXT: {context}
    """
)

stack_template = PromptTemplate(
    input_variables=['context'],
    template="""
    Give me a full and ordered tech stack for a mobile app based on the following context
    CONTEXT: {context}
    """
)

integration_template = PromptTemplate(
    input_variables=['context', 'stack'],
    template="""
    Give me details on how to integrate this tech stack
    STACK: {stack}
    given the following context
    CONTEXT: {context}
    """
)

resources_template = PromptTemplate(
    input_variables=['stack'],
    template="""
    Give me a list of documentation URLs for all the tools mentioned in this tech stack
    STACK: {stack}
    """
)

features_template = PromptTemplate(
    input_variables=['context'],
    template="""
    Give me a list of features and functionalities that should be considered and integrated into a mobile app based on the following context
    CONTEXT: {context}
    """
)

advice_template = PromptTemplate(
    input_variables=['context'],
    template="""
    Give me some advice to successfully develop a mobile app based on the following context
    CONTEXT: {context}
    """
)

# Language model and chains
llm = OpenAI(temperature=0.0)
validation_chain = LLMChain(llm=llm, prompt=validation_template, verbose=True)
context_chain = LLMChain(llm=llm, prompt=context_template, verbose=True, output_key='context')
names_chain = LLMChain(llm=llm, prompt=names_template, verbose=True, output_key='names')
stack_chain = LLMChain(llm=llm, prompt=stack_template, verbose=True, output_key='stack')
integration_chain = LLMChain(llm=llm, prompt=integration_template, verbose=True, output_key='integration')
resources_chain = LLMChain(llm=llm, prompt=resources_template, verbose=True, output_key='resources')
features_chain = LLMChain(llm=llm, prompt=features_template, verbose=True, output_key='features')
advice_chain = LLMChain(llm=llm, prompt=advice_template, verbose=True, output_key='advice')
sequential_chain = SequentialChain(
    chains=[
        context_chain,
        names_chain,
        stack_chain,
        integration_chain,
        resources_chain,
        features_chain,
        advice_chain
    ],
    input_variables=['description'],
    output_variables=['context', 'names', 'stack', 'integration', 'resources', 'features', 'advice'],
    verbose=True
)

# App content
st.markdown("<h1 style='text-align: center;'>🤓 Mobile Mentor</h1>", unsafe_allow_html=True)
st.markdown("""
<p style="text-align: center;"><i>Your trusted companion in the world of mobile development.</i> <br><br>
Do you have an amazing idea but don't know where to begin? No need to worry! I'm here to help you kickstart your mobile development journey smoothly and effectively. Just give me a brief description of your desired outcome, and I'll make sure to understand it and provide you with practical ideas, recommendations, step-by-step guidance, and other valuable information to help you achieve your goal. Go ahead and test me!<br></p>
""", unsafe_allow_html=True)

# User input
prompt = st.text_area("**Put your project description here**")

# Process user input
if prompt:
    # Check for profane and sensitive content
    with st.spinner("Checking prompt..."):
        is_sensitive = any(predict([prompt]))
        validation_response = str(validation_chain.run(description=prompt)).lower().strip()

    if is_sensitive or validation_response == 'flag':
        # Handle sensitive or inappropriate content
        error_phrase = get_error_phrase()
        st.snow()
        st.write(error_phrase)
        with st.expander('**🚨 Warning**'):
            st.info('Your description may not have enough context, be inappropriate, sensitive, or offensive. Please provide another prompt')
    else:
        # Generate responses
        with st.spinner("Generating response..."):
            response = sequential_chain({'description': prompt})
        success_phrase = get_success_phrase()
        st.balloons()
        st.write(success_phrase)

        with st.expander('**🧠 Context**'):
            st.info(response['context'])
        with st.expander('**💡 Name ideas**'):
            st.info(response['names'])
        with st.expander('**🍔 Tech stack**'):
            st.info(response['stack'])
        with st.expander('**🧩 Integration**'):
            st.info(response['integration'])
        with st.expander('**📚 Resources**'):
            st.info(response['resources'])
        with st.expander('**✨ Features**'):
            st.info(response['features'])
        with st.expander('**🔮 Advice**'):
            st.info(response['advice'])
