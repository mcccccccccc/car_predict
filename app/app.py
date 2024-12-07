import logging

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, ValidationError
from typing import List
from contextlib import asynccontextmanager
import pandas as pd
from sklearn.pipeline import Pipeline
from pipline import get_pipe, prepare_data

pipe: Pipeline

# загружаем pipeline 1 раз при старте сервиса.
@asynccontextmanager
async def lifespan(app: FastAPI):
    global pipe
    # pipe = get_pipe('model_linreg_cars.pkl')
    pipe = get_pipe('model_ridge_cars_brands.pkl')
    yield
    del pipe


app = FastAPI(lifespan=lifespan)


class Item(BaseModel):
    name: str
    year: int
    # selling_price: int # это таргет, он не передается, его надо предсказать
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
    df = prepare_data(df)
    prediction = pipe.predict(df)

    return prediction


@app.post("/predict_items")
def predict_items(items: List[Item]) -> List[float]:
    df = pd.DataFrame([item.model_dump() for item in items])
    df = prepare_data(df)
    predictions = pipe.predict(df)

    return predictions.tolist()

@app.post("/predict_file")
def upload(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
    except Exception:
        raise HTTPException(status_code=500, detail='Error uploading file')
    finally:
        file.file.close()

    try:
        Item(**df.iloc[0].to_dict())
    except ValidationError as e:
        logging.error(e.errors(), exc_info = e)
        raise HTTPException(status_code=500, detail='Error validating file')

    df = prepare_data(df)
    predictions = pipe.predict(df)

    return predictions.tolist()