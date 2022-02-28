
def getGraphClassProperties(schema, graphClass, properties=[]):
    properties.append({
        "@id": graphClass["@id"],
        "properties": graphClass["ns:properties"]})
    try:
        superClass = graphClass["rdfs:subClassOf"]["@id"]
        getGraphClassProperties(
            schema=schema,
            graphClass=schema.graph[schema.graphIndexByNodeID(superClass)],
            properties=properties
        )
    except Exception as e:
        print(e)
        pass
    return properties

def classPropertyDataForTable(schema, node):

    classProperties = getGraphClassProperties(schema=schema, graphClass=node)

    res = []
    for group in classProperties:
        property_indices = [schema.graphIndexByNodeID(x) for x in group["properties"]]
        group["properties"] = [propertyDataForTable(
            schema=schema,
            property=schema.graph[i]) for i in property_indices]
        res.append(group)

    return res

def propertyDataForTable(schema, property):
    return {
        "label": property["rdfs:label"],
        "link": schema.resolveKeyContext(property["@id"]),
        "range": property["ns:range"],
        "comment": property["rdfs:comment"]
    }
