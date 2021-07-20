from random import randint
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship, Session
from database import Base
from settings import GRID_SIZE, MINES_RATE


class Board(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    tiles = relationship('Tile', back_populates='board')
    status = Column(String)
    grid_size = Column(Integer, default=GRID_SIZE)
    mines_number = Column(Integer, default=int(GRID_SIZE * MINES_RATE))

    @property
    def grid(self):
        return [0 if self.status == 'playing' and t == 'm' else t
                for t in self._grid]

    @property
    def grid_length(self):
        return self.grid_size * self.grid_size

    def generate_grid(self, db):
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
        for idx in range(self.grid_length):
            if idx in checked_tiles:
                if idx in mine_tiles:
                    arr.append('*')
                else:
                    arr.append('v')
            elif idx in mine_tiles:
                arr.append('m')
            else:
                arr.append(0)  # TODO calculate the coordinates of mines
        self._grid = arr

    @property
    def url(self):
        return f'/board/{self.id}'

    def update_status(self):
        if 0 not in self._grid:
            self.status = 'won'
        elif '*' in self._grid:
            self.status = 'lost'

    def put_mines(self, db: Session):
        for _ in range(self.mines_number):
            position = randint(0, self.grid_length - 1)
            existing_tile = db.query(Tile).filter(
                Tile.board_id == self.id,
                Tile.position == position
            )
            # In case it's already assigned
            while not existing_tile:
                position = randint(0, self.grid_length - 1)
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

    def _get_next_positions(self, current, visited: set):
        positions = []
        vertical_align = current % self.board.grid_size

        next_position = current - self.board.grid_size
        if next_position > 0 and next_position not in visited:
            positions.append(next_position)

        next_position = current + self.board.grid_size
        already_visited = next_position in visited
        if next_position < self.board.grid_length and not already_visited:
            positions.append(next_position)

        next_position = current + 1
        if (next_position % self.board.grid_size) == vertical_align + 1:
            if next_position not in visited:
                positions.append(next_position)

        next_position = current - 1
        if (next_position % self.board.grid_size) == vertical_align - 1:
            if next_position not in visited:
                positions.append(next_position)

        return positions

    def _check_positions(self, positions: list, visited: set):
        '''
        Returns true if there are not adjacent mines
        '''
        [visited.add(p) for p in positions]
        return not any(self.board._grid[p] == 'm' for p in positions)

    def expand_tile(self, db: Session):
        positions_to_check = set()
        positions_visited = set([self.position])

        to_check = self._get_next_positions(self.position, positions_visited)

        if self._check_positions(to_check, positions_visited):
            [
                positions_to_check.add(p)
                for p in to_check
            ]

        while len(positions_to_check) > 0:
            position = positions_to_check.pop()
            to_check = self._get_next_positions(position, positions_visited)

            if self._check_positions(to_check, positions_visited):
                new_tile = Tile(
                    board=self.board,
                    position=position,
                    is_a_mine=False
                )
                db.add(new_tile)
                [
                    positions_to_check.add(p)
                    for p in to_check
                ]
                self.board._grid[position] = 'v'
        db.commit()
