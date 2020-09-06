# To The Top Backend

To prepare your shell for development run:
```sh
virtualenv .env
source .env/bin/activate
pip install -r requirements_dev.txt

# Fill the values before running!
export DATABASE_PASSWORD=
export DATABASE_USERNAME=
export DATABASE_NAME=
export COLLECTION_NAME=
export COLLECTION_PASSWORD=
export MONGO_URI_FORMAT=
export AUTH_TOKEN=
export CHUNK_SIZE=
```

To run unit tests run:
```sh
pytest
```

To run the app locally run:
```sh
export FLASK_APP=app.py
flask run

# or
gunicorn app:app --log-level=info
```

Before creatin PR, update the `requirements.txt` file and the `runtime.txt` file!
> Keep the requirements.txt as minimal as possible
```sh
pip freeze > requirements.txt

# Check the Python version to update the runtime.txt file
python -V
```