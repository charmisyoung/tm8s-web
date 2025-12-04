from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class Player(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    api_id: int = Field(index=True, unique=True)
    name: str = Field(index=True)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    search_count: int = Field(default=1)
    careers: List["CareerEntry"] = Relationship(back_populates="player")


class CareerEntry(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    club_name: str
    start_year: int
    end_year: int
    crest_url: Optional[str] = Field(default=None)

    player_id: int = Field(foreign_key="player.id")
    player: Player = Relationship(back_populates="careers")