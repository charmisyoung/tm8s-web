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

    # 1. Resolve the raw strings into actual Player objects/records first
    # (We will likely need to tweak services.py to make sure this method 
    # returns both the clean name AND the history)
    player1_record = service.resolve_player(p1) 
    player2_record = service.resolve_player(p2)

    if not player1_record:
        raise HTTPException(status_code=404, detail=f"Player '{p1}' not found in database. Try a different spelling.")
    if not player2_record:
        raise HTTPException(status_code=404, detail=f"Player '{p2}' not found in database. Try a different spelling.")

    # 2. Fetch the club histories using the resolved, standardized records
    # (Assuming your resolve function grabs their canonical ID or exact DB match)
    p1_history = service.get_player_history(player1_record.id)
    p2_history = service.get_player_history(player2_record.id)

    # 3. Run the math engine
    connections = finder.find_player_connections(p1_history, p2_history)

    # 4. Return the beautifully formatted, canonical names back to the frontend UI
    return {
        "player1": player1_record.canonical_name,  # ✅ e.g., "Bernardo Silva"
        "player2": player2_record.canonical_name,  # ✅ e.g., "Abdukodir Khusanov"
        "connections": connections,
        "count": len(connections)
    }
