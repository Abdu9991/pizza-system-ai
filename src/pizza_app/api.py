import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from pizza_app.service import get_pizza_recommendation


class RecommendationRequest(BaseModel):
    customer_request: str = Field(..., min_length=1, description="Customer order preferences")


class RecommendationResponse(BaseModel):
    recommendation: str


app = FastAPI(title="Pizza System AI", version="0.1.0")


@app.get("/", response_class=HTMLResponse)
def home() -> str:
        return """
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Pizza System AI</title>
                <style>
                    :root {
                        color-scheme: light;
                        --bg: #fff8ef;
                        --panel: #ffffff;
                        --text: #2b1d14;
                        --muted: #6a5246;
                        --accent: #c2410c;
                        --accent-2: #15803d;
                        --border: #f1d6be;
                    }
                    body {
                        margin: 0;
                        font-family: Georgia, "Times New Roman", serif;
                        background: radial-gradient(circle at top, #ffe7cf 0%, var(--bg) 55%, #fffdf9 100%);
                        color: var(--text);
                    }
                    .wrap {
                        max-inline-size: 780px;
                        margin: 0 auto;
                        padding: 56px 24px;
                    }
                    .card {
                        background: var(--panel);
                        border: 1px solid var(--border);
                        border-radius: 20px;
                        padding: 32px;
                        box-shadow: 0 18px 48px rgba(111, 68, 28, 0.12);
                    }
                    h1 {
                        font-size: clamp(2.2rem, 5vw, 4rem);
                        line-height: 1;
                        margin: 0 0 12px;
                    }
                    p {
                        font-size: 1.05rem;
                        line-height: 1.7;
                        color: var(--muted);
                        margin: 0 0 18px;
                    }
                    .pill {
                        display: inline-block;
                        padding: 8px 12px;
                        border-radius: 999px;
                        background: #fff1e5;
                        color: var(--accent);
                        font-weight: 700;
                        letter-spacing: 0.03em;
                        text-transform: uppercase;
                        font-size: 0.78rem;
                        margin-block-end: 18px;
                    }
                    .endpoints {
                        display: grid;
                        gap: 12px;
                        margin: 24px 0;
                    }
                    .endpoint {
                        border: 1px solid var(--border);
                        border-radius: 14px;
                        padding: 14px 16px;
                        background: #fffaf5;
                    }
                    code {
                        font-family: "Courier New", Courier, monospace;
                        font-size: 0.95rem;
                        color: var(--text);
                    }
                    .ok {
                        color: var(--accent-2);
                        font-weight: 700;
                    }
                </style>
            </head>
            <body>
                <main class="wrap">
                    <section class="card">
                        <div class="pill">Render deployment ready</div>
                        <h1>Pizza System AI</h1>
                        <p>This service exposes a simple pizza recommendation API backed by the CrewAI workflow in this repository.</p>
                        <div class="endpoints">
                            <div class="endpoint"><code>GET /health</code> <span class="ok">for uptime checks</span></div>
                            <div class="endpoint"><code>POST /recommend</code> <span class="ok">for pizza recommendations</span></div>
                        </div>
                        <p>Send JSON like <code>{"customer_request":"I want a spicy chicken pizza with a side"}</code> to the recommendation endpoint.</p>
                    </section>
                </main>
            </body>
        </html>
        """


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest) -> RecommendationResponse:
    try:
        recommendation = get_pizza_recommendation(request.customer_request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to generate recommendation") from exc

    return RecommendationResponse(recommendation=recommendation)


def serve() -> None:
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("pizza_app.api:app", host="0.0.0.0", port=port)