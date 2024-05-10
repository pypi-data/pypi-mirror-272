from simple_ddl_parser import DDLParser
import pprint

ddl = """CREATE TABLE test (
  timestamp TIMESTAMP,
  date DATE GENERATED ALWAYS AS (CAST(timestamp AS DATE))
)"""

result = DDLParser(ddl).run(output_mode="postgres")
pprint.pprint(result)


