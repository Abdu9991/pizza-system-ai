from crewai import Agent, Crew, Process, Task
from crewai_tools import ScrapeWebsiteTool

MENU_URL = "https://www.dominos.com/en/pages/order/menu"


def get_pizza_recommendation(customer_request: str) -> str:
    request_text = customer_request.strip()
    if not request_text:
        raise ValueError("customer_request must not be empty")

    menu_scrape_tool = ScrapeWebsiteTool(website_url=MENU_URL)
    menu_expert = Agent(
        role="Menu Expert and Food Advisor",
        goal="Provide personalized pizza menu recommendations",
        backstory="You are a pizza expert who helps customers choose the best order.",
        tools=[menu_scrape_tool],
        verbose=True,
    )
    recommend_task = Task(
        description=(
            "Analyze the customer's pizza preferences and recommend menu items. "
            "Customer request: {customer_request}. Use the scraped menu to suggest a "
            "few strong options, explain why they fit, and include useful add-ons or sides."
        ),
        expected_output=(
            "A concise recommendation with pizza choices, short reasons for each choice, "
            "and optional add-ons."
        ),
        agent=menu_expert,
    )
    crew = Crew(
        agents=[menu_expert],
        tasks=[recommend_task],
        process=Process.sequential,
        verbose=True,
    )
    result = crew.kickoff(inputs={"customer_request": request_text})
    return result.raw.strip() if getattr(result, "raw", None) else str(result).strip()