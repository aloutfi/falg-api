from fastapi import FastAPI, Request, HTTPException, status, Cookie, UploadFile, File
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from typing import Optional
from base64 import b64encode
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(docs_url='/')

client_id = os.getenv('SPOTIFY_CLIENT_ID')  # Your client id
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')  # Your secret
redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')  # Your redirect uri


@app.get("/login")
async def login():
    return RedirectResponse(
        url=f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}"
        f"&scope=user-read-private%20user-read-email%20playlist-modify-public%20playlist-modify-private&redirect_uri={redirect_uri}")

@app.get("/callback")
async def callback(code: Optional[str] = None):

    headers = {
        'Authorization': 'Basic ' + b64encode(f"{client_id}:{client_secret}".encode()).decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }
    async with AsyncClient() as client:
        response = await client.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
        response.raise_for_status()

        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']

        headers = {
            'Authorization': f"Bearer {access_token}",
        }
        response = await client.get('https://api.spotify.com/v1/me', headers=headers)
        print(response.json())

    return RedirectResponse(url=f"/#?access_token={access_token}&refresh_token={refresh_token}")


@app.get("/refresh_token")
async def refresh_token(refresh_token: str):
    headers = {
        'Authorization': 'Basic ' + b64encode(f"{client_id}:{client_secret}".encode()).decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    async with AsyncClient() as client:
        response = await client.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
        response.raise_for_status()

        access_token = response.json()['access_token']

    return {"access_token": access_token}

@app.post("/flier")
async def parse_text_from_flier(file: UploadFile = File(...)):
    return "INFRA\nSOUN\nABSTRAKT SONACE\nAES DANA\nALEJO\nAMERICAN GRIME\nANNA MORGAN AXJA BACKLEFT\nBIOLUMIGEN BLACK CARL! BROTHEL\      nCENTRIFIC CHEZ C-MON & KYPSKI (DJ SET)\nCURRA CUT CHEMIST DE-TU DEADCROW\nDMVU x2 EASTWOOD RED EASYJACK\nFREQ GENTLEMENS CLUB x2\nGROUCH       GROUCH IN DUB\nBARNACLE BOI BETAFUSE\nCARBON BASED LIFEFORMS\nCONFIDENTCHILL CROWELL\nDIE BY THE SWORD DJ MADD\nELIOT LIPP ESSEKS FALLS\nG      LADKILL GRIMBLEE GRLL SMTH\nHAMDI\nJ.ADJODHA\nHYPHO\nKODE9 KURSK\nJEN SYMMETRY JON CASEY\nKYPSKI (DJ SET)\nLYNY\nMAD PROFESSOR\nMOONSPLATT      A\nMICKMAN MINDEX\nMAD ZACHx2 MAXFIELD\nMORNING COFFEE MOUSAI MR CARMACK MURKURY MUX MOOL\nN-TYPE X2 NAUTICAL DEVINE NECROMANCER NEVERSKY       OLDBOY\nOOGA OVOID (LIVE) PARKBREEZY PHEEL. POTIONS PUSHLOOP\nR.O REDRUM RESONANT LANGUAGE REVAZZ ROHAAN SAKA\nSKELER SORTOF VAGUE SUBTOLL       SUMTHIN' SUMTHIN' SYNC24\nTERNION SOUND x2 THE AUTONYM THE GLITCH MOB THE WIDDLER\nTHOUGHT PROCESS TUNIC VIBESQUAD XLO\nZEBBLER ENCANTI E      XPERIENCE\n2004\nKEOTA\nKLL BILL\nMACHINEDRUM\nSOUND SYSTEMS BY FUNKTION-ONE, VOID ACOUSTIC & ELEMENT 5\nLIVE MURAL PAINTING BY AARON BROO      KS, APEX COLLECTIVE & MORE\nMAY 18-21, 2023\nHARMONY PARK MUSIC GARDEN-CLARKS GROVE, MN\nPORNMINN\nm\nTI\n4004000"



@app.post("/lineup")
def create_playlist_from_lineup(spotify_user_id: str, lineup_name: str, lineup: str):
    """Creates a playlist of the included lineup for the given spotify user."""
    return "https://open.spotify.com/playlist/1xCc4TruODjgZLRl2mR5Kz?si=cd3e6f02f0644f90"
