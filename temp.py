from fastapi import FastAPI, Form, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import model

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")


# Define routes
@app.get("/", response_class=HTMLResponse)
def get_basic_form(request: Request):
    return templates.TemplateResponse("temp.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
def submit_form(request: Request, open: float = Form(...), high: float = Form(...), low: float = Form(...),
                nse_symbol: str = Form(...)):
    model.train_model(nse_symbol)
    pred = model.predict(open, high, low)
    return templates.TemplateResponse("temp.html", {"request": request, "pred": pred})

# Dummy list of stock names for demonstration purposes
stock_names = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "FB", "NFLX", "NVDA", "PYPL", "INTC"]
@app.get("/autocomplete")
async def autocomplete_stock_names(query: str = Query(None, min_length=1)):
    matched_names = [name for name in stock_names if query.lower() in name.lower()]
    return JSONResponse(content=matched_names)
