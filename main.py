from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from cookie import suno_auth, keep_alive

import schemas
from utils import (
    generate_lyrics,
    generate_music,
    get_feed,
    get_lyrics,
    concat_music,
    get_feeds,
)

def get_token():
    try:
        keep_alive(suno_auth)
        token = suno_auth.get_token()
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication token not available.",
            )
        return token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving token: {str(e)}",
        )


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_root():
    return schemas.Response()


@app.post("/generate")
async def generate(
    data: schemas.CustomModeGenerateParam
):
    token = await get_token()
    try:
        data_response = await generate_music(data.dict(), token)
        return data_response
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.post("/generate/description-mode")
async def generate_with_song_description(
    data: schemas.DescriptionModeGenerateParam, token: str = Depends(get_token)
):
    token = await get_token()
    try:
        resp = await generate_music(data.dict(), token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.get("/feed/{aid}")
async def fetch_feed(aid: str):
    token = await get_token()
    try:
        resp = await get_feed(aid, token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.get("/feeds/{aid}")
async def fetch_feed(aid: str):
    token = await get_token()
    try:
        resp = await get_feeds(aid, token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.post("/generate/lyrics/")
async def generate_lyrics_post(
    data: schemas.GenerateLyricsParam
):
    token = await get_token()
    try:
        resp = await generate_lyrics(data.prompt, token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.get("/lyrics/{lid}")
async def fetch_lyrics(lid: str):
    token = await get_token()
    try:
        resp = await get_lyrics(lid, token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.post("/generate/concat")
async def concat(data: schemas.ConcatParam):
    token = await get_token()
    try:
        resp = await concat_music(data.dict(), token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
