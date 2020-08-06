import os

REDIS_URI = os.environ.get('REDIS_URI', 'redis://localhost')
NEO4J_URI = os.environ.get('NEO4J_URI', 'neo4j:localhost')
