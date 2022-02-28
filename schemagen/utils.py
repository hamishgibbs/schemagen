def getClassDependencyDepth(schema, nodeId, start):
    graphClass = schema.graph[schema.graphIndexByNodeID(nodeId)]
    try:
        getClassDependencyDepth(schema, graphClass["rdfs:subClassOf"]["@id"], start.append(1))
    except Exception as e:
        pass
    return sum(start)

def getGraphClassProperties(schema, graphClass, properties=[]):
    properties.append({
        "label": schema.removeKeyContext(graphClass["@id"]),
        "link": schema.resolveKeyContext(graphClass["@id"]),
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

    classProperties = getGraphClassProperties(schema=schema, graphClass=node,
        properties=[])

    tableContents = []
    for group in classProperties:
        formattedGroup = group.copy()
        property_indices = [schema.graphIndexByNodeID(x) for x in group["properties"]]
        formattedGroup["properties"] = [propertyDataForTable(
            schema=schema,
            property=schema.graph[i]) for i in property_indices]
        tableContents.append(formattedGroup)

    return tableContents

def propertyAnnotationDataForTable(schema, node):
    annotation_indices = [schema.graphIndexByNodeID(x) for x in node["ns:annotations"]]
    annotations = [propertyDataForTable(
        schema=schema,
        property=schema.graph[i]) for i in annotation_indices]
    return annotations


def propertyDataForTable(schema, property):
    return {
        "label": property["rdfs:label"],
        "link": schema.resolveKeyContext(property["@id"]),
        "range": property["ns:range"],
        "comment": property["rdfs:comment"]
    }
