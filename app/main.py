from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ---------------------------------------------------
# Project Paths
# ---------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------
# FastAPI
# ---------------------------------------------------

app = FastAPI(
    title="House Price Prediction",
    description="Machine Learning House Price Prediction using FastAPI",
    version="1.0.0"
)

# ---------------------------------------------------
# Static Files & Templates
# ---------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=ROOT / "app" / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=ROOT / "app" / "templates"
)

# ---------------------------------------------------
# Load Model
# ---------------------------------------------------

pipeline = joblib.load(
    ROOT / "models" / "house_price_pipeline.pkl"
)

# ---------------------------------------------------
# Home Page
# ---------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "prediction": None,
            "OverallQual": None,
            "GrLivArea": None,
            "GarageCars": None,
            "GarageArea": None,
            "TotalBsmtSF": None,
            "FullBath": None,
            "YearBuilt": None,
            "LotArea": None,
            "Neighborhood": None,
            "MSZoning": None
        }
    )

# ---------------------------------------------------
# Prediction
# ---------------------------------------------------

@app.post("/", response_class=HTMLResponse)
def predict(

    request: Request,

    OverallQual: int = Form(...),
    GrLivArea: float = Form(...),
    GarageCars: int = Form(...),
    GarageArea: float = Form(...),
    TotalBsmtSF: float = Form(...),
    FullBath: int = Form(...),
    YearBuilt: int = Form(...),
    LotArea: float = Form(...),
    Neighborhood: str = Form(...),
    MSZoning: str = Form(...)

):

    # Load one sample house
    sample = pd.read_csv(
        ROOT / "data" / "raw" / "train.csv"
    )

    # Remove target
    sample = sample.drop(columns=["SalePrice"])

    # Copy first row
    data = sample.iloc[[0]].copy()

    # Replace with user values

    data["OverallQual"] = OverallQual
    data["GrLivArea"] = GrLivArea
    data["GarageCars"] = GarageCars
    data["GarageArea"] = GarageArea
    data["TotalBsmtSF"] = TotalBsmtSF
    data["FullBath"] = FullBath
    data["YearBuilt"] = YearBuilt
    data["LotArea"] = LotArea
    data["Neighborhood"] = Neighborhood
    data["MSZoning"] = MSZoning

    # Predict

    prediction = pipeline.predict(data)[0]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={

            "prediction": f"${prediction:,.0f}",

            "OverallQual": OverallQual,
            "GrLivArea": GrLivArea,
            "GarageCars": GarageCars,
            "GarageArea": GarageArea,
            "TotalBsmtSF": TotalBsmtSF,
            "FullBath": FullBath,
            "YearBuilt": YearBuilt,
            "LotArea": LotArea,
            "Neighborhood": Neighborhood,
            "MSZoning": MSZoning

        }
    )