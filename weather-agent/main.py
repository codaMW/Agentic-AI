from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
import httpx


class Coordinates(BaseModel):
    latitude: float
    longitude: float


class CurrentWeather(BaseModel):
    city: str
    tempereture: float
    description: str


class WeatherAgent:
    def get_coordinates(self, city: str) -> Coordinates:

        try:
            response = httpx.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city, "count": 1},
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("results")

            if not results:
                raise ValueError(f"City '{city}' was not found.")

            result = results[0]

            return Coordinates(
                latitude=result["latitude"], longitude=result["longitude"]
            )

        except httpx.ConnectError:
            print("Could not connect to the server.")

        except httpx.TimeoutException:
            print("The request timed out.")

        except httpx.HTTPStatusError as e:
            print(f"Server returned HTTP {e.response.status_code}")

    def describe_weather(self, code: int) -> str:
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
        }
        return weather_codes.get(code, "Unknown")

    def get_weather(self, city) -> CurrentWeather:

        coordinates = self.get_coordinates(city)

        response = httpx.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": coordinates.latitude,
                "longitude": coordinates.longitude,
                "current": "temperature_2m,weather_code",
            },
        )
        response.raise_for_status()
        data = response.json()
        current = data["current"]
        return CurrentWeather(
            city=city,
            tempereture=current["temperature_2m"],
            description=self.describe_weather(current["weather_code"]),
        )


agent = Agent(
    "groq:llama-3.3-70b-versatile",
    instructions=(
        "You are a precise, helpful, and professional Weather Assistant. "
        "Your primary goal is to provide accurate weather forecasts and current conditions "
        "by utilizing available weather tools and structuring the data flawlessly.\n\n"
        "### Core Responsibilities:\n"
        "1. **Location Resolution:** Extract the location (city, country, region) from the user's query. If ambiguous, ask for clarification or use the most logical default.\n"
        "2. **Tool Execution:** Use the provided weather tools to fetch real-time or historical data. Never make up weather data.\n"
        "3. **Data Mapping:** Carefully parse the tool outputs to fulfill the schema requirements of the `WeatherAgent` response type.\n\n"
        "### Formatting & Tone Guidelines:\n"
        "- **Tone:** Friendly, conversational, but direct and informative.\n"
        "- **Units:** Default to the metric system (Celsius, km/h, mm) unless the user explicitly requests imperial units (Fahrenheit, mph).\n"
        "- **Clarity:** Summarize complex meteorological data into simple, digestible insights (e.g., instead of just 'humidity 95%', mention 'expect a humid day').\n\n"
        "### Behavioral Constraints:\n"
        "- If a location's weather cannot be found, populate the error fields in your structured output or explain the limitation gracefully.\n"
        "- Do not hallucinate current dates or times; rely entirely on the tool's timestamps or system context.\n"
        "- Strict adherence to the `WeatherAgent` output structure is mandatory."
    ),
    ## out_type=WeatherAgent
    deps_type=WeatherAgent,
)


@agent.tool
def current_weather(ctx: RunContext[WeatherAgent], city: str) -> CurrentWeather:
    print(f"[TOOL] Fetching weather for {city}")

    return ctx.deps.get_weather(city)


history = None


while True:
    prompt = input("you> ")

    if prompt.lower() in {"exit", "quit"}:
        break
    if not prompt:
        continue

    try:
        weather = WeatherAgent()
        result = agent.run_sync(prompt, message_history=history, deps=weather)
        print(f"bot> {result.output}")
        history = result.all_messages()
    except Exception as e:
        print(f"Error {type(e).__name__} {e}")
