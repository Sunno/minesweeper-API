from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from gh_md_to_html import core_converter

from models import Base, Board, Tile
from database import engine, get_db
from schemas import TileSchema, BoardSchemaResponse, BoardSchema

app = FastAPI()
Base.metadata.create_all(engine)


@app.get('/', response_class=HTMLResponse)
def index():
    '''
    Just a welcome message :)
    '''
    with open('./README.md') as readme:
        content = core_converter.markdown(
            readme.read()
        )

    return content


@app.post('/init',
          status_code=status.HTTP_201_CREATED,
          response_model=BoardSchemaResponse)
def new_game(board_data: BoardSchema, db: Session = Depends(get_db)):
    """
    This returns you a new board url
    """
    board = Board(
        status='playing',
        **board_data.dict())
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

    if tile_data.position >= board.grid_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Position cannot be greater than the board size'
        )

    existing_tile = db.query(Tile).filter(
        Tile.board_id == board_id,
        Tile.position == tile_data.position
    ).first()

    if existing_tile and not existing_tile.is_a_mine:
        board.generate_grid(db)
        return board

    tile = Tile(**tile_data.dict())
    tile.board = board
    db.add(tile)
    db.commit()
    db.refresh(tile)

    board.generate_grid(db)
    tile.expand_tile(db)
    board.update_status()
    db.commit()
    return board
