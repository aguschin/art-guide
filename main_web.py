import io

import uvicorn
from decouple import config
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image

from services import run_all_models_web

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # , "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["X-Image-Description"],
)

# todo; this does not work all the times
api_port = int(config("API_PORT"))


def format_header_value(value):
    value = value.encode("ascii", "ignore").decode()
    value = value.replace("\r", "").replace("\n", "<br>").replace("\t", " ")
    value = value.strip()

    return value


@app.post("/process_image_web/")
async def process_image_web(file: UploadFile):
    contents = await file.read()

    pil_image = Image.open(io.BytesIO(contents))

    croped, text = run_all_models_web(pil_image)

    croped = Image.fromarray(croped)

    text = format_header_value(text)

    img_byte_array = io.BytesIO()
    croped.save(img_byte_array, format="PNG")
    img_byte_array = img_byte_array.getvalue()

    return StreamingResponse(
        io.BytesIO(img_byte_array),
        media_type="image/png",
        headers={"X-Image-Description": text},
    )


if __name__ == "__main__":
    uvicorn.run("main_web:app", host="0.0.0.0", port=api_port)
