from crewai import Agent
from crewai_tools import ScrapeWebsiteTool

# Tool to scrape pizza menu
menu_scrape_tool = ScrapeWebsiteTool(
    website_url="https://www.dominos.com/en/pages/order/menu"
)

# Menu Expert Agent
menu_expert = Agent(
    role="Menu Expert and Food Advisor",
    goal="Provide personalized menu recommendations",
    backstory="You are a pizza connoisseur helping customers pick the best pizzas.",
    tools=[menu_scrape_tool],
    verbose=True
)