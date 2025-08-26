import os
import asyncio
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts


import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")


import logging
logging.basicConfig(level=logging.ERROR)


print("Libraries imported.")


import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

import os
from dotenv import load_dotenv
import requests
from typing import Optional

load_dotenv()

weather_api_key = os.getenv("WEATHER_API_KEY")


# @title Define Tools for Greeting and Farewell Agents
def say_hello(name: Optional[str] = None) -> str:
   """Provides a simple greeting. If a name is provided, it will be used.


   Args:
       name (str, optional): The name of the person to greet. Defaults to a generic greeting if not provided.


   Returns:
       str: A friendly greeting message.
   """
   if name:
       greeting = f"Hello, {name}!"
       print(f"--- Tool: say_hello called with name: {name} ---")
   else:
       greeting = "Hello there!" # Default greeting if name is None or not explicitly passed
       print(f"--- Tool: say_hello called without a specific name (name_arg_value: {name}) ---")
   return greeting


def say_goodbye() -> str:
   """Provides a simple farewell message to conclude the conversation."""
   print(f"--- Tool: say_goodbye called ---")
   return "Goodbye! Have a great day."


print("Greeting and Farewell tools defined.")



# @title Define the get_current_weather tool
def get_current_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
    """
    print(f"--- Tool: get_current_weather called for city: {city} ---") # Log tool execution

    response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no")

    return response.json()



# @title Define the get_forecast tool
def get_forecast(city: str) -> dict:
    """Retrieves the weather forecast for the next 14 days for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather forecast information.
    """
    print(f"--- Tool: get_forecast called for city: {city} ---") # Log tool execution

    response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={city}&days=14&aqi=no&alerts=no")

    return response.json()



# @title Define the Sub_Agents

# --- Greeting Agent ---
greeting_agent = None
try:
   greeting_agent = Agent(
       # Using a potentially different/cheaper model for a simple task
       model = "gemini-2.0-flash",
       # model=LiteLlm(model=MODEL_GPT_4O), # If you would like to experiment with other models
       name="greeting_agent",
       instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
                   "Use the 'say_hello' tool to generate the greeting. "
                   "If the user provides their name, make sure to pass it to the tool. "
                   "Do not engage in any other conversation or tasks.",
       description="Handles simple greetings and hellos using the 'say_hello' tool.", # Crucial for delegation
       tools=[say_hello],
   )
   print(f"✅ Agent '{greeting_agent.name}' created using model '{greeting_agent.model}'.")
except Exception as e:
   print(f"❌ Could not create Greeting agent. Check API Key ({greeting_agent.model}). Error: {e}")


# --- Farewell Agent ---
farewell_agent = None
try:
   farewell_agent = Agent(
       # Can use the same or a different model
       model = "gemini-2.0-flash",
       # model=LiteLlm(model=MODEL_GPT_4O), # If you would like to experiment with other models
       name="farewell_agent",
       instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
                   "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
                   "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
                   "Do not perform any other actions.",
       description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.", # Crucial for delegation
       tools=[say_goodbye],
   )
   print(f"✅ Agent '{farewell_agent.name}' created using model '{farewell_agent.model}'.")
except Exception as e:
   print(f"❌ Could not create Farewell agent. Check API Key ({farewell_agent.model}). Error: {e}")




# @title Define the Root Agent with Sub-Agents
# Ensure sub-agents were created successfully before defining the root agent.
# Also ensure the original 'get_weather' tool is defined.
root_agent = None
runner_root = None # Initialize runner


if greeting_agent and farewell_agent and 'get_current_weather' and 'get_forecast' in globals():
   # Let's use a capable Gemini model for the root agent to handle orchestration
   root_agent_model = "gemini-2.0-flash"


   root_agent = Agent(
       name="weather_agent",
       model=root_agent_model,
       description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
       instruction="You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information. "
                   "Use the 'get_current_weather' tool ONLY for specific weather requests (e.g., 'weather in London'). "
                   "Use the 'get_forecast' tool ONLY for specific weather forecast requests (e.g., 'what is the weather in London tomorrow?'). "
                   "You have specialized sub-agents: "
                   "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. "
                   "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. "
                   "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. "
                   "If it's a weather request, handle it yourself using 'get_current_weather'. "
                   "If it's a request for future weather forecast, handle it yourself using 'get_forecast'. "
                   "For anything else, respond appropriately or state you cannot handle it.",
       tools=[get_current_weather, get_forecast],
       sub_agents=[greeting_agent, farewell_agent]
   )
   print(f"✅ Root Agent '{root_agent.name}' created using model '{root_agent_model}' with sub-agents: {[sa.name for sa in root_agent.sub_agents]}")


else:
   print("❌ Cannot create root agent because one or more sub-agents failed to initialize or 'get_weather' tool is missing.")
   if not greeting_agent: print(" - Greeting Agent is missing.")
   if not farewell_agent: print(" - Farewell Agent is missing.")
   if 'get_current_weather' not in globals(): print(" - get_current_weather function is missing.")
   if 'get_forecast' not in globals(): print(" - get_forecast function is missing.")












