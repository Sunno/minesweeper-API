from random import randint
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship, Session
from database import Base
from settings import GRID_SIZE, GRID_HEIGHT, GRID_WIDTH, MINES_RATE


class Board(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    tiles = relationship('Tile', back_populates='board')
    status = Column(String)

    def generate_grid(self, db, paint_mines=False):
        checked_tiles = db.query(Tile.position).filter(
            Tile.board_id == self.id, Tile.is_a_mine.is_(False)
        ).all()

        checked_tiles = [c[0] for c in checked_tiles]

        mine_tiles = db.query(Tile.position).filter(  # noqa
            Tile.board_id == self.id,
            Tile.is_a_mine.is_(True)
        ).all()
        mine_tiles = [m[0] for m in mine_tiles]

        arr = []
        for idx in range(GRID_SIZE):
            if idx in checked_tiles:
                if idx in mine_tiles:
                    arr.append('*')
                else:
                    arr.append('v')
            elif paint_mines and idx in mine_tiles:
                arr.append('m')
            else:
                arr.append(0)  # TODO calculate the coordinates of mines
        self.grid = arr

    @property
    def url(self):
        return f'/board/{self.id}'

    @property
    def grid_size(self):
        return GRID_WIDTH, GRID_HEIGHT

    def put_mines(self, db: Session):
        mine_number = int(GRID_SIZE * MINES_RATE)
        for _ in range(mine_number):
            position = randint(0, GRID_SIZE - 1)
            existing_tile = db.query(Tile).filter(
                Tile.board_id == self.id,
                Tile.position == position
            )
            # In case it's already assigned
            while not existing_tile:
                position = randint(0, GRID_SIZE - 1)
                existing_tile = db.query(Tile).filter(
                    Tile.board_id == self.id,
                    Tile.position == position
                )
            tile = Tile(
                board_id=self.id,
                position=position,
                is_a_mine=True
            )
            db.add(tile)
        db.commit()


class Tile(Base):
    __tablename__ = 'board'

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, ForeignKey('games.id'))
    board = relationship('Board', back_populates='tiles')
    position = Column(Integer)
    is_a_mine = Column(Boolean, default=False)
