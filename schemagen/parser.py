import csv
import json

class SchemaParser():
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.activeClass = None
        self.activeProperty = None
        self.graph = []

    def parse_csv_schema(self, fn):

        with open(fn) as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                print(row)
                if row[0] != '':
                    # This should be abstracted
                    graphClass = self.createGraphClass(
                        label=row[0],
                        superClass=row[1],
                        comment=row[5]
                    )
                    self.activeClass = graphClass["@id"]
                    self.graph.append(graphClass)
                elif row[2] != '':
                    # Put this propery on the activeClass
                    graphProperty = self.createGraphProperty(
                        label=row[2],
                        valueType=row[4],
                        comment=row[5]
                    )
                    self.activeProperty = graphProperty["@id"]
                    self.graph.append(graphProperty)
                    self.appendPropertyToActiveClass(graphProperty["@id"])
                elif row[3] != '':
                    # Put this Annotation on the activeProperty
                    graphAnnotation = self.createGraphAnnotation(
                        label=row[3],
                        valueType=row[4],
                        comment=row[5]
                    )
                    self.graph.append(graphAnnotation)
                    self.appendAnnotationToActiveProperty(graphAnnotation["@id"])
                else:
                    pass

    def appendBaseUrl(self, label):
        return "schema/" + label

    def createGraphClass(self,
                   label,
                   superClass,
                   comment):

        node = {"@id": self.appendBaseUrl(label),
                "@type": "rdfs:Class",
                "rdfs:comment": comment,
                "rdfs:label": label,
                "ns:properties": []}

        if superClass != '':
            node["rdfs:subClassOf"] = {
               # DEV: Currently cannot use definitions in other schemas
               "@id": self.appendBaseUrl(label)
            }

        return node

    def createGraphProperty(self,
                      label,
                      valueType,
                      comment):

        node = {"@id": self.appendBaseUrl(label),
                "@type": "rdfs:Property",
                "rdfs:comment": comment,
                "rdfs:label": label,
                "ns:annotations": [],
                "ns:range": valueType}

        return node

    def createGraphAnnotation(self,
                        label,
                        valueType,
                        comment):

        node = {"@id": self.appendBaseUrl(label),
                "@type": "Annotation",
                "rdfs:comment": comment,
                "rdfs:label": label,
                "ns:range": valueType}

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
            "ns:ns": "non-standard-convenience-properties",
            "schema": self.baseUrl
          },
          "@graph": self.graph
          }
        return jsonData

    def graphAsHTML(self):
        return False
