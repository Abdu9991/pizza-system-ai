
from pizza_app.service import get_pizza_recommendation


def main() -> None:
	print("--- Welcome to the AI Pizza Assistant ---")
	user_order = input("What would you like to order today? ")
	result = get_pizza_recommendation(user_order)

	print("\n" + "=" * 30)
	print("FINAL RECOMMENDATION:")
	print(result)
	print("=" * 30)


if __name__ == "__main__":
	main()