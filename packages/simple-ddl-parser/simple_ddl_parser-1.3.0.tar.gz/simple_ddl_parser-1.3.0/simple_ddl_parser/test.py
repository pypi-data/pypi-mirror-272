from simple_ddl_parser import DDLParser
import pprint

ddl = """CREATE TABLE data.test(
   field_a INT OPTIONS(description='some description')
 )
 PARTITION BY DATE(field);"""

result = DDLParser(ddl).run(output_mode="bigquery")
pprint.pprint(result)


