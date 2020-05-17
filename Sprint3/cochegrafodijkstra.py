from collections import deque, namedtuple

import json
#import requests
import urllib.request
#import urllib2

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
    ("P", "PA", 60),  ("PA", "PAB", 60),  ("PCD", "PA", 120), ("PAB", "PCD", 60),
    ("PCD", "PAB", 60), ("PA", "AB", 300), ("AB", "PA", 300),  ("PAB", "AA", 300),
    ("AA", "PAB", 300), ("AA", "A22", 20), ("A22", "AA", 20), ("AA", "A20-21", 20),
    ("A20-21", "AA", 20), ("AA", "AB", 40), ("AB", "AA", 40), ("AB", "A18-19", 20),
    ("A18-19", "AB", 20), ("AB", "AC", 50), ("AC", "AB", 50), ("AC", "AD", 30),
    ("AD", "AC", 30), ("AC", "A15-17", 20), ("A15-17", "AC", 20), ("AD", "A14", 20),
    ("A14", "AD", 20), ("AD", "AE", 40), ("AE", "AD", 40), ("AE", "A12-13", 20),
    ("A12-13", "AE", 20), ("AE", "AF", 30), ("AF", "AE", 30), ("AF", "A10-11", 20),
    ("A10-11", "AF", 20), ("A09", "AF", 20), ("AF", "A09", 20), ("PAB", "BA", 300),
    ("BA", "PAB", 300), ("BA", "B36", 20), ("B36", "BA", 20), ("BA", "BD", 20), 
    ("BD", "BA", 20), ("BD", "B37", 20), ("B37", "BD", 20), ("BD", "B30", 20),
    ("B30", "BD", 20), ("BD", "B31", 20), ("B31", "BD", 20), ("BA", "BB", 30),
    ("BB", "BA", 30), ("BB", "BC", 30), ("BC", "BB", 30), ("BC", "B33", 40),
    ("B33", "BC", 40), ("BB", "B35", 20), ("B35", "BB", 20), ("B32", "BB", 20),
    ("BB", "B32", 20), ("BC", "B34", 20), ("B34", "BC", 20), ("PCD", "CA", 150),
    ("CA", "PCD", 150), ("CA", "CB", 150), ("CB", "CA", 150), ("CA", "C71-73", 20),
    ("C71-73", "CA", 20), ("CB", "CC", 30), ("CC", "CB", 30), ("CC", "CD", 30), 
    ("CD", "CC", 30), ("CD", "CE", 30), ("CE", "CD", 30), ("CE", "CF", 30), 
    ("CF", "CE", 30), ("CF", "CG", 30), ("CG", "CF", 30), ("CG", "CI", 30),
    ("CI", "CG", 30), ("CC", "C38", 20), ("C38", "CC", 20), ("CC", "C39A-39B", 20),
    ("C39A-39B", "CC", 20), ("CD", "C40", 20), ("C40", "CD", 20), ("CE", "C41-42", 20),
    ("C41-42", "CE", 20), ("CF", "C43-44", 20), ("C43-44", "CF", 20), ("CG", "C45-46", 20),
    ("C45-46", "CG", 20), ("CI", "C48", 20), ("C48", "CI", 20), ("CG", "C69A-69B", 40), 
    ("C69A-69B", "CG", 40), ("CF", "CO", 20), ("CO", "CF", 20), ("CO", "CP", 20), 
    ("CP", "CO", 20), ("CP", "CQ", 20), ("CQ", "CP", 20), ("CR", "CQ", 20), 
    ("CQ", "CR", 20), ("CR", "CS", 20), ("CS", "CR", 20), ("CO", "C68", 20), 
    ("C68", "CO", 20),("CP", "C66", 20), ("C66", "CP", 20), ("CP", "C67", 20),
    ("C67", "CP", 20), ("CQ", "C64", 20), ("C64", "CQ", 20), ("CQ", "C65", 20),
    ("C65", "CQ", 20), ("CR", "C62", 20), ("C62", "CR", 20), ("CR", "C63", 20),
    ("C63", "CR", 20), ("CS", "C60", 20), ("C60", "CS", 20), ("CS", "C61", 20),
    ("C61", "CS", 20), ("CI", "CJ", 30), ("CJ", "CI", 30), ("CJ", "CK", 30),
    ("CK", "CJ", 30), ("CL", "CK", 30), ("CK", "CL", 30), ("CL", "CM", 30),
    ("CM", "CN", 30), ("CN", "CM", 30), ("CJ", "C50", 20), ("C50", "CJ", 20),
    ("CK", "C52", 20), ("C52", "CK", 20), ("CL", "C54", 20), ("C54", "CL", 20),
    ("CL", "C55", 20), ("C55", "CL", 20), ("CM", "C56", 20), ("C56", "CM", 20),
    ("CM", "C57", 20), ("C57", "CM", 20), ("CN", "C58", 20), ("C58", "CN", 20),
    ("CM", "C59", 20), ("C59", "CM", 20), ("PCD", "DA", 150), ("DA", "PCD", 150),
    ("DA", "DB", 30), ("DB", "DA", 30), ("DB", "DC", 30), ("DC", "DB", 30), 
    ("DC", "DD", 30), ("DD", "DC", 30), ("DD", "DE", 30), ("DE", "DD", 30),
    ("DE", "DF", 30), ("DF", "DE", 30), ("DF", "DG", 30), ("DG", "DF", 30),
    ("DG", "DH", 30), ("DH", "DG", 30), ("DH", "DI", 30), ("DI", "DH", 30),
    ("DC", "DJ", 30), ("DJ", "DC", 30), ("DA", "D80", 20), ("D80", "DA", 20),
    ("DA", "D81", 20), ("D81", "DA", 20), ("DB", "D82", 20), ("D82", "DB", 20),
    ("DB", "D83", 20), ("D83", "DB", 20), ("DC", "D84", 20), ("D84", "DC", 20),
    ("DJ", "D86", 20), ("D86", "DJ", 20), ("DJ", "D87", 20), ("D87", "DJ", 20),
    ("DD", "D88", 20), ("D88", "DD", 20), ("DD", "D89", 20), ("D89", "DD", 20),
    ("DE", "D90", 20), ("D90", "DE", 20), ("DE", "D91", 20), ("D91", "DE", 20),
    ("DF", "D92", 20), ("D92", "DF", 20), ("DF", "D93", 20), ("D93", "DF", 20),
    ("DG", "D94", 20), ("D94", "DG", 20), ("DG", "D95", 20), ("D95", "DG", 20),
    ("DH", "D96", 20), ("D96", "DH", 20), ("DH", "D97", 20), ("D97", "DH", 20),
    ("DI", "D98", 20), ("D98", "DI", 20), ("DI", "D99", 20), ("D99", "DI", 20)

])

