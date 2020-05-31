#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
##########################################
#Codi adaptat per l'equip A1
##########################################

from collections import deque, namedtuple

import requests
#import urllib.request

from random import random

import time
# generate random integer values
from random import seed
from random import randint
# seed random number generator
seed(1)

# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
  return Edge(start, end, cost)


class Graph:
    def __init__(self, edges):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path

#Construim el graf dijkstra afegint les relacions entre nodes i les distàncies
graph = Graph([
    ("P", "PA", 60),  ("PA", "PAB", 60),  ("PCD", "PA", 120), ("PAB", "PCD", 60),("PCD", "PAB", 60), ("PA", "AB", 300), ("AB", "PA", 300),  ("PAB", "AA", 300),("AA", "PAB", 300), ("AA", "A22", 20), ("A22", "AA", 20), ("AA", "A20-21", 20),    ("A20-21", "AA", 20), ("AA", "AB", 40), ("AB", "AA", 40), ("AB", "A18-19", 20),    ("A18-19", "AB", 20), ("AB", "AC", 50), ("AC", "AB", 50), ("AC", "AD", 30),    ("AD", "AC", 30), ("AC", "A15-17", 20), ("A15-17", "AC", 20), ("AD", "A14", 20),    ("A14", "AD", 20), ("AD", "AE", 40), ("AE", "AD", 40), ("AE", "A12-13", 20),    ("A12-13", "AE", 20), ("AE", "AF", 30), ("AF", "AE", 30), ("AF", "A10-11", 20),    ("A10-11", "AF", 20), ("A09", "AF", 20), ("AF", "A09", 20), ("PAB", "BA", 300),    ("BA", "PAB", 300), ("BA", "B36", 20), ("B36", "BA", 20), ("BA", "BD", 20),    ("BD", "BA", 20), ("BD", "B37", 20), ("B37", "BD", 20), ("BD", "B30", 20),    ("B30", "BD", 20), ("BD", "B31", 20), ("B31", "BD", 20), ("BA", "BB", 30),    ("BB", "BA", 30), ("BB", "BC", 30), ("BC", "BB", 30), ("BC", "B33", 40),    ("B33", "BC", 40), ("BB", "B35", 20), ("B35", "BB", 20), ("B32", "BB", 20),    ("BB", "B32", 20), ("BC", "B34", 20), ("B34", "BC", 20), ("PCD", "CA", 150),    ("CA", "PCD", 150), ("CA", "CB", 150), ("CB", "CA", 150), ("CA", "C71-73", 20),    ("C71-73", "CA", 20), ("CB", "CC", 30), ("CC", "CB", 30), ("CC", "CD", 30),    ("CD", "CC", 30), ("CD", "CE", 30), ("CE", "CD", 30), ("CE", "CF", 30),    ("CF", "CE", 30), ("CF", "CG", 30), ("CG", "CF", 30), ("CG", "CI", 30),    ("CI", "CG", 30), ("CC", "C38", 20), ("C38", "CC", 20), ("CC", "C39A-39B", 20),    ("C39A-39B", "CC", 20), ("CD", "C40", 20), ("C40", "CD", 20), ("CE", "C41-42", 20),    ("C41-42", "CE", 20), ("CF", "C43-44", 20), ("C43-44", "CF", 20), ("CG", "C45-46", 20),    ("C45-46", "CG", 20), ("CI", "C48", 20), ("C48", "CI", 20), ("CG", "C69A-69B", 40),    ("C69A-69B", "CG", 40), ("CF", "CO", 20), ("CO", "CF", 20), ("CO", "CP", 20),    ("CP", "CO", 20), ("CP", "CQ", 20), ("CQ", "CP", 20), ("CR", "CQ", 20),    ("CQ", "CR", 20), ("CR", "CS", 20), ("CS", "CR", 20), ("CO", "C68", 20),    ("C68", "CO", 20),("CP", "C66", 20), ("C66", "CP", 20), ("CP", "C67", 20),    ("C67", "CP", 20), ("CQ", "C64", 20), ("C64", "CQ", 20), ("CQ", "C65", 20),    ("C65", "CQ", 20), ("CR", "C62", 20), ("C62", "CR", 20), ("CR", "C63", 20),    ("C63", "CR", 20), ("CS", "C60", 20), ("C60", "CS", 20), ("CS", "C61", 20),    ("C61", "CS", 20), ("CI", "CJ", 30), ("CJ", "CI", 30), ("CJ", "CK", 30),    ("CK", "CJ", 30), ("CL", "CK", 30), ("CK", "CL", 30), ("CL", "CM", 30),    ("CM", "CN", 30), ("CN", "CM", 30), ("CJ", "C50", 20), ("C50", "CJ", 20),    ("CK", "C52", 20), ("C52", "CK", 20), ("CL", "C54", 20), ("C54", "CL", 20),    ("CL", "C55", 20), ("C55", "CL", 20), ("CM", "C56", 20), ("C56", "CM", 20),    ("CM", "C57", 20), ("C57", "CM", 20), ("CN", "C58", 20), ("C58", "CN", 20),    ("CM", "C59", 20), ("C59", "CM", 20), ("PCD", "DA", 150), ("DA", "PCD", 150),    ("DA", "DB", 30), ("DB", "DA", 30), ("DB", "DC", 30), ("DC", "DB", 30),    ("DC", "DD", 30), ("DD", "DC", 30), ("DD", "DE", 30), ("DE", "DD", 30),    ("DE", "DF", 30), ("DF", "DE", 30), ("DF", "DG", 30), ("DG", "DF", 30),    ("DG", "DH", 30), ("DH", "DG", 30), ("DH", "DI", 30), ("DI", "DH", 30),    ("DC", "DJ", 30), ("DJ", "DC", 30), ("DA", "D80", 20), ("D80", "DA", 20),    ("DA", "D81", 20), ("D81", "DA", 20), ("DB", "D82", 20), ("D82", "DB", 20),    ("DB", "D83", 20), ("D83", "DB", 20), ("DC", "D84", 20), ("D84", "DC", 20),    ("DJ", "D86", 20), ("D86", "DJ", 20), ("DJ", "D87", 20), ("D87", "DJ", 20),    ("DD", "D88", 20), ("D88", "DD", 20), ("DD", "D89", 20), ("D89", "DD", 20),    ("DE", "D90", 20), ("D90", "DE", 20), ("DE", "D91", 20), ("D91", "DE", 20),    ("DF", "D92", 20), ("D92", "DF", 20), ("DF", "D93", 20), ("D93", "DF", 20),    ("DG", "D94", 20), ("D94", "DG", 20), ("DG", "D95", 20), ("D95", "DG", 20),    ("DH", "D96", 20), ("D96", "DH", 20), ("DH", "D97", 20), ("D97", "DH", 20),    ("DI", "D98", 20), ("D98", "DI", 20), ("DI", "D99", 20), ("D99", "DI", 20)

])

