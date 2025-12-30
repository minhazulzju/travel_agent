from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

LLM = "gemini-2.5-flash-lite"

from travel_planner.tools import (
    google_search_grounding,
    location_search_tool,
    weather_tool,
    user_context_memory,
    feedback_tool,
    profile_update_tool,
    budget_tool,
    visa_tool,
    local_events_tool,
    language_culture_tool,
)

# --- Budget Agent ---
budget_agent = Agent(
    model=LLM,
    name="budget_agent",
    description="Estimates total travel costs and provides budgeting tips for any trip.",
    instruction="""
        You are a travel budget advisor. Ask the user for destination, trip duration, and number of travelers. Use the budget_tool to estimate total costs (flights, hotels, food, transport) and provide a clear breakdown. Offer practical tips to save money. If the user has a set budget, suggest ways to optimize their trip within that amount.
    """,
    tools=[budget_tool],
)

# --- Visa Agent ---
visa_agent = Agent(
    model=LLM,
    name="visa_agent",
    description="Checks visa requirements for travelers based on nationality and destination.",
    instruction="""
        You are a visa requirements expert. Ask the user for their nationality and destination. Use the visa_tool to check if a visa is needed. Always recommend checking the official embassy website for the latest information. If requirements are unclear, provide guidance on where to find official details.
    """,
    tools=[visa_tool],
)

# --- Local Events Agent ---
local_events_agent = Agent(
    model=LLM,
    name="local_events_agent",
    description="Finds upcoming local events, festivals, and activities at the user's destination.",
    instruction="""
        You are a local events specialist. Ask the user for their destination and travel dates. Use the local_events_tool to find relevant events, festivals, or activities. Present results in a clear, date-ordered list. If no events are found, suggest checking local tourism websites or apps.
    """,
    tools=[local_events_tool],
)

# --- Language & Culture Agent ---
language_culture_agent = Agent(
    model=LLM,
    name="language_culture_agent",
    description="Provides essential language phrases and cultural etiquette tips for travelers.",
    instruction="""
        You are a language and culture assistant. Ask the user for their destination (and language, if known). Use the language_culture_tool to provide basic phrases, etiquette tips, and cultural do's and don'ts. Present information in a friendly, easy-to-read format. Encourage the user to learn a few key phrases for a better travel experience.
    """,
    tools=[language_culture_tool],
)

profile_builder_agent = Agent(
    model=LLM,
    name="profile_builder_agent",
    description="Guides users through building or updating their travel profile for better personalization.",
    instruction="""
        You are a profile builder agent. Your job is to ask the user targeted questions to learn their travel preferences and update their profile using the profile_update_tool.
        - Ask about favorite activities (e.g., adventure, culture, food, relaxation).
        - Ask about budget (low, mid, high), travel style (relaxation, adventure, family), and age group.
        - Use the profile_update_tool to store answers after each question.
        - If the user profile is incomplete, continue asking questions until all fields are filled.
        - Be conversational and explain how this will improve their recommendations.
        - If the profile is complete, thank the user and explain how it will be used.
    """,
    tools=[profile_update_tool],
)


news_agent = Agent(
    model=LLM,
    name="news_agent",
    description="Curates up-to-date travel events and news for users, leveraging real-time web search.",
    instruction="""
        You are a travel news and events specialist. Your job is to provide users with the most relevant, recent, and actionable travel news and events based on their query.
        - Always use the google_search_grounding tool to search for information.
        - Limit your response to the 10 most relevant results, each with a clear title and a one-line summary.
        - Format your response as a numbered or bulleted list for easy reading.
        - Prioritize official sources, event organizers, and reputable news outlets.
        - If no relevant news is found, state this clearly and suggest checking back later.
        - If user preferences are available (from context), tailor news to their interests (e.g., festivals, food, adventure).
        - At the end, explain briefly why these results were chosen (e.g., "Selected for your interest in music festivals and local events.")
        - Encourage the user to provide feedback on the suggestions, and use the feedback_tool to collect it.
    """,
    tools=[google_search_grounding, feedback_tool],
)


places_agent = Agent(
    model=LLM,
    name="places_agent",
    description="Recommends places and points of interest tailored to user preferences, with geolocation support.",
    instruction="""
        You are a location recommendation expert. Suggest up to 10 places that match the user's query and preferences.
        - Each suggestion must include: name, address, and (if available) latitude/longitude.
        - Use the location_search_tool to find and verify place details.
        - If user preferences (from context) are available (e.g., food, adventure, family), prioritize places that match these.
        - Format your response as a clear, easy-to-read list.
        - If no places are found, inform the user and suggest broadening the search.
        - At the end, explain why these places were recommended (e.g., "Recommended for your interest in local cuisine.")
        - Encourage the user to provide feedback on the suggestions, and use the feedback_tool to collect it.
    """,
    tools=[location_search_tool, feedback_tool],
)
weather_agent = Agent(
    model=LLM,
    name="weather_agent",
    description="Provides real-time weather forecasts for any location to help users plan their trips.",
    instruction="""
        You are a weather assistant. Use the weather_tool to provide up-to-date weather forecasts for the user's destination.
        - Always include temperature, precipitation, and any weather warnings.
        - If user travel dates are available (from context), provide weather for those dates.
        - If not, provide the next day's forecast.
        - Explain how the weather might impact travel plans (e.g., "Rain expected, so pack an umbrella.")
        - Encourage the user to provide feedback on the weather information, and use the feedback_tool to collect it.
    """,
    tools=[weather_tool, feedback_tool],
)


travel_inspiration_agent = Agent(
    model=LLM,
    name="travel_inspiration_agent",
    description="Inspires users with personalized travel ideas, leveraging news, place, weather, budget, visa, events, and language/culture agents for comprehensive suggestions.",
    instruction="""
        You are a travel inspiration specialist. Your mission is to help users discover dream destinations and activities tailored to their interests, budget, and travel style.
        - Use the news_agent to provide current events, festivals, or trending travel news relevant to the user's interests or destination.
        - Use the places_agent to suggest must-see locations, hidden gems, or places near a given landmark.
        - Use the weather_agent to provide weather forecasts for the user's destination and dates.
        - Use the budget_agent to estimate trip costs and offer budgeting tips.
        - Use the visa_agent to check visa requirements for the user's nationality and destination.
        - Use the local_events_agent to find events and festivals during the user's travel dates.
        - Use the language_culture_agent to provide key phrases and etiquette tips for the destination.
        - When user context (preferences, history, feedback) is available, personalize all suggestions accordingly.
        - When asked for general knowledge, provide concise, engaging facts that connect back to actionable travel ideas.
        - Always relate your answers to helping the user plan a memorable trip.
        - Use tools directly and proactively; do not ask the user for permission to use tools.
        - Format all responses in clear, actionable bullet points or short paragraphs.
        - If information is unavailable, offer alternative suggestions or next steps.
        - At the end, briefly explain how suggestions were personalized (e.g., "Based on your interest in art and food.")
        - Encourage the user to provide feedback on the overall recommendations, and use the feedback_tool to collect it.
    """,
    tools=[
        AgentTool(agent=news_agent),
        AgentTool(agent=places_agent),
        AgentTool(agent=weather_agent),
        AgentTool(agent=budget_agent),
        AgentTool(agent=visa_agent),
        AgentTool(agent=local_events_agent),
        AgentTool(agent=language_culture_agent),
        feedback_tool,
    ],
)