#Para provar antes de API
#peticio = '{ "Origen":"P", "Desti":"CK" }'
#peticioConvertida = json.loads(peticio)
#camicotxe = graph.dijkstra(peticioConvertida["Origen"], peticioConvertida["Desti"])
#Procesan los resultados de consultar un API en ---para después----
# import requests
# peticio = requests.get('http://ip-api.com/json/208.80.152.201')
# peticioConvertida = json.loads(peticio.content)

#print(peticioConvertida["Origen"])

#while True:
try:
	#Imprimim les opcions que seran en un futur a l'aplicació i la web
	print("Benvingut a l'aeroport de Vilanova i la Geltrú------------------------------")
	print("Localitzacions:")
	print("P=Parquing")
	print("Terminal A:")
	print("Portes:")
	print("A09=Terminal A - Porta A09")
	print("A10-11=Terminal A - Porta A10-11")
	print("A12-13=Terminal A - Porta A12-13")
	print("A14=Terminal A - Porta A14")
	print("A15-17=Terminal A - Porta A15-17")
	print("A18-19=Terminal A - Porta A18-19")
	print("A20-21=Terminal A - Porta A20-21")
	print("A22=Terminal A - Porta A22")
	print("Parades del cotxe secundàries al Terminal A")
	print("AA=Terminal A - Parada AA")
	print("AB=Terminal A - Parada AB")
	print("AC=Terminal A - Parada AC")
	print("AD=Terminal A - Parada AD")
	print("AE=Terminal A - Parada AE")
	print("AF=Terminal A - Parada AF")
	print("------------------------------------")
	print("Terminal B:")
	print("Portes:")
	print("B30=Terminal B - Porta B30")
	print("B31=Terminal B - Porta B31")
	print("B32=Terminal B - Porta B32")
	print("B33=Terminal B - Porta B33")
	print("B34=Terminal B - Porta B34")
	print("B35=Terminal B - Porta B35")
	print("B36=Terminal B - Porta B36")
	print("B37=Terminal B - Porta B37")
	print("Parades del cotxe secundàries al Terminal B")
	print("BA=Terminal B - Parada BA")
	print("BB=Terminal B - Parada BB")
	print("BC=Terminal B - Parada BC")
	print("BD=Terminal B - Parada BD")
	print("------------------------------------")
	print("Terminal C:")
	print("Portes:")
	print("C71-73=Terminal C - Porta C71-73")
	print("C38=Terminal C - Porta C38")
	print("C39A-39B=Terminal C - Porta C39A-39B")
	print("C40=Terminal C - Porta C40")
	print("C41-42=Terminal C - Porta C41-42")
	print("C43-44=Terminal C - Porta C43-44")
	print("C45-46=Terminal C - Porta C45-46")
	print("C48=Terminal C - Porta C48")
	print("C50=Terminal C - Porta C50")
	print("C52=Terminal C - Porta C52")
	print("C54=Terminal C - Porta C54")
	print("C55=Terminal C - Porta C55")
	print("C56=Terminal C - Porta C56")
	print("C57=Terminal C - Porta C57")
	print("C58=Terminal C - Porta C58")
	print("C59=Terminal C - Porta C59")
	print("C60=Terminal C - Porta C60")
	print("C61=Terminal C - Porta C61")
	print("C62=Terminal C - Porta C62")
	print("C63=Terminal C - Porta C63")
	print("C64=Terminal C - Porta C64")
	print("C65=Terminal C - Porta C65")
	print("C66=Terminal C - Porta C66")
	print("C67=Terminal C - Porta C67")
	print("C68=Terminal C - Porta C68")
	print("C69A-69B=Terminal C - Porta C69A-69B")
	print("Parades del cotxe secundàries al Terminal C")
	print("CA=Terminal C - Parada CA")
	print("CB=Terminal C - Parada CB")
	print("CC=Terminal C - Parada CC")
	print("CD=Terminal C - Parada CD")
	print("CE=Terminal C - Parada CE")
	print("CE=Terminal C - Parada CE")
	print("CF=Terminal C - Parada CF")
	print("CG=Terminal C - Parada CG")
	print("CI=Terminal C - Parada CI")
	print("CJ=Terminal C - Parada CJ")
	print("CK=Terminal C - Parada CK")
	print("CL=Terminal C - Parada CL")
	print("CM=Terminal C - Parada CM")
	print("CN=Terminal C - Parada CN")
	print("CO=Terminal C - Parada CO")
	print("CP=Terminal C - Parada CP")
	print("CQ=Terminal C - Parada CQ")
	print("CR=Terminal C - Parada CR")
	print("CS=Terminal C - Parada CS")
	print("-----------------------------------")
	print("Terminal D:")
	print("Portes:")
	print("D80=Terminal D - Porta D80")
	print("D81=Terminal D - Porta D81")
	print("D82=Terminal D - Porta D82")
	print("D83=Terminal D - Porta D83")
	print("D84=Terminal D - Porta D84")
	print("D85=Terminal D - Porta D85")
	print("D86=Terminal D - Porta D86")
	print("D87=Terminal D - Porta D87")
	print("D88=Terminal D - Porta D88")
	print("D89=Terminal D - Porta D89")
	print("D90=Terminal D - Porta D90")
	print("D91=Terminal D - Porta D91")
	print("D92=Terminal D - Porta D92")
	print("D93=Terminal D - Porta D93")
	print("D94=Terminal D - Porta D94")
	print("D95=Terminal D - Porta D95")
	print("D96=Terminal D - Porta D96")
	print("D97=Terminal D - Porta D97")
	print("D98=Terminal D - Porta D98")
	print("D99=Terminal D - Porta D99")
	print("Parades del cotxe secundàries al Terminal D")
	print("DA=Terminal D - Parada DA")
	print("DB=Terminal D - Parada DB")
	print("DC=Terminal D - Parada DC")
	print("DD=Terminal D - Parada DD")
	print("DE=Terminal D - Parada DE")
	print("DF=Terminal D - Parada DF")
	print("DG=Terminal D - Parada DG")
	print("DH=Terminal D - Parada DH")
	print("DI=Terminal D - Parada DI")
	print("DJ=Terminal D - Parada DJ")
	print("------------------------------------")
	#seleccio = input("Mode manual[m] o Mode automático[a]:")
	#if seleccio == "a":
	#	print("Ruta Escogida:")
	#else:
	#Preguntem al client on es i cap a on va
	print("Esculli ruta:")
	puntOrigencotxe = "P"
	puntOrigen = input("On es troba?: ")
	puntDesti = input("On va?: ")
	#el cotxe calcula la ruta automàticament entre el parquing i el punt on es troba el passatger a recollir
	camicotxe= graph.dijkstra(puntOrigencotxe, puntOrigen)
	print("Ruta cotxe-client: "+str(camicotxe))
	#tracem la ruta entre el punt on es el cotxe amb el client fins el destí escollit del client
	cami = graph.dijkstra(puntOrigen, puntDesti)
	#Aquest script cridaria al cotxe posant en marxa els sensors i les rodes
	#execfile("arduino.py")
