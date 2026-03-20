from pizza_app.service import get_pizza_recommendation

# 1. Ask the user what they want
print("--- Welcome to the AI Pizza Assistant ---")
user_order = input("What would you like to order today? ")

# 2. Run the recommendation service
result = get_pizza_recommendation(user_order)

# 3. Show the final recommendation
print("\n" + "="*30)
print("FINAL RECOMMENDATION:")
print(result)
print("="*30)