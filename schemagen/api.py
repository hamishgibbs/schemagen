import csv
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from schemagen.parser import SchemaParser
from schemagen.utils import (
    getGraphClassProperties,
    classPropertyDataForTable,
    propertyAnnotationDataForTable
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static/templates")

# parse csv schema here
schema = SchemaParser("http://127.0.0.1:8000/")
with open("data/schema.csv") as f:
    reader = csv.reader(f)
    schema.parse_csv_schema(reader)

@app.get("/")
async def root():
    return RedirectResponse("/full.html")

@app.get("/full.html", response_class=HTMLResponse)
async def index(request: Request):
    classes = [{"label": x["rdfs:label"],
    "link": schema.resolveKeyContext(x["@id"])}
    for x in schema.graph if x["@type"] == "rdfs:Class"]

    response_context = {"request": request,
        "classes": classes}

    return templates.TemplateResponse("full.html",
        response_context)

@app.get("/{node}", response_class=HTMLResponse)
async def node_page(request: Request, node: str):
    node = schema.graph[schema.graphIndexByNodeID("schema:" + node)]

    response_context = {"request": request,
        "label": node["rdfs:label"],
        "type": schema.removeKeyContext(node["@type"]),
        "comment": node["rdfs:comment"],
        "JSONLD": json.dumps(schema.JSONLD, sort_keys=True, indent=4)}

    if schema.removeKeyContext(node["@type"]) == "Class":
        response_context["properties"] = classPropertyDataForTable(
            schema=schema, node=node)
        td = response_context.copy()
        td.pop("request")
        schema.pprintJSON(td)
        return templates.TemplateResponse("class.html",
            response_context)
    elif schema.removeKeyContext(node["@type"]) == "Property":
        response_context["properties"] = propertyAnnotationDataForTable(
            schema=schema, node=node)
        return templates.TemplateResponse("property.html",
            response_context)
    else:
        return templates.TemplateResponse("base.html",
            response_context)
