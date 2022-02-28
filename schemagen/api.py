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
    propertyAnnotationDataForTable,
    getClassDependencyDepth
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static/templates")

# parse csv schema here
schema = SchemaParser("http://127.0.0.1:8000/")
with open("data/schema.csv") as f:
    reader = csv.reader(f)
    schema.parse_csv_schema(reader)

with open("dist/schemas/schema.jsonld", "w") as f:
    json.dump(schema.JSONLD, f, indent = 4)

@app.get("/")
async def root():
    return RedirectResponse("/full.html")

@app.get("/full.html", response_class=HTMLResponse)
async def index(request: Request):
    # move this out of here
    class_hierarchy = []
    for node in schema.graph:
        if node["@type"] != "rdfs:Class":
            continue

        try:
            parentId = node["rdfs:subClassOf"]["@id"]
        except:
            parentId = node["@id"]
        depth = getClassDependencyDepth(schema=schema,
            nodeId=node["@id"], start=[])

        class_hierarchy.append({
            "parent": parentId,
            "child": node["@id"],
            "depth": depth,
            "label": node["rdfs:label"],
            "link": schema.resolveKeyContext(node["@id"])
        })

    class_hierarchy = sorted(class_hierarchy,
            key=lambda k: (k['parent'], k['depth'], k['child']))
    #schema.pprintJSON(class_hierarchy)

    response_context = {"request": request,
        "classes": class_hierarchy}

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
