from schemagen.parser import (
    SchemaParser
)

def test_SchemaParser():
    parser = SchemaParser("go.fuck.yourself.org")

    res = parser.parse_csv_schema("data/schema.csv")

    print(res)

    assert res == False
