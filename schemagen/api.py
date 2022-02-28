import csv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/full.html")
async def index():
    classes = [{"node": x, "depth": getClassDependencyDepth(
        schema=schema, nodeId=x["@id"], start=[])}
        for x in schema.graph if x["@type"] == "rdfs:Class"]
    for graphClass in classes:
        if graphClass["depth"] == 0:

    rootClasses = [x for x in classes if x["depth"] == 0]
    classesSorted = sorted(classes, key=lambda d: d['depth'])
    dependencies = []
    for graphClass in classesSorted:
        if graphClass["depth"] == 0:
            dependencies.append({
                "label": graphClass["rdfs:label"],
                "link": resolveKeyContext(graphClass["@id"]),
                "children": []
            })
        else:
            parentIndex = [i for i, x in enumerate(dependencies) if x["label"] == graphClass["rdfs:label"]][0]
            dependencies[parentIndex]["children"].append({
                "label": graphClass["rdfs:label"],
                "link": resolveKeyContext(graphClass["@id"]),
                "children": []
            })

    return classesSorted

    # Ideal format for referencing
    # {"label": , "link": , "children": ,}
    # Organisation
    #   Company
    #   University

@app.get("/{node}", response_class=HTMLResponse)
async def node_page(request: Request, node: str):
    node = schema.graph[schema.graphIndexByNodeID("schema:" + node)]

    response_context = {"request": request,
        "label": node["rdfs:label"],
        "type": schema.removeKeyContext(node["@type"]),
        "comment": node["rdfs:comment"]}

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
