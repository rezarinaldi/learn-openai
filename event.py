from datetime import datetime

from pydantic import BaseModel, Field
import json
from pm import PromptManager

# 1. Analyze a query if it's contain an event.
# 2. Extract event details
# 3. Event confirmation


class AnalyzeEvent(BaseModel):
    is_event: bool = Field(description="Information of the query if contain an event")
    description: str = Field(description="Description of event")
    confidence_score: float = Field(description="How confidence you are between 0 to 1")


class EventDetail(BaseModel):
    name: str = Field(description="The name of the event")
    description: str = Field(description="The description of the event")
    date_time: str = Field(description="Date time of the event")
    duration: str = Field(description="Duration of the event")


def analyze_event(query):
    pm = PromptManager()
    pm.add_message("user", query)

    result = pm.generate_structured(AnalyzeEvent)
    description = result.get("description")
    is_event = result.get("is_event")
    confidence_score = result.get("confidence_score")

    return description, is_event, confidence_score


def extract_event(query):
    today = datetime.today()
    formatted_date = today.strftime("%Y-%m-%d")

    pm = PromptManager()
    pm.add_message(
        "system",
        f"Extract event details based on user query, as additonal information today's date is {formatted_date}",
    )
    pm.add_message("user", query)

    result = pm.generate_structured(EventDetail)
    return result


def get_current_event():
    return """
    Event List :
    
    - name : Meeting with Product Team
      date : 12 April 2025, 13.00 PM
      duration : 1 hour
      
    - name : Meeting with Investor
      date : 14 April 2025, 10.00 AM
      duration : 2 hour
    """


def aggregate_event(current_event: str, new_event: str):
    pm = PromptManager()
    pm.add_message(
        "system",
        f"You have list of user's current events, and check if its already exist. Here is the event: {current_event}",
    )
    pm.add_message("user", new_event)

    result = pm.generate()
    return result


def generate_confirmation(query):
    pm = PromptManager()
    pm.add_message(
        "system",
        """
        Create a confirmation message to the user, and ask if it's confirmed.
        
        EXAMPLE RESPONSE OUTPUT:
        Hey, i will make an event for your with this details: follow with the event details.
        Let me know if it's good!
        """,
    )
    pm.add_message("user", query)

    return pm.generate()


def run():
    input_query = input("Query: ")
    description, is_event, confidence_score = analyze_event(input_query)

    if is_event and confidence_score > 0.7:
        current_event = get_current_event()
        new_event = json.dumps(extract_event(description))

        agg_result = aggregate_event(current_event, new_event)
        print(agg_result)

    else:
        print("Not event!")


if __name__ == "__main__":
    run()