except IndexError:
	print("Error ;-)")
else:
	#Mostrem al client la ruta des d'on es troba fins al seu destí
	print("La seva ruta escollida: "+str(cami))
	print("En breus el cotxe vindrà a recollir-lo")
	data = {}
	data['camiEnviar'] = []
	i = 1
	while cami:
            #print('{}{}'.format("Punt: ",cami[0]))
			data['camiEnviar'].append({
			'Punt'+str(i): cami[0]})
			cami.popleft()
			i = i + 1
			print("Parades: "+str(cami))
	with open('cami.json', 'w') as file:
		json.dump(data, file, indent=4)
	print("Ha arribat al seu destí!. Gràcies per fer servir els serveis de l'Aeroport de Vilanova i la Geltrú!")	
        #Para cuando haya server----falta user, password---------------------
        # myurl = "http://www.testmycode.com"
        # req = urllib.request.Request(myurl)
        # req.add_header('Content-Type', 'application/json; charset=utf-8')
        # jsondata = json.dumps(data)
        # jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
        # req.add_header('Content-Length', len(jsondataasbytes))
        # print (jsondataasbytes)
        # response = urllib.request.urlopen(req, auth=('username', 'password'), verify=False, jsondataasbytes)
        # print(response.status_code) ----Aquí comprovaremos si la transmisión se ha realizado correctamente
finally:
	print("-------------------------------------")
