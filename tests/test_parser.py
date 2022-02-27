from schemagen.parser import (
    SchemaParser
)

def test_SchemaParser():
    parser = SchemaParser("gfy.org")

    parser.parse_csv_schema("data/schema.csv")

    print(parser.pprintGraph())

    assert False

# There need to be lots of tests for every key value pair
