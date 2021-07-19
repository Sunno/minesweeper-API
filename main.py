from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Base, Board, Tile
from database import engine, get_db
from schemas import TileSchema, BoardSchemaResponse, BoardSchema

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


@app.post('/init',
          status_code=status.HTTP_201_CREATED,
          response_model=BoardSchemaResponse)
def new_game(board_data: BoardSchema, db: Session = Depends(get_db)):
    """
    This returns you a new board url
    """
    grid_size = board_data.grid_size * board_data.grid_size
    board = Board(
        status='playing',
        grid_size=grid_size, mines_number=board_data.mines_number)
    db.add(board)
    db.commit()
    db.refresh(board)
    board.put_mines(db)
    board.generate_grid(db)
    return board


@app.get('/board/{board_id}', response_model=BoardSchemaResponse)
def get_board(board_id: int, db: Session = Depends(get_db)):
    """
    Returns current board status
    """
    board = db.query(Board).get(board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Board does not exist'
        )
    board.generate_grid(db)
    return board


@app.post('/board/{board_id}/tile',
          status_code=status.HTTP_201_CREATED,
          response_model=BoardSchemaResponse)
def select_tile(board_id: int,
                tile_data: TileSchema,
                db: Session = Depends(get_db)):
    '''
    Selects a tile and sees if it selectes a mine
    Returns the current status of the board
    '''
    board = db.query(Board).get(board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Board does not exist'
        )

    if board.status != 'playing':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This board is not available to play'
        )

    existing_tile = db.query(Tile).filter(
        Tile.board_id == board_id,
        Tile.position == tile_data.position
    ).first()

    if existing_tile and existing_tile.is_a_mine:
        board.status = 'lost'
        tile = Tile(**tile_data.dict())
        tile.board = board
        db.add(tile)
        db.commit()
        board.generate_grid(db, True)
        return board

    tile = Tile(**tile_data.dict())
    tile.board = board
    db.add(tile)
    db.commit()
    db.refresh(tile)

    board.generate_grid(db)
    return board
