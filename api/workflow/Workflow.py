from rdflib import Graph, Literal, URIRef, BNode, Namespace
from rdflib.namespace import RDF, RDFS, SKOS, XSD, OWL
from pyiron_base import PythonTemplateJob as PTJ
import owlrl
import pandas as pd
import mph
import os

class ComsolSimulation(PTJ):
    def __init__(self, project, job_name):
        super().__init__(project, job_name)
        self.input.DataResources = []
        self.input.comsol_model = None
        self.input.comsol_model_name = None
        self.input.parameters = None
        self.input.process = None
        self.input.object = None
        self.input.object_name = None
        self.output.comsol_model = None
        self.output.comsol_model_name = None
        self.output.object = None
        self.client = None
        self.graphURL = "/home/knownow/KnowNow/TUB/Ontology/KnowNow_old.owl"
        self.g = Graph()
        self.g.parse(self.graphURL, format="ttl")  # self.g is the knowledge graph of the ontology before reasoner
        self.gr = Graph()
        self.gr.parse(self.graphURL, format="ttl")  # self.gr is the knowledge graph of the ontology after reasoner
        rdfs = owlrl.CombinedClosure.RDFS_OWLRL_Semantics(self.gr, False, False, False)
        rdfs.closure()
        rdfs.flush_stored_triples()

    def connection_check(self):
        """
        Try to connect with the software Comsol.
        """
        try:
            self.client = mph.start(cores=1)
        except:
            self.client = None
        if self.client == None:
            print("Connection error")
            return 0
        else:
            print("Successful connection")
            return 1

    def set_graph(self, graphURL):
        """
        It is used to change the ontology´s URL.
        To run the knowledge graph with the new URL please make sure you run the method run.graph()
        """
        self.graphURL = graphURL

    def run_graph(self):
        """
        Refreshes the connection with the Ontology.
        """
        self.g.parse(self.graphURL, format="ttl")
        self.gr.parse(self.graphURL, format="ttl")
        rdfs = owlrl.CombinedClosure.RDFS_OWLRL_Semantics(self.gr, False, False, False)
        rdfs.closure()
        rdfs.flush_stored_triples()

    def get_models(self):
        """
        Returns a Pandas DataFrame with all the instances of Model.
        """
        query = """
        SELECT ?s 
        WHERE { 
            ?s a KN:Model
        }
        """
        data = {"Model": [], "Type": []}
        df = pd.DataFrame(data)
        models = []

        qres = self.gr.query(query)
        for row in qres:
            res = row.s.split("#")
            models.append(res[1])

        for model in models:
            query1 = """
            SELECT ?o
            WHERE {
                KN:%s a ?o
                FILTER (?o != owl:NamedIndividual)
            }
            """ % model
            qres1 = self.g.query(query1)
            for row in qres1:
                res = row.o.split("#")
                new_row = {"Model": model, "Type": res[1]}
                new_df = pd.DataFrame([new_row])
                df = pd.concat([df, new_df], axis=0, ignore_index=True)
        return df

    def get_objects(self):
        """
        Returns a Pandas DataFrame with all the instances of Object.
        """
        query = """
        SELECT ?s 
        WHERE { 
            ?s a KN:Object
        }
        """
        data = {"Object": [], "Type": []}
        df = pd.DataFrame(data)
        objects = []

        qres = self.gr.query(query)
        for row in qres:
            res = row.s.split("#")
            objects.append(res[1])

        for element in objects:
            query1 = """
            SELECT ?o
            WHERE {
                KN:%s a ?o
                FILTER (?o != owl:NamedIndividual)
            }
            """ % element
            qres1 = self.g.query(query1)
            for row in qres1:
                res = row.o.split("#")
                new_row = {"Object": element, "Type": res[1]}
                new_df = pd.DataFrame([new_row])
                df = pd.concat([df, new_df], axis=0, ignore_index=True)
        return df

    def get_processes(self):
        """
        Returns a Pandas DataFrame with all the instances of Process.
        """
        query = """
        SELECT ?s 
        WHERE { 
            ?s a KN:Process
        }
        """
        data = {"Process": [], "Type": []}
        df = pd.DataFrame(data)
        processes = []

        qres = self.gr.query(query)
        for row in qres:
            res = row.s.split("#")
            processes.append(res[1])

        for process in processes:
            query1 = """
            SELECT ?o
            WHERE {
                KN:%s a ?o
                FILTER (?o != owl:NamedIndividual)
            }
            """ % process
            qres1 = self.g.query(query1)
            for row in qres1:
                res = row.o.split("#")
                new_row = {"Process": process, "Type": res[1]}
                new_df = pd.DataFrame([new_row])
                df = pd.concat([df, new_df], axis=0, ignore_index=True)
        return df

    def get_process_parameters(self, process):
        """
        Returns a Pandas DataFrame with all the parameters and its values of a certain process.
        """
        query = """
        SELECT ?p ?o
        WHERE {
            KN:%s ?p ?o
            FILTER NOT EXISTS {?s a ?o}
            FILTER NOT EXISTS {?s KN:hasInputObject ?o}
            FILTER NOT EXISTS {?s KN:hasOutputObject ?o}
        }
        """ % process
        data1 = {"Process Parameter": [], "Value": []}
        df1 = pd.DataFrame(data1)

        qres1 = self.g.query(query)
        for row in qres1:
            res0 = row["p"].split("#")
            res1 = row["o"]
            new_row = {"Process Parameter": res0[1], "Value": res1}
            new_df = pd.DataFrame([new_row])
            df1 = pd.concat([df1, new_df], axis=0, ignore_index=True)

        df1 = df1.drop(df1.index[df1['Process Parameter'] == "sameAs"].tolist(), axis=0)
        df1 = df1.reset_index(drop=True)
        return df1

    def change_process_parameter(self, process, parameter, value, data_type=XSD.string):
        """
        Changes the existing parameters.
        """
        process = URIRef(f"http://www.semanticweb.org/baca/ontologies/2021/10/KnowNow#{process}")
        parameter = URIRef(f"http://www.semanticweb.org/baca/ontologies/2021/10/KnowNow#{parameter}")

        try:
            self.g.remove((process, parameter, None))
        except:
            pass
        self.g.add((process, parameter, Literal(value, datatype=data_type)))

    def set_input_parameters(self, DFparameters):
        """
        Defines the parameters used for running the simulation.
        """
        self.input.parameters = DFparameters

    def set_input_process(self, process):
        """
        Defines the process and tokes its parameters for running the simulation.
        """
        self.input.parameters = self.get_process_parameters(process)
        self.input.process = process

    def get_DataResources(self, showDomain=False):
        """
        Returns a Pandas DataFrame with all the data resources and its domains.
        """
        if showDomain == True:
            query = """
            SELECT ?s ?o
            WHERE {
                ?s KN:hasDataResource ?o
            }
            """
            data = {"Object": [], "Data Resource": []}
            df = pd.DataFrame(data)

            qres = self.g.query(query)
            for row in qres:
                res0 = row.s.split("#")
                res1 = row.o.split("#")
                new_row = {"Object": res0[1], "Data Resource": res1[1]}
                new_df = pd.DataFrame([new_row])
                df = pd.concat([df, new_df], axis=0, ignore_index=True)
        elif showDomain == False:
            query = """
            SELECT ?s
            WHERE {
                ?s a KN:DataResource
            }
            """
            data = {"Data Resource": []}
            df = pd.DataFrame(data)

            qres = self.g.query(query)
            for row in qres:
                res = row.s.split("#")
                new_row = {"Data Resource": res[1]}
                new_df = pd.DataFrame([new_row])
                df = pd.concat([df, new_df], axis=0, ignore_index=True)
        return df

    def set_input_DataResource(self, DataResource):  # It is used for extra files in addition of the model.
        """
        Defines additional needed files and returns its location.
        """
        query = """
        SELECT ?o
        WHERE {
             KN:%s KN:hasDataResourceLocation ?o
        }
        """ % DataResource
        qres = self.g.query(query)
        for row in qres:
            location = row.o.toPython()
        self.input.DataResources.append(location)

    def set_input_comsol_model(self, model):
        """
        Defines the model and returns its location.
        """
        query = """
        SELECT ?o
        WHERE {
             KN:%s KN:hasDataResourceLocation ?o
        }
        """ % model
        qres = self.g.query(query)
        for row in qres:
            location = row.o.toPython()
        self.input.comsol_model = location
        self.input.comsol_model_name = model

    def set_input_object(self, object_name):
        """
        Defines the object search the model, process and data resources connected to it and sets its location and parameters.
        """
        query = """
        SELECT ?o
        WHERE {
             KN:%s KN:hasModel ?o
             FILTER EXISTS {?o a KN:WorkPieceMultiPhysicsModel}
        }
        """ % object_name

        qres = self.g.query(query)
        for row in qres:
            res = row.o.split("#")
            model = res[1]

        query_process = """
        SELECT ?o
        WHERE {
            KN:%s KN:execute ?o
        }
        """ % model
        qres_process = self.g.query(query_process)
        for row in qres_process:
            res = row.o.split("#")
            process = res[1]

        query_DR = """
        SELECT ?o
        WHERE {
            KN:%s KN:hasDataResource ?o
            FILTER EXISTS {?o KN:hasDataResourceSerialization "mph"^^xsd:string}
        }
        """ % object_name
        qres_DR = self.g.query(query_DR)
        for row in qres_DR:
            res = row.o.split("#")
            model_DR = res[1]

        self.set_input_process(process)
        self.set_input_comsol_model(model_DR)
        self.input.object = object_name

    def modify_parameters_comsol(self, model):
        """
        Changes the parameters of the loaded COMSOL-Model.
        """
        for i in self.input.parameters.iterrows():
            model.parameter(str(i[1][0]), str(i[1][1]))

    def save_exports(self, model):
        exports = model.exports()

        for i in exports:
            i = i.replace(" ", "")
            model.export(i, i + ".png")

            URI_DR = URIRef(f"http://www.semanticweb.org/ontologies/KnowNow#{i}")

            self.g.add((URI_DR, RDF.type, DR))
            self.g.add((URI_DR, RDF.type, OWL.NamedIndividual))
            self.g.add((URI_DR, hasFormat, Literal("png", datatype=XSD.string)))
            self.g.add((URI_DR, hasUri, Literal(os.getcwd() + i + ".png", datatype=XSD.string)))

            self.g.add((URIOutputObject, hasDataResource, URI_DR))

    def save_results(self, model):
        self.output.comsol_model = self.input.comsol_model.split(".")[0] + "_solved.mph"
        self.output.comsol_model_name = self.input.comsol_model_name + "_solved"
        model.save(self.output.comsol_model)
        self.output.object = self.input.object + "_solved"

        URIOutputDR = URIRef(f"http://www.semanticweb.org/ontologies/KnowNow#{self.output.comsol_model_name}")
        DR = URIRef("http://www.semanticweb.org/ontologies/KnowNow#DataResource")
        hasFormat = URIRef("http://www.semanticweb.org/ontologies/KnowNow#hasDataResourceSerialization")
        hasUri = URIRef("http://www.semanticweb.org/ontologies/KnowNow#hasDataResourceLocation")
        hasDataResource = URIRef("http://www.semanticweb.org/ontologies/KnowNow#hasDataResource")

        URIOutputObject = URIRef(f"http://www.semanticweb.org/ontologies/KnowNow#{self.output.object}")
        Workpiece = URIRef("http://www.semanticweb.org/ontologies/KnowNow#WorkPiece")

        hasOutput = URIRef("http://www.semanticweb.org/ontologies/KnowNow#hasOutputObject")
        URIProcess = URIRef(f"http://www.semanticweb.org/ontologies/KnowNow#{self.input.process}")

        self.g.add((URIOutputObject, RDF.type, Workpiece))
        self.g.add((URIOutputObject, RDF.type, OWL.NamedIndividual))

        self.g.add((URIOutputDR, RDF.type, DR))
        self.g.add((URIOutputDR, RDF.type, OWL.NamedIndividual))
        self.g.add((URIOutputDR, hasFormat, Literal("mph", datatype=XSD.string)))
        self.g.add((URIOutputDR, hasUri, Literal(self.output.comsol_model, datatype=XSD.string)))

        self.g.add((URIProcess, hasOutput, URIOutputObject))

        self.g.add((URIOutputObject, hasDataResource, URIOutputDR))

        exports = model.exports()

        # Location to save the exports:
        exp_loc = self.input.comsol_model.split("/")
        exp_loc = exp_loc[1:-1]
        location_exp = '/'
        for element in exp_loc:
            location_exp = location_exp + element + '/'

        # Save the exports:
        for i in exports:
            i_p = i.replace(" ", "")
            model.export(i, i_p + ".png")

            URI_DR = URIRef(f"http://www.semanticweb.org/ontologies/KnowNow#{i_p}")

            self.g.add((URI_DR, RDF.type, DR))
            self.g.add((URI_DR, RDF.type, OWL.NamedIndividual))
            self.g.add((URI_DR, hasFormat, Literal("png", datatype=XSD.string)))
            self.g.add((URI_DR, hasUri, Literal(location_exp + i_p + ".png", datatype=XSD.string)))

            self.g.add((URIOutputObject, hasDataResource, URI_DR))

        self.g.serialize(self.graphURL, "turtle")
        self.run_graph()

    def run_static(self):  # Call a python function and store stuff in the output
        check = self.connection_check()
        if check == 1:  # if the connection is succesful the model will be loaded  to Comsol
            model = self.client.load(
                self.input.comsol_model)  # self.input.model is the location of the .mph file saved localy.
            # Load extra files e.g. CAD-Files
            self.modify_parameters_comsol(model)
            print("Model studies: ", model.studies())
            print("model materials: ", model.materials())
            print("model physics: ", model.physics())
            # Run simulation on COMSOL
            # model.mesh()
            # model.solve('Study DC & AC')
            self.save_results(model)
            print("Successful simulation")
            print("Output object saved as: ", self.output.comsol_model)
            self.status.finished = True