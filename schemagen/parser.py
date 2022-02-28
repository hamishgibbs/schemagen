import json

# I think this is actually not a SchemaParser but should instead
# be two objects - a schema parser and a schema
class SchemaParser():
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.activeClass = None
        self.activeProperty = None
        self.graph = []
        self.JSONLD = self.graphAsJSONLD()

    def parse_csv_schema(self, reader):

        for i, csvRow in enumerate(reader):
            if i == 0:
                continue
            row = self.parseSchemaRow(csvRow)

            if row['class'] != '':
                graphClass = self.createGraphClass(row)
                self.activeClass = graphClass["@id"]
                self.graph.append(graphClass)
            elif row['property'] != '':
                graphProperty = self.createGraphProperty(row)
                self.activeProperty = graphProperty["@id"]
                self.graph.append(graphProperty)
                self.appendPropertyToActiveClass(graphProperty["@id"])
            elif row['annotation'] != '':
                graphAnnotation = self.createGraphAnnotation(row)
                self.graph.append(graphAnnotation)
                self.appendAnnotationToActiveProperty(graphAnnotation["@id"])
            else:
                pass

    def parseSchemaRow(self, row):
        return {
            'class': row[0],
            'superClass': row[1],
            'property': row[2],
            'annotation': row[3],
            'valueType': row[4],
            'comment': row[5]}

    def appendBaseUrl(self, label):
        return "schema:" + label

    def createGraphClass(self, row):

        node = {"@id": self.appendBaseUrl(row["class"]),
                "@type": "rdfs:Class",
                "rdfs:comment": row["comment"],
                "rdfs:label": row["class"],
                "ns:properties": []}

        if row["superClass"] != '':
            node["rdfs:subClassOf"] = {
               # DEV: Currently cannot use definitions in other schemas
               # DEV: Can only be a subclass of one type
               "@id": self.appendBaseUrl(row["superClass"])
            }

        return node

    def createGraphProperty(self, row):

        node = {"@id": self.appendBaseUrl(row["property"]),
                "@type": "rdfs:Property",
                "rdfs:comment": row["comment"],
                "rdfs:label": row["property"],
                "ns:annotations": [],
                "ns:range": row["valueType"]}

        return node

    def createGraphAnnotation(self, row):

        node = {"@id": self.appendBaseUrl(row["annotation"]),
                "@type": "Annotation",
                "rdfs:comment": row["comment"],
                "rdfs:label": row["annotation"],
                "ns:range": row["valueType"]}

        return node

    def graphIndexByNodeID(self, id):

        activeClassIndex = [
            i for i, x in enumerate(self.graph) if x["@id"] == id
        ]
        return activeClassIndex[0]

    def appendPropertyToActiveClass(self, graphPropertyId):

        activeClassIndex = self.graphIndexByNodeID(self.activeClass)
        self.graph[activeClassIndex]["ns:properties"].append(graphPropertyId)

    def appendAnnotationToActiveProperty(self, graphAnnotationId):

        activePropertyIndex = self.graphIndexByNodeID(self.activeProperty)
        self.graph[activePropertyIndex]["ns:annotations"].append(graphAnnotationId)

    def pprintGraph(self):
        print(json.dumps(self.graphAsJSONLD(), sort_keys=True, indent=4))

    def graphAsJSONLD(self):
        jsonData = {"@context": {
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            # Replace this with a base document embedded in the schema
            "ns": "non-standard-convenience-properties",
            "schema": self.baseUrl
          },
          "@graph": self.graph
          }
        return jsonData

    def resolveKeyContext(self, key):
        prefix, label = key.split(":")
        return self.JSONLD["@context"][prefix] + label
