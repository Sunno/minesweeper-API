from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Board(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    tiles = relationship('Tile', back_populates='board')


class Tile(Base):
    __tablename__ = 'board'

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, ForeignKey('games.id'))
    board = relationship('Board', back_populates='tiles')
    position = Column(Integer)
    is_a_mine = Column(Boolean, default=False)
