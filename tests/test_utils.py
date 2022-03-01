import pytest
from schemagen.parser import (
    SchemaParser
)
from schemagen.utils import (
    getGraphClassProperties,
    getClassDependencyDepth
)

@pytest.fixture()
def parserFactory():
    return SchemaParser("gfy.org/")

@pytest.fixture()
def dependentClassGraph():
    return [
        {"@id": "schema:Organisation",
         "ns:properties": ["op1", "op2"]},
        {"@id": "schema:Company",
         "rdfs:subClassOf": {"@id": "schema:Organisation"},
         "ns:properties": ["cp1", "cp2"]},
        {"@id": "schema:SmallBusiness",
         "rdfs:subClassOf": {"@id": "schema:Company"},
         "ns:properties": ["sb1", "sb2"]}
    ]


def test_getGraphClassProperties(parserFactory, dependentClassGraph):
    parserFactory.graph = dependentClassGraph
    res = getGraphClassProperties(parserFactory,
        {"@id": "schema:Organisation",
         "ns:properties": ["op1", "op2"]})

    assert res == [
        {"label": "Organisation",
         "link": "gfy.org/Organisation",
         "properties": ["op1", "op2"]}
    ]

def test_getGraphClassProperties_dependent(parserFactory, dependentClassGraph):
    parserFactory.graph = dependentClassGraph
    res = getGraphClassProperties(parserFactory,
        {"@id": "schema:Company",
         "rdfs:subClassOf": "schema:Organisation",
         "ns:properties": ["cp1", "cp2"]})

    assert res == [
        {"label": "Organisation",
         "link": "gfy.org/Organisation",
         "properties": ["op1", "op2"]},
        {"label": "Company",
         "link": "gfy.org/Company",
         "properties": ["cp1", "cp2"]}
    ]

def test_getClassDependencyDepth(parserFactory, dependentClassGraph):
    parserFactory.graph = dependentClassGraph
    res = getClassDependencyDepth(
        schema=parserFactory,
        nodeId="schema:SmallBusiness",
        start=0)
    assert res == 2
