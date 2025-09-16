import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.
    Args:
        city (str): The name of the city for which to retrieve the weather report.
    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "singapore":
        return {
            "status": "success",
            "report": (
                "The weather in Singapore is sunny with a temperature of 30 degrees"
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }

def get_time(city: str) -> dict:
    """Returns the current time in a specified city.
    Args:
        city (str): The name of the city for which to retrieve the current time.
    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "singapore":
        tz_identifier = "Asia/Singapore"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.5-pro",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_time],
)