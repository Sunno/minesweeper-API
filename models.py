from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Board(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    tiles = relationship('Tile', back_populates='game')


class Tile(Base):
    __tablename__ = 'board'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship('Board', back_populates='tiles')
    is_a_mine = Column(Boolean)
