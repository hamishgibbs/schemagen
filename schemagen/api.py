import csv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from schemagen.parser import SchemaParser

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static/templates")

# parse csv schema here
schema = SchemaParser("http://127.0.0.1:8000")
with open("data/schema.csv") as f:
    reader = csv.reader(f)
    schema.parse_csv_schema(reader)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/{node}", response_class=HTMLResponse)
async def root(request: Request, node: str):
    node = schema.graph[schema.graphIndexByNodeID("schema:" + node)]
    print(resolveKeyContext(node["@type"], schema.JSONLD["@context"]))
    return templates.TemplateResponse("node.html",
        {"request": request,
        "label": node["rdfs:label"],
        "type": node["@type"],
        "comment": node["rdfs:comment"]})

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
