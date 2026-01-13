from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from PIL import Image
import io

app = FastAPI()

# Setup CORS biar bisa ditembak dari Astro lu
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Nanti ganti domain vercel lu kalo mau ketat
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Backend AI is Running!"}

@app.post("/remove-bg")
async def process_image(file: UploadFile = File(...)):
    # 1. Baca gambar upload
    input_image = await file.read()
    
    # 2. Proses Remove BG
    output_image = remove(input_image)
    
    # 3. Return sebagai PNG streaming
    return io.BytesIO(output_image).getvalue()

# Cara return raw bytes agar browser langsung anggap image
from fastapi.responses import Response
@app.post("/api/process")
async def api_process(file: UploadFile = File(...)):
    input_data = await file.read()
    output_data = remove(input_data)
    return Response(content=output_data, media_type="image/png")