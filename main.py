from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from game_logic import Game
from fastapi import Form

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

game = Game()


@app.get("/", include_in_schema=False)
def home(request: Request):
    first_question = game.start_game()
    return templates.TemplateResponse(request, "home.html", {"posts": first_question["question"]})


@app.post("/answer")
async def answer(request: Request, answer: str = Form()):
    q = game.handle_answer(answer)
    if "result" in q:
        game.reset()
        return templates.TemplateResponse(request, "home.html", {"posts": q["result"]})
    return templates.TemplateResponse(request, "home.html", {"posts": q["question"]})


@app.get("/top-animals")
def top_animals():
    """Return the top 10 most likely animals and their probabilities."""
    sorted_animals = sorted(
        game.animal_probs.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    return JSONResponse({
        "animals": [
            {"animal": animal, "probability": round(prob, 6)}
            for animal, prob in sorted_animals
        ]
    })