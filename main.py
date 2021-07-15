from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session

from models import Base, Board, Tile
from database import engine, get_db
from schemas import TileSchema

app = FastAPI()
Base.metadata.create_all(engine)


@app.get('/')
def index():
    '''
    Just a welcome message :)
    '''
    return {
        'Welcome': 'Please refer to the docs to know how to play'
    }


@app.post('/init', status_code=status.HTTP_201_CREATED)
def new_game(db: Session = Depends(get_db)):
    """
    This returns you a new board url
    """
    board = Board()
    db.add(board)
    db.commit()
    db.refresh(board)
    return {
        'board_url': f'/board/{board.id}'
    }


@app.get('/board/{board_id}')
def get_board(board_id: int):
    """
    Returns current board status
    """
    return {
        'status': 'playing',  # playing | won | lost
        'grid': []
    }


@app.post('/board/{board_id}/tile', status_code=status.HTTP_201_CREATED)
def select_tile(board_id: int,
                tile_data: TileSchema, db: Session = Depends(get_db)):
    '''
    Selects a tile and sees if it selectes a mine
    Returns the current status of the board
    '''
    board = db.query(Board).filter(Board.id == board_id).first()
    tile = Tile(**tile_data.dict())
    tile.board = board
    db.add(tile)
    db.commit()
    db.refresh(tile)
    return {
        'status': 'playing',  # playing | won | lost
        'tile': tile,
        'grid': []
    }
