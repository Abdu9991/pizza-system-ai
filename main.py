import os
from crewai import Crew
from agents import menu_expert
from tasks import task1_recommend 

# 1. Ask the user what they want
print("--- Welcome to the AI Pizza Assistant ---")
user_order = input("What would you like to order today? ")

# 2. Define the Crew
pizza_crew = Crew(
    agents=[menu_expert],
    tasks=[task1_recommend],
    verbose=True # This lets you see the "thinking" process in the terminal
)

# 3. Kickoff the crew using the variable 'user_order'
result = pizza_crew.kickoff(inputs={"customer_request": user_order})

# 4. Show the final recommendation
print("\n" + "="*30)
print("FINAL RECOMMENDATION:")
print(result)
print("="*30)