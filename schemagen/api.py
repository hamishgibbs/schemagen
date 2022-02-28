from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static/templates")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

def createItemPage():
        # Header (rdfs:label)
        # Whether it is a type, a property, or an annotation (@type)
        # Comment from the type (rdfs:comment)

        # If a Class:
        #    A table of properties (Moving up class inheritance in blocks):
        #    For each inherited class:
        #    Class (rdfs:label)
        #       (rdfs:label) and (@id) link (ns:range) and (rdfs:comment)

        # If a Property:
        # A table of annotations:
        # property (rdfs:label) and (@id) link (ns:range) and (rdfs:comment)

        # If an Annotation:
        # annotation (ns:range) and (rdfs:comment)

        # Create pages for each item in a hierarchy
    return False

def createIndexPage():
        # Create pages for each item in a hierarchy
        # full.html
    return False
