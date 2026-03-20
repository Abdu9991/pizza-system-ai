#!/usr/bin/env python
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from datetime import datetime
from pizza_app.crew import PizzaApp

app = FastAPI(title="Pizza AI Ordering System")

@app.get("/")
def health_check():
    return {"status": "active", "service": "PizzaApp Crew"}

@app.get("/order")
def run_order(customer_request: str):
    """
    Production endpoint to trigger the crew via URL.
    Example: /order?customer_request=2 large pepperoni pizzas
    """
    inputs = {
        'customer_request': customer_request,
        'current_year': str(datetime.now().year)
    }

    try:
        # Kickoff the crew and return the result as JSON
        result = PizzaApp().crew().kickoff(inputs=inputs)
        return {"recommendation": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crew execution failed: {e}")

# Keep your original CLI 'run' logic for local testing
def run():
    inputs = {
        'customer_request': 'I want 2 large pepperoni pizzas',
        'current_year': str(datetime.now().year)
    }
    PizzaApp().crew().kickoff(inputs=inputs)

# Entry point for Render/Production
if __name__ == "__main__":
    # Render provides a $PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    # Run the web server
    uvicorn.run(app, host="0.0.0.0", port=port)