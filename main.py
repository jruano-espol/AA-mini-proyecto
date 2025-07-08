from enum import IntEnum


class Estado(IntEnum):
    HABILITADO = 1
    CERRADO = 2
    AGRIETADO = 3


class Arista:
    def __init__(self, min: float, max: float, estado: Estado):
        self.min = min
        self.max = max
        self.estado = estado

    def peso_efectivo(self) -> float:
        if self.estado == Estado.CERRADO:
            return float('inf')

        def interpolacion_lineal(t: float, a: float, b: float) -> float:
            return a + t * (b - a)

        severidad = { Estado.HABILITADO: 0.20, Estado.AGRIETADO: 0.65 }
        penalizacion = { Estado.HABILITADO: 0, Estado.AGRIETADO: 2 }

        x = interpolacion_lineal(severidad[self.estado], self.min, self.max)
        return x + penalizacion[self.estado]

    def __repr__(self):
        return f"Arista(min={self.min}, max={self.max}, estado={self.estado.name})"


type Nodo = str
type Grafo = dict[Nodo, list[tuple[Nodo, Arista]]]


class MinHeap:
    class Elemento:
        def __init__(self, inicio: Nodo, fin: Nodo, arista: Arista):
            self.inicio = inicio
            self.fin = fin
            self.arista = arista

        def __repr__(self):
            return f"MinHeap.Elemento(inicio={self.inicio}, fin={self.fin}, arista={self.arista})"

    def __init__(self):
        self.lista: list[Elemento] = []

    def __len__(self):
        return len(self.lista)

    def padre(self, i: int):
        return (i - 1) // 2

    def hijo_izquierdo(self, i: int):
        return 2 * i + 1

    def hijo_derecho(self, i: int):
        return 2 * i + 2

    def intercambiar(self, i: int, j: int):
        self.lista[i], self.lista[j] = self.lista[j], self.lista[i]

    def peso(self, i: int):
        return self.lista[i].arista.peso_efectivo()

    def encolar(self, inicio: Nodo, fin: Nodo, arista: Arista):
        i = len(self.lista)
        self.lista.append(MinHeap.Elemento(inicio, fin, arista))
        while i > 0 and self.peso(self.padre(i)) > self.peso(i):
            self.intercambiar(i, self.padre(i))
            i = self.padre(i)

    def sift_down(self, i: int):
        mayor: int = i
        izq: int = self.hijo_izquierdo(i)
        der: int = self.hijo_derecho(i)

        if izq < len(self.lista) and self.peso(izq) > self.peso(mayor):
            mayor = izq
        if der < len(self.lista) and self.peso(der) > self.peso(mayor):
            mayor = der

        if mayor != i:
            self.intercambiar(i, mayor)
            self.sift_down(mayor)

    def desencolar(self) -> tuple[Nodo, Nodo, Arista]:
        assert(len(self.lista) > 0)
        menor: Elemento = self.lista[0]
        self.lista[0] = self.lista.pop()
        self.sift_down(0)
        return menor.inicio, menor.fin, menor.arista


def prim(grafo: Grafo, POI_inicial: Nodo):
    mst: list[tuple[Nodo, Nodo, Arista]] = []
    cola = MinHeap()

    visitados = set([POI_inicial])
    for vecino, arista in grafo[POI_inicial]:
        cola.encolar(POI_inicial, vecino, arista)

    while len(cola) > 0 and len(visitados) < len(grafo):
        inicio, fin, arista = cola.desencolar()
        if fin not in visitados:
            mst.append((inicio, fin, arista))
            visitados.add(fin)
            for vecino, arista_vecino in grafo[fin]:
                peso_vecino = arista_vecino.peso_efectivo()
                if vecino not in visitados and peso_vecino < float('inf'):
                    cola.encolar(fin, vecino, arista_vecino)
    return mst


def main():
    grafo = {
        'A': [('B', Arista(2, 4, Estado.HABILITADO)), ('C', Arista(1, 6, Estado.AGRIETADO))],
        'B': [('A', Arista(2, 4, Estado.HABILITADO)), ('D', Arista(2, 5, Estado.AGRIETADO))],
        'C': [('A', Arista(1, 6, Estado.AGRIETADO)), ('D', Arista(1, 3, Estado.HABILITADO))],
        'D': [('B', Arista(2, 5, Estado.AGRIETADO)), ('C', Arista(1, 3, Estado.HABILITADO))]
    }
    mst = prim(grafo, 'A')
    print(mst)


if __name__ == "__main__":
    main()
