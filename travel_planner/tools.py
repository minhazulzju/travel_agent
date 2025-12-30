from google.adk.tools import FunctionTool


# --- Budget Calculation Tool ---
def calculate_budget(
    user_id: str, destination: str, days: int, travelers: int = 1
) -> str:
    """
    Estimate travel budget based on destination, days, and number of travelers.
    (Uses static average costs; can be extended with real APIs.)
    """
    # Example static costs (USD)
    avg_flight = 500
    avg_hotel_per_night = 100
    avg_food_per_day = 40
    avg_transport_per_day = 20
    total = (
        avg_flight * travelers
        + avg_hotel_per_night * days * travelers
        + avg_food_per_day * days * travelers
        + avg_transport_per_day * days * travelers
    )
    return (
        f"Estimated budget for {travelers} traveler(s) to {destination} for {days} days:\n"
        f"- Flights: ${avg_flight * travelers}\n"
        f"- Hotels: ${avg_hotel_per_night * days * travelers}\n"
        f"- Food: ${avg_food_per_day * days * travelers}\n"
        f"- Local Transport: ${avg_transport_per_day * days * travelers}\n"
        f"- Total: ${total} (estimate)\n"
        "Tip: Book in advance and compare prices for savings."
    )


budget_tool = FunctionTool(func=calculate_budget)


# --- Visa Check Tool ---
def check_visa_requirement(nationality: str, destination: str) -> str:
    """
    Check visa requirements (static demo; extend with real API for production).
    """
    # Example: US citizens to France = no visa for short stays
    if nationality.lower() == "us" and destination.lower() == "france":
        return "No visa required for US citizens visiting France for up to 90 days."
    return f"Visa requirements for {nationality} to {destination}: Please check the official embassy website for up-to-date information."


visa_tool = FunctionTool(func=check_visa_requirement)


# --- Local Events Tool ---
def find_local_events(
    destination: str, start_date: str = None, end_date: str = None
) -> str:
    """
    Find local events (static demo; extend with real API for production).
    """
    # Example static events
    events = [
        "Food Festival - Central Park, July 10-12",
        "Jazz Night - Downtown Club, July 11",
        "Art Market - Main Square, July 12-13",
    ]
    return f"Upcoming events in {destination}:\n" + "\n".join(events)


local_events_tool = FunctionTool(func=find_local_events)


# --- Language & Culture Tool ---
def get_language_culture_tips(destination: str, language: str = None) -> str:
    """
    Provide basic phrases and etiquette tips (static demo; extend with real API for production).
    """
    tips = [
        "Basic greeting: 'Hello' = 'Bonjour' (French)",
        "Thank you: 'Merci' (French)",
        "Cultural tip: Always greet shopkeepers when entering a store.",
        "Tipping: 10-15% is customary in restaurants.",
    ]
    return f"Language & culture tips for {destination}:\n" + "\n".join(tips)


language_culture_tool = FunctionTool(func=get_language_culture_tips)
from google.adk.tools.google_search_tool import google_search
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool


# --- Profile Update Tool ---
def update_user_profile(user_id: str, profile_updates: dict) -> str:
    """
    Update the user's profile in memory.
    Args:
        user_id (str): Unique user identifier.
        profile_updates (dict): Dict of profile fields to update.
    Returns:
        str: Confirmation message.
    """
    user_context_memory.update_profile(user_id, profile_updates)
    return "✅ Your profile has been updated!"


profile_update_tool = FunctionTool(func=update_user_profile)


# --- Feedback Tool ---
def submit_feedback(user_id: str, feedback: str) -> str:
    """
    Store user feedback (rating, comment, etc.) in user context memory.
    Args:
        user_id (str): Unique user identifier.
        feedback (str): Feedback text or rating.
    Returns:
        str: Confirmation message.
    """
    user_context_memory.add_feedback(user_id, feedback)
    return (
        "✅ Thank you for your feedback! It will help us improve your recommendations."
    )


feedback_tool = FunctionTool(func=submit_feedback)


# --- Google Search Grounding AgentTool ---
LLM = "gemini-robotics-er-1.5-preview"

_search_agent = Agent(
    model=LLM,
    name="google_search_wrapped_agent",
    description="An agent providing Google-search grounding capability",
    instruction="""
        Answer the user's question directly using google_search grounding tool; Provide a brief but concise response. 
        Rather than a detail response, provide the immediate actionable item for a tourist or traveler, in a single sentence.
        Do not ask the user to check or look up information for themselves, that's your role; do your best to be informative.
        IMPORTANT: 
        - Always return your response in bullet points
        - Specify what matters to the user
    """,
    tools=[google_search],
)

google_search_grounding = AgentTool(agent=_search_agent)


from google.adk.tools import FunctionTool
from geopy.geocoders import Nominatim
import requests
from typing import Dict, Any, Optional


# --- User Context Memory (Simple Example) ---


