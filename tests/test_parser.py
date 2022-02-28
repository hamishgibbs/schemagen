import csv
import pytest
from schemagen.parser import (
    SchemaParser
)

@pytest.fixture()
def parserFactory():
    return SchemaParser("gfy.org")


def test_parseSchemaRow(parserFactory):
    csvRow = [''] * 6
    res = parserFactory.parseSchemaRow(csvRow)
    exp_keys = ['class', 'superClass', 'property', 'annotation',
                'valueType', 'comment']
    assert list(res.keys()) == exp_keys

def test_appendBaseUrl(parserFactory):
    res = parserFactory.appendBaseUrl("Person")
    assert res == "schema:Person"

def test_createGraphClass_noninherited(parserFactory):
    inputRow = {"class": "Person", "comment": "A Person", "superClass":''}
    res = parserFactory.createGraphClass(inputRow)
    assert res["@id"] == "schema:Person"
    assert res["rdfs:comment"] == "A Person"
    assert res["rdfs:label"] == "Person"

    with pytest.raises(KeyError):
        res["rdfs:subClassOf"]


def test_createGraphClass_inherited(parserFactory):
    inputRow = {"class": "Person", "comment": "A Person", "superClass":'Thing'}
    res = parserFactory.createGraphClass(inputRow)
    assert res["rdfs:subClassOf"] == {"@id": 'schema:Thing'}

def test_createGraphProperty(parserFactory):
    inputRow = {"property": "born", "comment": "Birth date", "valueType":'ISODate'}
    res = parserFactory.createGraphProperty(inputRow)
    assert res["@id"] == "schema:born"
    assert res["rdfs:comment"] == "Birth date"
    assert res["rdfs:label"] == "born"
    assert res["ns:range"] == "ISODate"

def test_createGraphAnnotation(parserFactory):
    inputRow = {"annotation": "startDate", "comment": "Starting date", "valueType":'ISODate'}
    res = parserFactory.createGraphAnnotation(inputRow)
    assert res["@id"] == "schema:startDate"
    assert res["rdfs:comment"] == "Starting date"
    assert res["rdfs:label"] == "startDate"
    assert res["ns:range"] == "ISODate"

def test_graphIndexByNodeID(parserFactory):
    parserFactory.graph = [{"@id": "schema:Animal"}, {"@id": "schema:Person"}]
    res = parserFactory.graphIndexByNodeID("schema:Person")
    assert res == 1

def test_appendPropertyToActiveClass(parserFactory):
    parserFactory.graph = [{"@id": "schema:Animal", "ns:properties": []}]
    parserFactory.activeClass = "schema:Animal"
    parserFactory.appendPropertyToActiveClass("schema:born")
    assert len(parserFactory.graph[0]["ns:properties"]) == 1

def test_appendAnnotationToActiveProperty(parserFactory):
    parserFactory.graph = [{"@id": "schema:almaMater", "ns:annotations": []}]
    parserFactory.activeProperty = "schema:almaMater"
    parserFactory.appendAnnotationToActiveProperty("schema:enrollmentDate")
    assert len(parserFactory.graph[0]["ns:annotations"]) == 1

def test_SchemaParser():

    parser = SchemaParser("gfy.org")

    with open("data/schema.csv") as f:
        reader = csv.reader(f)
        parser.parse_csv_schema(reader)

    # print(parser.pprintGraph())

    assert True

# There need to be lots of tests for every key value pair
