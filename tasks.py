from crewai import Task
from agents import menu_expert

# Task: Recommend pizzas to customer
task1_recommend = Task(
    description="Analyze customer pizza preferences and recommend menu items.",
    expected_output="List of pizza recommendations based on customer preferences.",
    agent=menu_expert
)