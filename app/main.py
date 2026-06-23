from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from .database import create_db_and_tables, get_session
from .services import PlayerService
from .core.connections import ConnectionFinder
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
def read_root():
    return {"status": "tm8s API is running"}


@app.get("/api/players/search")
def search_players(q: str, session: Session = Depends(get_session)):
    service = PlayerService(session)
    results = service.search_players(q)
    return {"results": results}


@app.get("/api/connections")
def find_connections(p1: str, p2: str, session: Session = Depends(get_session)):
    service = PlayerService(session)
    finder = ConnectionFinder()

    # 1. Fetch data (this now returns the dictionary we just created)
    p1_data = service.get_player_data(p1)
    p2_data = service.get_player_data(p2)

    # 2. Check if they exist
    if not p1_data:
        raise HTTPException(status_code=404, detail=f"Player '{p1}' not found in database.")
    if not p2_data:
        raise HTTPException(status_code=404, detail=f"Player '{p2}' not found in database.")

    # 3. Extract the history lists to feed into the mathematical engine
    p1_history = p1_data["history"]
    p2_history = p2_data["history"]

    # 4. Run the overlap logic
    connections = finder.find_player_connections(p1_history, p2_history)

    # 5. Return the CANONICAL names back to the frontend UI
    return {
        "player1": p1_data["name"],  # ✅ FIXED: E.g., "Bernardo Silva"
        "player2": p2_data["name"],  # ✅ FIXED: E.g., "Abdukodir Khusanov"
        "connections": connections,
        "count": len(connections)
    }
