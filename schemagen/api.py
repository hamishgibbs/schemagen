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
schema = SchemaParser("http://127.0.0.1:8000/")
with open("data/schema.csv") as f:
    reader = csv.reader(f)
    schema.parse_csv_schema(reader)

def propertyDataForTable(property):
    return {
        "label": property["rdfs:label"],
        "link": schema.resolveKeyContext(property["@id"]),
        "range": property["ns:range"],
        "comment": property["rdfs:comment"]
    }

@app.get("/")
async def root():
    return {"message": "Hello World"}

def getGraphClassProperties(graphClass, properties={}):
    properties[graphClass["@id"]] = graphClass["ns:properties"]
    try:
        superClass = graphClass["rdfs:subClassOf"]["@id"]
        getGraphClassProperties(schema.graph[schema.graphIndexByNodeID(superClass)], properties)
    except:
        pass
    return properties


@app.get("/{node}", response_class=HTMLResponse)
async def root(request: Request, node: str):
    node = schema.graph[schema.graphIndexByNodeID("schema:" + node)]

    response_context = {"request": request,
        "label": node["rdfs:label"],
        "type": schema.removeKeyContext(node["@type"]),
        "comment": node["rdfs:comment"]}
    if schema.removeKeyContext(node["@type"]) == "Class":
        # DEV: Add here for inherited properties up the chain
        getGraphClassProperties(node)
        property_indices = [schema.graphIndexByNodeID(x) for x in node["ns:properties"]]
        properties = [propertyDataForTable(schema.graph[i]) for i in property_indices]
        response_context["properties"] = properties
        return templates.TemplateResponse("node.html",
            response_context)

    elif schema.removeKeyContext(node["@type"]) == "Property":
        annotation_indices = [schema.graphIndexByNodeID(x) for x in node["ns:annotations"]]
        annotations = [propertyDataForTable(schema.graph[i]) for i in annotation_indices]
        response_context["properties"] = annotations
        return templates.TemplateResponse("node_with_properties.html",
            response_context)
    else:
        return templates.TemplateResponse("node.html",
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
