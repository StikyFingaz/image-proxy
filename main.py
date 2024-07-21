import os
from brotli_asgi import BrotliMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
import httpx

app = FastAPI()

origins = [
    'http://127.0.0.1:3000',
    'http://127.0.0.1:3001',
    'http://192.168.1.4:3001',
    'https://dktshumen.com',
    'https://www.dktshumen.com',
    'https://nuxt.dktshumen.com',
    'https://test.dktshumen.com',
    'https://festival.dktshumen.com',
    'https://vercel-nuxt-test.nuxt.dev'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Add BrotliMiddleware to enable brotli compression
app.add_middleware(BrotliMiddleware)


# https://cdn.grand-ant.com/cdn-cgi/image/w=500,f=webp/file/dkts-main/media/plays/little-red-riding-hood/photos/7.jpg
@app.get('/{full_path:path}')
async def fetch_image(full_path: str):
    if os.path.exists(f'./{full_path}'):
        return FileResponse(f'./{full_path}')

    return await request_image(full_path)


@app.post('/{full_path}')
async def request_image(full_path: str):
    base_url = 'https://cdn.grand-ant.com'
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{base_url}/{full_path}')

    local_dir = os.path.dirname(f'{full_path}/')
    os.makedirs(os.path.dirname(local_dir), exist_ok=True)
    with open(f'./{full_path}', "wb") as file:
        file.write(response.content)

    return RedirectResponse(f'{base_url}/{full_path}')
