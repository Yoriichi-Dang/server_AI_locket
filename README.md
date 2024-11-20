# Create AI Server with FASTAPI for Image captioning

## Set up enviroment

**Version of python on mac** : python 3.9

### Install python

```zsh
brew install python@3.9
```

### Create venv and activate

```zsh
python3.9 -m venv venv
source venv/bin/activate
```

### Install library

```zsh
pip install -r requirements.txt
```

### Set up enviroment

```zsh
DATABASE_URL = "postgresql://postgres:<password>@localhost:5432/carla_app"
```

### Run Database

```zsh
alembic revision --autogenerate -m "migration message"
alembic upgrade head
```

### Run FastAPI Server

**Server now localhost:8000**

```zsh
uvicorn main:app --reload
```

### Test api on swagger

```zsh
http://127.0.0.1:8000/docs
```
