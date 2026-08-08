def build_itinerary_prompt(
    destination: str,
    start_date: str,
    end_date: str,
    budget: str,
    travelers: int,
) -> str:
    return (
        "Create a detailed day-by-day travel itinerary for the following trip. "
        "Use a clear, practical, and friendly tone. "
        "Organize the response by day and include suggested activities, "
        "meal ideas, travel pacing, and any helpful notes for the traveler. "
        "Keep the itinerary realistic and easy to follow.\n\n"
        f"Destination: {destination}\n"
        f"Start Date: {start_date}\n"
        f"End Date: {end_date}\n"
        f"Budget: {budget}\n"
        f"Travelers: {travelers}\n\n"
        "Return only the itinerary.")
