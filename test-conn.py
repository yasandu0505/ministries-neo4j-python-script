from neo4j import GraphDatabase

uri = "neo4j+ssc://b1331415.databases.neo4j.io"
user = "neo4j"
password = "o079ZCmVViuKS0wkyICK_fjR0DiRfREMtiMHkdzZJbs"

driver = GraphDatabase.driver(uri, auth=(user, password))

with driver.session() as session:
    greeting = session.run("RETURN 'Connection successful' AS message").single()
    print(greeting["message"])