class UserContextMemory:
    """
    Enhanced in-memory user context for demo purposes.
    Stores profile, preferences, history, and feedback for personalization.
    """

    def __init__(self):
        self.user_data: Dict[str, Dict[str, Any]] = {}

    def get(self, user_id: str) -> Dict[str, Any]:
        return self.user_data.setdefault(
            user_id,
            {
                "profile": {
                    "activities": [],  # e.g., ["adventure", "culture", "food"]
                    "budget": None,  # e.g., "low", "mid", "high"
                    "style": None,  # e.g., "relaxation", "adventure", "family"
                    "age_group": None,  # e.g., "18-25", "26-40", etc.
                },
                "preferences": {},
                "history": [],
                "feedback": [],
            },
        )

    def update_profile(self, user_id: str, profile_updates: Dict[str, Any]):
        self.get(user_id)["profile"].update(profile_updates)

    def get_profile(self, user_id: str) -> Dict[str, Any]:
        return self.get(user_id)["profile"]

    def update_preferences(self, user_id: str, preferences: Dict[str, Any]):
        self.get(user_id)["preferences"].update(preferences)

    def add_history(self, user_id: str, query: str):
        self.get(user_id)["history"].append(query)

    def add_feedback(self, user_id: str, feedback: str):
        self.get(user_id)["feedback"].append(feedback)


user_context_memory = UserContextMemory()


def get_weather_forecast(location: str, days: int = 1) -> str:
    """
    Fetches weather forecast for a location using Open-Meteo API.
    Args:
        location (str): City or place name.
        days (int): Number of days to forecast (default: 1).
    Returns:
        str: Weather summary or error message.
    """
    try:
        geolocator = Nominatim(user_agent="weather_agent")
        loc = geolocator.geocode(location)
        if not loc:
            return f"❌ Could not find location '{location}' for weather."
        lat, lon = loc.latitude, loc.longitude
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode&forecast_days={days}&timezone=auto"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return f"❌ Weather API error: {resp.status_code}"
        data = resp.json().get("daily", {})
        if not data:
            return "ℹ️ No weather data available."
        temps_max = data.get("temperature_2m_max", [])
        temps_min = data.get("temperature_2m_min", [])
        precip = data.get("precipitation_sum", [])
        summary = [
            f"Weather for {location} (next {days} day{'s' if days > 1 else ''}):"
        ]
        for i in range(min(days, len(temps_max))):
            summary.append(
                f"- Day {i+1}: High {temps_max[i]}°C, Low {temps_min[i]}°C, Precipitation: {precip[i]}mm"
            )
        return "\n".join(summary)
    except requests.Timeout:
        return "❌ Weather request timed out."
    except Exception as e:
        return f"❌ Error fetching weather: {str(e)}"


weather_tool = FunctionTool(func=get_weather_forecast)


def find_nearby_places_open(
    query: str, location: str, radius: int = 3000, limit: int = 5
) -> str:
    """
    Finds nearby places for any text query using free OpenStreetMap APIs (no API key needed).

    Args:
        query (str): What you’re looking for (e.g., "restaurant", "hospital", "gym", "bar").
        location (str): The city or area to search in.
        radius (int): Search radius in meters (default: 3000).
        limit (int): Number of results to show (default: 5).

    Returns:
        str: List of matching place names and addresses, formatted for user display.
    """
    try:
        geolocator = Nominatim(user_agent="open_place_finder_modern")
        loc = geolocator.geocode(location)
        if not loc:
            return f"❌ Could not find location '{location}'. Please check the spelling or try a nearby city."

        lat, lon = loc.latitude, loc.longitude
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json][timeout:25];
        (
          node["name"~"{query}", i](around:{radius},{lat},{lon});
          node["amenity"~"{query}", i](around:{radius},{lat},{lon});
          node["shop"~"{query}", i](around:{radius},{lat},{lon});
        );
        out body {limit};
        """
        response = requests.get(
            overpass_url, params={"data": overpass_query}, timeout=20
        )
        if response.status_code != 200:
            return f"❌ Overpass API error: {response.status_code}. Please try again later."

        data = response.json()
        elements = data.get("elements", [])
        if not elements:
            return f"ℹ️ No results found for '{query}' near {location}. Try a different keyword or location."

        output = [
            f"Top {min(limit, len(elements))} results for '{query}' near {location}:"
        ]
        for el in elements[:limit]:
            name = el.get("tags", {}).get("name", "Unnamed place")
            street = el.get("tags", {}).get("addr:street", "")
            city = el.get("tags", {}).get("addr:city", "")
            country = el.get("tags", {}).get("addr:country", "")
            lat = el.get("lat", None)
            lon = el.get("lon", None)
            full_addr = ", ".join(filter(None, [street, city, country]))
            coords = f" (Lat: {lat:.5f}, Lon: {lon:.5f})" if lat and lon else ""
            output.append(
                f"- {name}{coords} | {full_addr if full_addr else 'Address not available'}"
            )
        return "\n".join(output)
    except requests.Timeout:
        return "❌ The request to the Overpass API timed out. Please try again."
    except Exception as e:
        return f"❌ Error searching for '{query}' near '{location}': {str(e)}"


location_search_tool = FunctionTool(func=find_nearby_places_open)
