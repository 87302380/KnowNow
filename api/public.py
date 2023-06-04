import json
import os

from rdflib import Graph, Literal, URIRef, BNode
from rdflib.term import Identifier
from rdflib.collection import Collection
from rdflib.namespace import RDF, RDFS, SKOS, XSD, OWL
import rdflib.plugins.sparql.update
import owlrl
from rdflib.plugins.sparql import prepareQuery

KnowNow_URL = "https://git.tu-berlin.de/felipebaca/know-now/-/raw/main/KnowNow_V8_ttl.owl"
g = Graph() # create an empty graph
g.parse(KnowNow_URL, format = "ttl") # load the ontology

def query_sparql(sparql: str) :
    results = g.query(prepareQuery(sparql))
    headers = [str(var) for var in results.vars]
    rows = [[str(val) for val in row] for row in results]
    return json.dumps([dict(zip(headers, row)) for row in rows])
