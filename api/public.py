import json
import os
import paramiko
from scp import SCPClient
import configparser

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

def upload_file_to_server(path, file):
    file_path = "./KnowNow/tmp/" + file.name

    with open(file_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)

    config = configparser.ConfigParser()
    config.read('config.ini')

    host = config['scp']['host']
    port = config['scp']['port']
    username = config['scp']['username']
    password = config['scp']['password']

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(host, port, username, password)
    scpclient = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)

    remote_path = "/home/knownow/KnowNow/" + path

    try:
        scpclient.put(file_path, remote_path)
        status = 200
    except:
        status = 500

    scpclient.close()
    ssh_client.close()

    os.remove(file_path)
    return status

def query_sparql(sparql: str) :
    results = g.query(prepareQuery(sparql))
    headers = [str(var) for var in results.vars]
    rows = [[str(val) for val in row] for row in results]
    return json.dumps([dict(zip(headers, row)) for row in rows])
