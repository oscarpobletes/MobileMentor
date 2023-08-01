# Mobile Mentor App

The Mobile Mentor app combines Streamlit and LangChain to help you kickstart your mobile development journey smoothly and effectively.

## Installation

To run the MobileMentor app, you need to install the following dependencies:

`pip install streamlit langchain openai tiktoken alt-profanity-check`

## Running the App

To start the app, run the following command:

`streamlit run app.py`

## Usage

1. Launch the MobileMentor app by running the provided command.
2. Once the app is running, you will see a text area labeled "**Put your project description here**".
3. Enter a brief description of your desired mobile app project into the text area.
4. The app will check for profane and sensitive content in the description. If any such content is detected, an error message will be displayed, and you will need to provide another description.
5. If the description is appropriate, the app will generate a set of responses and recommendations based on your input.
6. The app will provide information in various categories, which can be expanded for more details:
   - **Context**: A brief summary of the understanding derived from the description.
   - **Name Ideas**: Suggestions for names for your mobile app.
   - **Tech Stack**: A full and ordered list of technologies to consider for your app.
   - **Integration**: Details on how to integrate the tech stack.
   - **Resources**: A list of documentation URLs for the tools mentioned in the tech stack.
   - **Features**: Suggestions for features and functionalities to be integrated into the app.
   - **Advice**: Guidance and advice for successfully developing your mobile app.

## Note
The clarity of the prompt directly influences the specificity of the response. When a development environment is not specified, the recommendations are more likely to be oriented towards hybrid development tools. On the other hand, when a specific environment such as iOS or Android is provided, the suggestions will be adjusted to match that particular platform.

## Rate Limit Considerations

When attempting to execute the application, it is likely to encounter RateLimit errors. This happens because the free version of the OpenAI API supports three requests per minute (RPM), while the application requires around eight requests per minute to perform optimally. If you are using the free version, the application will still work, but it is important to consider that occasional delays and rest periods between requests may be necessary.

Best of luck on your mobile development journey!
