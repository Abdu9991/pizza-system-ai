import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

logger = logging.getLogger("pizza_api")

from pizza_app.service import get_pizza_recommendation


class RecommendationRequest(BaseModel):
    customer_request: str = Field(..., min_length=1, description="Customer order preferences")


class RecommendationResponse(BaseModel):
    recommendation: str


app = FastAPI(title="Pizza System AI", version="0.1.0")


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pizza System AI</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; }
    :root {
      --bg: #fff8ef;
      --panel: #ffffff;
      --text: #2b1d14;
      --muted: #6a5246;
      --accent: #c2410c;
      --accent-hover: #9a3209;
      --accent-2: #15803d;
      --border: #f1d6be;
      --input-bg: #fffaf6;
      --result-bg: #f9f4ee;
    }
    body {
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      background: radial-gradient(circle at top, #ffe7cf 0%, var(--bg) 55%, #fffdf9 100%);
      min-height: 100vh;
      color: var(--text);
    }
    .wrap {
      max-width: 700px;
      margin: 0 auto;
      padding: 48px 20px 80px;
    }
    .pill {
      display: inline-block;
      padding: 6px 14px;
      border-radius: 999px;
      background: #fff1e5;
      color: var(--accent);
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      font-size: 0.72rem;
      margin-bottom: 14px;
    }
    h1 {
      font-size: clamp(2rem, 6vw, 3.4rem);
      line-height: 1.05;
      margin: 0 0 10px;
    }
    .tagline {
      font-size: 1.05rem;
      color: var(--muted);
      margin: 0 0 36px;
      line-height: 1.65;
    }
    /* ORDER CARD */
    .card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 32px 32px 28px;
      box-shadow: 0 18px 48px rgba(111,68,28,0.11);
    }
    .card h2 {
      margin: 0 0 6px;
      font-size: 1.4rem;
    }
    .card .sub {
      font-size: 0.92rem;
      color: var(--muted);
      margin: 0 0 20px;
    }
    textarea {
      width: 100%;
      min-height: 110px;
      resize: vertical;
      border: 1.5px solid var(--border);
      border-radius: 12px;
      padding: 14px 16px;
      font-family: inherit;
      font-size: 1rem;
      color: var(--text);
      background: var(--input-bg);
      outline: none;
      transition: border-color .2s;
      line-height: 1.6;
    }
    textarea:focus { border-color: var(--accent); }
    textarea::placeholder { color: #bfa99a; }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      margin-top: 14px;
      padding: 13px 28px;
      background: var(--accent);
      color: #fff;
      font-family: inherit;
      font-size: 1rem;
      font-weight: 700;
      border: none;
      border-radius: 12px;
      cursor: pointer;
      transition: background .18s, opacity .18s;
    }
    .btn:hover:not(:disabled) { background: var(--accent-hover); }
    .btn:disabled { opacity: 0.55; cursor: not-allowed; }
    .spinner {
      width: 16px; height: 16px;
      border: 2px solid rgba(255,255,255,.35);
      border-top-color: #fff;
      border-radius: 50%;
      animation: spin .7s linear infinite;
      display: none;
    }
    .btn.loading .spinner { display: block; }
    .btn.loading .btn-text { opacity: .75; }
    @keyframes spin { to { transform: rotate(360deg); } }
    /* RESULT */
    #result-box {
      display: none;
      margin-top: 24px;
      border-top: 1px solid var(--border);
      padding-top: 20px;
    }
    #result-box h3 {
      margin: 0 0 10px;
      font-size: 1.1rem;
      color: var(--accent-2);
    }
    #result-text {
      background: var(--result-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 18px;
      font-size: 0.97rem;
      line-height: 1.75;
      white-space: pre-wrap;
      color: var(--text);
    }
    .error-msg {
      color: #b91c1c;
      background: #fff1f1;
      border: 1px solid #fecaca;
      border-radius: 12px;
      padding: 14px 16px;
      font-size: 0.95rem;
    }
    /* API INFO */
    .api-info {
      margin-top: 32px;
      padding: 20px 24px;
      background: #fffaf5;
      border: 1px solid var(--border);
      border-radius: 14px;
    }
    .api-info h3 {
      margin: 0 0 12px;
      font-size: 1rem;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: .05em;
      font-size: .78rem;
    }
    .ep { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; font-size: .92rem; }
    code {
      font-family: "Courier New", Courier, monospace;
      font-size: .88rem;
      background: #f5ebe0;
      padding: 2px 7px;
      border-radius: 6px;
      color: var(--text);
    }
    .ok { color: var(--accent-2); font-size: .88rem; }
  </style>
</head>
<body>
<main class="wrap">
  <div class="pill">Render deployment ready</div>
  <h1>🍕 Pizza System AI</h1>
  <p class="tagline">
    Tell us what you're craving and our AI crew will craft the perfect pizza recommendation for you.
  </p>

  <div class="card">
    <h2>Place Your Order</h2>
    <p class="sub">Describe what you feel like — toppings, crust, spice level, sides, anything.</p>

    <textarea
      id="order-input"
      placeholder="e.g. I want a spicy chicken pizza with a thin crust and garlic bread on the side…"
      rows="4"
    ></textarea>

    <button class="btn" id="submit-btn" onclick="submitOrder()">
      <span class="btn-text">Get Recommendation</span>
      <span class="spinner"></span>
    </button>

    <div id="result-box">
      <h3>🧑‍🍳 Your Recommendation</h3>
      <div id="result-text"></div>
    </div>
  </div>

  <div class="api-info">
    <h3>REST API Endpoints</h3>
    <div class="ep"><code>GET /health</code><span class="ok">uptime check</span></div>
    <div class="ep"><code>POST /recommend</code><span class="ok">JSON: {"customer_request":"…"}</span></div>
  </div>
</main>

<script>
  async function submitOrder() {
    const input = document.getElementById('order-input');
    const btn = document.getElementById('submit-btn');
    const resultBox = document.getElementById('result-box');
    const resultText = document.getElementById('result-text');

    const order = input.value.trim();
    if (!order) {
      input.focus();
      return;
    }

    btn.disabled = true;
    btn.classList.add('loading');
    btn.querySelector('.btn-text').textContent = 'Working on it…';
    resultBox.style.display = 'none';

    try {
      const res = await fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ customer_request: order }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
        resultText.className = 'error-msg';
        resultText.textContent = '⚠️ ' + (err.detail || 'Something went wrong. Please try again.');
      } else {
        const data = await res.json();
        resultText.className = '';
        resultText.textContent = data.recommendation;
      }
    } catch (e) {
      resultText.className = 'error-msg';
      resultText.textContent = '⚠️ Could not reach the server. Please check your connection.';
    } finally {
      btn.disabled = false;
      btn.classList.remove('loading');
      btn.querySelector('.btn-text').textContent = 'Get Recommendation';
      resultBox.style.display = 'block';
    }
  }

  document.getElementById('order-input').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) submitOrder();
  });
</script>
</body>
</html>"""


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
        logger.exception("Recommendation failed")
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendation: {exc}") from exc

    return RecommendationResponse(recommendation=recommendation)


def serve() -> None:
    import uvicorn

    port = int(os.getenv("PORT", "8082"))
    uvicorn.run("pizza_app.api:app", host="0.0.0.0", port=port)