try:
    puntOrigenPasajero = ""
    puntDesti = ""
    pasajero = ""
    #Procesan los resultados de consultar un API
    while True: #emulació d'un do...while
        #peticio = requests.get('http://192.168.1.71:3000/listaespera')
        print("llega")
        peticio = requests.get('http://craaxcloud.epsevg.upc.edu:36302/listaespera/next')
        item = peticio.json();
        print(item)

        if str(item) != "[]":
            puntOrigenPasajero = item['nodoactual']
            puntDesti = item['nododestino']
            pasajero = item['id_pasajero']

            numCoche = "Batmovil" #<- S'ha de fer una consulta a la BD per escollir un cotxe.
            #peticio2 = requests.get('http://192.168.1.71:3000/coches/'+str(numCoche))
            peticio2 = requests.get('http://craaxcloud.epsevg.upc.edu:36302/coches/'+str(numCoche))
            while peticio2.status_code != 200:
                peticio2 = requests.get('http://craaxcloud.epsevg.upc.edu:36302/coches/'+str(numCoche))

            #if peticio2.status_code != 200:
                # This means something went wrong.
                #raise ApiError('GET /tasks/ {}'.format(peticio2.status_code))


            cotxe = peticio2.json()
            #print(cotxe['puntOrigencotxe'])
            puntOrigencotxe = cotxe['puntOrigencotxe']

            #el cotxe calcula la ruta automàticament entre el punt on estigui lliure el cotxe i el punt on es troba el passatger a recollir
            camicotxe= graph.dijkstra(puntOrigencotxe, puntOrigenPasajero)

            #tracem la ruta entre el punt on es el cotxe amb el client fins el destí escollit del client
            cami = graph.dijkstra(puntOrigenPasajero, puntDesti)
            #url = 'http://192.168.1.71:3000/coches/'+str(numCoche)
            url = 'http://craaxcloud.epsevg.upc.edu:36302/coches/'+str(numCoche)
            #myobj = {'estado': 'ocupado', 'id_pasajero': pasajero}
            myobj = {'puntOrigen':puntOrigenPasajero, 'puntDesti': puntDesti,'estado': 'en curs...', 'id_pasajero': pasajero}
            print("en curs...")
            x = requests.put(url, json = myobj)
            for i, elem in enumerate(camicotxe):
                veloc = randint(1, 12) #rang de temps
                #veloc = randint(1, 3) #rang de temps

                myobj = {'puntActual': elem}
                print(elem)
                x = requests.put(url, json = myobj)

                time.sleep(veloc)

            myobj = {'estado': 'carregant...'}
            print("carregant...")
            x = requests.put(url, json = myobj)
            time.sleep(randint(1, 20))
            #time.sleep(randint(1, 3))

            myobj = {'estado': 'ocupat'}
            print("ocupat")
            x = requests.put(url, json = myobj)
            for i, elem in enumerate(cami):
                veloc = randint(1, 12) #rang de temps
                #veloc = randint(1, 3) #rang de temps
                myobj = {'puntActual': elem}
                print(elem)
                x = requests.put(url, json = myobj)
                time.sleep(veloc)

            myobj = {'puntOrigen': '', 'puntDesti': '', 'puntOrigencotxe': puntDesti, 'estado': 'disponible', 'id_pasajero': ''}
            x = requests.put(url, json = myobj)
            while x.status_code != 200 and x.status_code != 204:
                x = requests.put(url, json = myobj)

        else:
            time.sleep(5); #Esperem 5 segons entre peticions.

        #for m in peticio.json():
            #puntOrigencotxe = "P"
            #puntOrigenPasajero = item['nodoactual']
            #puntDesti = item['nododestino']
            #pasajero = item['id_pasajero']
            #if pasajero != "": #si és buit, continua demanant
            #    break


    time.sleep(randint(3, 5))
except:
    print("Error ;-)")

finally:
    exit()
