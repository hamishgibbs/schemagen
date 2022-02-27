import csv


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
                    self.graph.append(
                        self.graphClass(
                            label=row[0],
                            superClass=row[1],
                            comment=row[5]
                        )
                    )
                elif row[2] != '':
                    # Put this propery on the activeClass
                    self.graph.append(
                        self.graphProperty(
                            label=row[2],
                            valueType=row[4],
                            comment=row[5]
                        )
                    )
                elif row[3] != '':
                    # Put this Annotation on the activeProperty
                    self.graph.append(
                        self.graphAnnotation(
                            label=row[3],
                            valueType=row[4],
                            comment=row[5]
                        )
                    )
                else:
                    pass

    def appendBaseUrl(self, label):
        return self.baseUrl + '/' + label

    def graphClass(self,
                   label,
                   superClass,
                   comment):

        node = {"@id": self.appendBaseUrl(label),
                "@type": "rdfs:Class",
                "rdfs:comment": comment,
                "rdfs:label": label,
                "properties": []}

        if superClass != '':
            node["rdfs:subClassOf"] = {
               # DEV: Currently cannot use definitions in other schemas
               "@id": self.appendBaseUrl(label)
            }

        return node

    def graphProperty(self,
                      label,
                      valueType,
                      comment):

        node = {"@id": self.appendBaseUrl(label),
                "@type": "rdfs:Property",
                "rdfs:comment": comment,
                "rdfs:label": label,
                "annotations": [],
                "range": valueType}

        return node

    def graphAnnotation(self,
                        label,
                        valueType,
                        comment):

        node = {"@id": self.appendBaseUrl(label),
                "@type": "Annotation",
                "rdfs:comment": comment,
                "rdfs:label": label,
                "range": valueType}

        return node
