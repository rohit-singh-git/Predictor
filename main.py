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


@app.get("/", response_class=HTMLResponse)
async def get_basic_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def submit_form(request: Request, open: float = Form(...), high: float = Form(...), low: float = Form(...),
                      nse_symbol: str = Form(...)):
    try:
        stock_symbol = None
        for stock in model.stock_list:
            if nse_symbol.lower() in stock["SYMBOL"].lower() or nse_symbol.lower() in stock["NAMEOFCOMPANY"].lower():
                stock_symbol = stock["SYMBOL"]
                break
        if not stock_symbol:
            raise ValueError("Stock not found.")

        model.train_model(stock_symbol)
        pred = model.predict(open, high, low)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return templates.TemplateResponse("index.html", {"request": request, "pred": pred})


@app.get("/autocomplete")
async def autocomplete_stock_names(query: str = Query(..., min_length=1)):
    matched_names = [stock for stock in model.stock_list if
                     query.lower() in stock["SYMBOL"].lower() or query.lower() in stock["NAMEOFCOMPANY"].lower()]
    return JSONResponse(content=matched_names)

