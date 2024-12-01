from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from contextlib import asynccontextmanager
import pandas as pd
from sklearn.pipeline import Pipeline
from pipline import drop_cols, get_pipe, convert_str_cols

pipe: Pipeline

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pipe
    pipe = get_pipe('model_linreg_cars.pkl')

    yield

    del pipe


app = FastAPI(lifespan=lifespan)


class Item(BaseModel):
    name: str
    year: int
    # selling_price: int
    km_driven: int
    fuel: str
    seller_type: str
    transmission: str
    owner: str
    mileage: str
    engine: str
    max_power: str
    torque: str
    seats: float


class Items(BaseModel):
    objects: List[Item]


@app.post("/predict_item")
def predict_item(item: Item) -> float:
    df = pd.DataFrame(item.model_dump(), index=[0])
    df = drop_cols(df)
    df = convert_str_cols(df)

    prediction = pipe.predict(df)

    return prediction


@app.post("/predict_items")
def predict_items(items: List[Item]) -> List[float]:
    df = pd.DataFrame([item.model_dump() for item in items])
    df = drop_cols(df)
    df = convert_str_cols(df)

    predictions = pipe.predict(df)

    return predictions.tolist()

