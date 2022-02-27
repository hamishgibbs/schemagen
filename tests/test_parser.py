from schemagen.parser import (
    SchemaParser
)

def test_SchemaParser():
    parser = SchemaParser("gfy.org")

    parser.parse_csv_schema("data/schema.csv")

    print(parser.graph)

    assert False
