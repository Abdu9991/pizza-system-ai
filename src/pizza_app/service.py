from crewai import Agent, Crew, Process, Task

# Built-in menu — no external scraping needed, works reliably on every platform.
PIZZA_MENU = """
=== PIZZA MENU ===

CLASSIC PIZZAS
- Margherita        — tomato sauce, fresh mozzarella, basil
- Pepperoni         — tomato sauce, mozzarella, pepperoni
- BBQ Chicken       — BBQ sauce, grilled chicken, red onion, mozzarella
- Veggie Supreme    — tomato sauce, bell peppers, mushrooms, olives, red onion, mozzarella
- Meat Feast        — pepperoni, sausage, ham, bacon, beef, mozzarella
- Hawaiian          — tomato sauce, ham, pineapple, mozzarella

SPICY PIZZAS
- Spicy Chicken     — hot sauce base, spicy chicken, jalapeños, red onion, mozzarella
- Diavola           — tomato sauce, spicy salami, chilli flakes, mozzarella
- Inferno           — ghost-pepper sauce, pepperoni, jalapeños, habanero drizzle

SPECIALTY PIZZAS
- Truffle Mushroom  — truffle oil, mixed mushrooms, parmesan, rocket
- Four Cheese       — mozzarella, cheddar, parmesan, gorgonzola
- Seafood Delight   — tomato sauce, prawns, calamari, garlic, mozzarella

CRUST OPTIONS
- Thin & Crispy  |  Classic Hand-Tossed  |  Thick Pan  |  Stuffed Crust (+ $2)

SIZES
- Small (6")  |  Medium (10")  |  Large (14")  |  XL Party (18")

SIDES
- Garlic Bread        - Cheesy Garlic Bread
- Chicken Wings (6/12) - Buffalo Wings
- Mozzarella Sticks   - Loaded Potato Wedges
- Garden Salad        - Caesar Salad

DRINKS
- Soft Drinks (330ml / 1.5L)  |  Fresh Lemonade  |  Sparkling Water

DESSERTS
- Chocolate Lava Cake  |  Tiramisu Slice  |  Cookie Dough

DEALS
- Family Meal Deal: XL pizza + 2 sides + 2 drinks — $29.99
- 2-for-1 Tuesdays: any two medium pizzas — buy one get one free
- Student Discount: 15% off with valid student ID
"""


def get_pizza_recommendation(customer_request: str) -> str:
    request_text = customer_request.strip()
    if not request_text:
        raise ValueError("customer_request must not be empty")

    menu_expert = Agent(
        role="Pizza Menu Expert and Food Advisor",
        goal="Provide friendly, personalised pizza recommendations based on the menu.",
        backstory=(
            "You are an enthusiastic pizza expert who knows the menu inside-out. "
            "You listen carefully to what the customer wants and suggest the best "
            "options with clear reasons, never recommending items not on the menu."
        ),
        verbose=True,
    )
    recommend_task = Task(
        description=(
            "Use the menu below to recommend pizzas and sides for the customer.\n\n"
            f"{PIZZA_MENU}\n\n"
            "Customer request: {customer_request}\n\n"
            "Suggest 1-3 specific menu items that best match the request. "
            "For each, give a brief reason why it fits. "
            "Mention any relevant deals or sides that complement the order. "
            "Keep the response friendly and concise (under 200 words)."
        ),
        expected_output=(
            "A friendly recommendation listing 1-3 pizza options from the menu, "
            "a short reason for each, and any relevant sides or deals."
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