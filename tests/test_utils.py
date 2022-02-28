import pytest
from schemagen.parser import (
    SchemaParser
)
from schemagen.utils import getGraphClassProperties

@pytest.fixture()
def parserFactory():
    return SchemaParser("gfy.org/")

@pytest.fixture()
def dependentClassGraph():
    return [
        {"@id": "schema:Organisation",
         "ns:properties": ["op1", "op2"]},
        {"@id": "schema:Company",
         "rdfs:subClassOf": "schema:Organisation",
         "ns:properties": ["cp1", "cp2"]}
    ]


def test_getGraphClassProperties(parserFactory, dependentClassGraph):
    parserFactory.graph = dependentClassGraph
    res = getGraphClassProperties(parserFactory,
        {"@id": "schema:Organisation",
         "ns:properties": ["op1", "op2"]})

    assert res == {"schema:Organisation": ["op1", "op2"]}

def test_getGraphClassProperties_dependent(parserFactory, dependentClassGraph):
    parserFactory.graph = dependentClassGraph
    res = getGraphClassProperties(parserFactory,
        {"@id": "schema:Company",
         "rdfs:subClassOf": "schema:Organisation",
         "ns:properties": ["cp1", "cp2"]})

    assert res == {"schema:Organisation": ["op1", "op2"],
                   "schema:Company": ["cp1", "cp2"]}
