import uvicorn
from decouple import config
from fastapi import FastAPI

from services import run_all_models

app = FastAPI()

verbose = bool(config("DEBUG"))
k_nearest = int(config("DEBUG_KNUMBER"))
api_port = int(config("API_PORT"))


@app.get("/process_image/")
async def process_image(json: dict):
    filename = json.get("filename")
    photo_url = json.get("photo_url")

    response = run_all_models(
        filename, photo_url, verbose=verbose, k_neibours=k_nearest
    )

    return response


if __name__ == "__main__":
    print(api_port)
    uvicorn.run("main:app", host="0.0.0.0", port=api_port)
