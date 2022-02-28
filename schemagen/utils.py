
def getGraphClassProperties(schema, graphClass, properties={}):
    properties[graphClass["@id"]] = graphClass["ns:properties"]
    try:
        superClass = graphClass["rdfs:subClassOf"]["@id"]
        getGraphClassProperties(
            schema.graph[schema.graphIndexByNodeID(superClass)],
            properties
        )
    except:
        pass
    return properties
