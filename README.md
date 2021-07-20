
# Minesweeper API

Minesweeper game but in an API!

## API Reference

The reference can be checked out and tested in `/docs` from your local installation or in [The demo docs](https://intense-forest-24519.herokuapp.com/docs)

### Design decisions

- The board will be square and the total tiles in the board will be `grid_size * grid_size`
- Like in most tiling games, the representation of the tiles will be in a single array instead of a two dimensional array, this is made because it's faster to access the memory positions in a simple array.
- This app is made for a client app, which will be responsible for the proper representation of the board
- This project makes use of `FastAPI` library and `SQLAlchemy`, because these libraries don't have the boilerplate of a Django project, for example we don't need sessions or user management in this application.

## How to Play

- Create a new game in `/init` endpoint
- You can check out the status of the board in `/board`
- Select a tile by sending a post request to `/board/{board_id}/tile`
- Every endpoint returns the status of the board, possible statuses: `playing`, `won`, `lost`

## Legend

- `0`: Covered tile
- `v`: Selected tile

#### After winning/losing

- `*`: Selected tile that had a mine
- `m`: Mine
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file or environment

`DATABASE_URL`

### Example:

```bash
export DATABASE_URL='sqlite:///game.db'
```

This app supports `Sqlite` and `Postgresql` databases
## Installation

### Requirements
You need to have `Python 3.8` and [Pipenv package manager](https://pipenv.pypa.io/en/latest/) installed

### How-to

Install the project with pipenv

```bash
  pipenv install
```

In case you're developing you can add `--dev` param.
## Run Locally

After installing just run the uvicorn server

```bash
  pipenv run uvicorn main:app --reload
```

By default the app runs in port 8000 http://127.0.0.1:8000
## Demo

You can play the game in my demo deployed in [heroku](https://intense-forest-24519.herokuapp.com/)

  
