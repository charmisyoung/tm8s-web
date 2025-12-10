from fastapi import FastAPI, Depends, HTTPException, Request # 👈 Add Request
from .models import Player, CareerEntry, SearchLog # 👈 Add SearchLog
from sqlmodel import Session
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from .database import create_db_and_tables, get_session
from .services import PlayerService
from .core.connections import ConnectionFinder
from fastapi.middleware.cors import CORSMiddleware

import os
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    """Creates the database file if it doesn't exist on launch"""
    create_db_and_tables()


@app.get("/api/players/search")
def search_players(q: str, session: Session = Depends(get_session)):
    service = PlayerService(session)
    results = service.search_players(q)
    return {"results": results}


@app.get("/api/connections")
def find_connections(
    p1: str, 
    p2: str, 
    request: Request, # 👈 Add this parameter to get IP info
    session: Session = Depends(get_session)
):
    service = PlayerService(session)
    finder = ConnectionFinder()

    # 1. Logic (Keep existing)
    p1_data = service.get_player_data(p1)
    p2_data = service.get_player_data(p2)

    if not p1_data or not p2_data:
        # Log failure before raising error
        log = SearchLog(
            player1=p1, 
            player2=p2, 
            found_connection=False,
            ip_address=request.headers.get("fly-client-ip") or request.client.host
        )
        session.add(log)
        session.commit()
        raise HTTPException(status_code=404, detail="Player not found")

    connections = finder.find_player_connections(p1_data, p2_data)
    
    # 2. Log Success (New Logic)
    # Fly.io passes the real user IP in the 'fly-client-ip' header
    user_ip = request.headers.get("fly-client-ip") or request.client.host
    
    log = SearchLog(
        player1=p1, 
        player2=p2, 
        found_connection=len(connections) > 0,
        ip_address=user_ip
    )
    session.add(log)
    session.commit()

    return {"player1": p1, "player2": p2, "connections": connections, "count": len(connections)}