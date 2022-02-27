import csv

class SchemaParser():
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.activeClass = None
        self.activeProperty = None
        self.activeAnnotation = None
        self.graph = []

    def parse_csv_schema(self, fn):

        with open(fn) as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)
                if row[0] != '':
                    self.graph.append(
                        self.csvToClass(
                            label=row[0],
                            superClass=row[1],
                            comment=row[5]
                        )
                    )

    def csvToClass(label,
                   superClass,
                   comment):

        node = {"@id": self.baseUrl + label,
                "@type": "rdfs:Class",
                "rdfs:comment": comment,
                "rdfs:label": label,
                "properties": []}

        if superClass != '':
            node["rdfs:subClassOf"] = {
               # DEV: Currently cannot use definitions in other schemas
               "@id": self.baseUrl + superClass
            }

        return node
