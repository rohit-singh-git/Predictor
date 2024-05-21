from fastapi import FastAPI, Form, Request, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import model

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_event():
    await model.cache_stock_info()


# Define routes
@app.get("/", response_class=HTMLResponse)
async def get_basic_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def submit_form(request: Request, open: float = Form(...), high: float = Form(...), low: float = Form(...),
                      nse_symbol: str = Form(...)):
    try:
        stock_symbol = None
        for stock in model.stock_info_cache:
            if nse_symbol.lower() in stock["symbol"].lower() or nse_symbol.lower() in stock["name"].lower():
                stock_symbol = stock["symbol"]
                break
        if not stock_symbol:
            raise ValueError("Stock not found.")
        await model.train_model(nse_symbol)
        pred = model.predict(open, high, low)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return templates.TemplateResponse("index.html", {"request": request, "pred": pred})


@app.get("/autocomplete")
async def autocomplete_stock_names(query: str = Query(..., min_length=1)):
    matched_names = [stock for stock in model.stock_info_cache if
                     query.lower() in stock["symbol"].lower() or query.lower() in stock["name"].lower()]
    return JSONResponse(content=matched_names)
