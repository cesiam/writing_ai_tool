# Writing Coach

Helps students through the writing process. Helps them in the outlining/brainstorming stage and after the initial first draft. It is meant to encourage an iterative approach to writing, where the student responds to specific feedback given by OpenAI's GPT 5.4-mini to then improve their writing.

## Description

Front-end:
Uses Tailwind CSS and JavaScript to render a basic user interface. Background and accent colors were chosen randomly, though for further development, the colors could be chosen to promote accessibility.

Back-end:
Uses FastAPI to build a simple internal API. Calls the Parley API for LLM models (GPT-5.4-mini). Uses MDConverter to convert documents into Markdown files for better AI results. Enforces structured outputs on all API calls through Pydantic. Uses SQLite as a database, which lives locally. Uses the SQLAlchemy library as the Python interface to the SQL database.

Overall process:
The front-end sends requests to the FastAPI back-end, which validates and structures data using Pydantic, calls the Parley API to generate LLM responses, and persists results to the local SQLite database through SQLAlchemy.

The instructor provides annotations on an exemplar essay along with a simple rubric to give a clearer sense of what is expected of the student. The system uses this information to gauge how well the student is meeting requirements during the pre-writing session, and uses the insights from the exemplar annotations to learn what should be annotated in the student's work.


## Getting Started


## 1. Create and activate a virtual environment

From the project root:

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

`(venv)` appear in your terminal prompt once it's active.

## 2. Install dependencies

Refering to the `requirements.txt` file with the listed packages, run:

```bash
pip install -r requirements.txt
```

Or install them directly:

```bash
pip install "fastapi>=0.110" "sqlalchemy>=2.0" "openai>=1.0" pydantic python-dotenv httpx pytest
```

## 3. Set up environment variables

Create a `.env` file in the project root with your Parley API key and any other required settings:

```
PARLEY_API_KEY=your_key_here
```

## 4. Start the back-end server

From the project root run these commands on the terminal

```bash
cd backend
fastapi dev main.py
```

Replace `main:app` with the correct module and app object name if your entry point is named differently (e.g. `app.main:app`).

By default this serves the API at `http://127.0.0.1:8000`. You can view the interactive API docs at `http://127.0.0.1:8000/docs`.

## 5. Using the /docs interface

FastAPI automatically generates interactive API documentation at `http://127.0.0.1:8000/docs` (Swagger UI) while the back-end server is running. This is useful for testing endpoints without needing the front-end.

To try an endpoint:

1. Open `http://127.0.0.1:8000/docs` in your browser.
2. Click on the endpoint you want to test to expand it.
3. Click the "Try it out" button.
4. Fill in any required parameters or request body fields.
5. Click "Execute" to send the request.
6. Scroll down to see the response, including the status code, response body, and headers.

This is a quick way to confirm the back-end is working correctly and to inspect the structure of requests and responses, since Pydantic models define the expected schemas shown here.

## 6. Start the front-end server

Since the front-end is vanilla HTML/JS/Tailwind, you can serve it with Python's built-in server. From the front-end directory:

```bash
python3 -m http.server 5500
```

Then open `http://127.0.0.1:5500` in your browser.

## 7. Running tests

With the virtual environment active:

```bash
pytest
```

## Notes

- Keep the back-end (`fastapi dev`) and front-end (`http.server`) running in two separate terminal windows/tabs.
- Make sure your front-end's API calls point to the correct back-end URL (e.g. `http://127.0.0.1:8000`).
- Deactivate the virtual environment when done with `deactivate`.


## Version History

* Prototype 0.1
    * See [commit change]()

