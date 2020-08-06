import neo4j

import settings


def __run_transaction(func):
    driver = neo4j.GraphDatabase.driver(settings.NEO4J_URI)
    with driver.session() as s:
        res = s.write_transaction(func)
    return res

def get_count():
    return __run_transaction(lambda tx: tx.run("MATCH(n:VM) RETURN COUNT(n)").single()[0])

def get_attackers(machine_id):
    return __run_transaction(lambda tx: tx.run("MATCH (from:VM)-[r]->(:VM{id:'%s'}) RETURN from" % machine_id).values())
