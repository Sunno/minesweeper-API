from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    '''
    Just a welcome message :)
    '''
    return {
        'Welcome': 'Please refer to the docs to know how to play'
    }


@app.post('/init')
def new_game():
    """
    This returns you a new board url
    """
    return {
        'board_url': '/board/10'
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


@app.post('board/tile')
def select_tile():
    '''
    Selects a tile and sees if it selectes a mine
    Returns the current status of the board
    '''
    return {
        'status': 'playing',  # playing | won | lost
        'grid': []
    }
