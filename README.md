This project is a multi-agent system built with the Google Agent Development Kit (ADK). It demonstrates how a team of agents can collaborate to handle user requests, with a root agent orchestrating tasks and delegating to specialized sub-agents.

The agent team can provide current weather information, 14-day forecasts, and handle conversational greetings and farewells.

## ✨ Features

*   **Current Weather:** Get the real-time weather for any city.
*   **Weather Forecast:** Retrieve a 14-day forecast.
*   **Agent Delegation:** A root agent analyzes user intent and delegates to:
    *   A `greeting_agent` for hellos.
    *   A `farewell_agent` for goodbyes.
*   **Tool Usage:** Demonstrates multiple tools for fetching data and generating responses.

## 📋 Prerequisites

*   Python 3.10+
*   An active Google Gemini API Key. You can create one in Google AI Studio.
*   An API key from WeatherAPI.com. A free account is sufficient.

## 🚀 Setup and Installation

1.  **Clone the Repository:**
    First, clone this repository to your local machine. Replace the URL with your repository's URL.
    ```bash
    git clone https://github.com/your-username/weather-agent.git
    ```

2.  **Navigate to the Project Directory:**
    ```bash
    cd weather-agent
    ```

3.  **Set up a Virtual Environment:**
    From the project's root directory, create and activate a Python virtual environment.
    ```bash
    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # For Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

4.  **Install Dependencies:**
    Install the necessary Python libraries.
    This command reads the `requirements.txt` file and installs the exact versions of all required packages.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Environment Variables:**
    Create a file named `.env` in the project's root directory and add your API keys.

    ```env
    # .env
    GOOGLE_GENAI_USE_VERTEXAI=FALSE
    GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    WEATHER_API_KEY="YOUR_WEATHER_API_KEY"
    ```

## ▶️ Running the Agent

1.  Make sure you are in the root directory of the project that contains the agent folder and your virtual environment is activated.
2.  Run the ADK web server:
    ```bash
    adk web
    ```
3.  The terminal will output a URL (usually `http://127.0.0.1:8000`). Open this in your browser and select the agent from the dropdown menu to interact with the agent.

## 💬 Example Interactions

You can try the following prompts in the web UI:

> `Hello there!`

> `What's the weather like in London?`

> `Can you give me the forecast for San Francisco?`

> `What's the weather like in Tokyo tomorrow?`

> `Thanks, that's all I need. Bye!`