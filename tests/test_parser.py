import csv
from schemagen.parser import (
    SchemaParser
)

def test_SchemaParser():

    parser = SchemaParser("gfy.org")

    with open("data/schema.csv") as f:
        reader = csv.reader(f)
        parser.parse_csv_schema(reader)

    print(parser.pprintGraph())

    assert False

# There need to be lots of tests for every key value pair
