from fastapi import FastAPI
import uvicorn
from services import run_all_models
from decouple import config

app = FastAPI()

verbose = bool(config('DEBUG'))
k_nearest = int(config('DEBUG_KNUMBER'))


@app.get("/process_image/")
async def process_image(json: dict):
    filename = json.get('filename')
    photo_url = json.get('photo_url')

    response = run_all_models(filename, photo_url, verbose=verbose, k_neibours=k_nearest)

    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
