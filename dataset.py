

# Clase que contendra los datos del parse
class Dataset:

    def __init__(self,title):
        self.title = title

    def setEjeY(self,matriz):
        self.ejey = matriz

    def getEjeY(self,eleccion):
        return self.searchRow(self.searchIndex(eleccion))

    def setEjeX(self,array):
        self.ejex = array


    def getEjeX(self):
        return self.ejex


    def getTitle(self):
        return self.title

    # Esto hay que eliminarlo no es optimo
    # En vez de set paises deberia ser setTodasLasOpciones, esto es debido a que son todas las opciones incluidos duplicados
    def setTodasLasOpciones(self, array):
        self.TOpciones = array

    # Le pasamos un pais y nos devulve un array con la posicion o posiciones del pais | en vez de pais que sea
    # Le indicamos la opcion que escogio el usuario y nos indica el indice de la fila en la que se encuentra
    def searchIndex(self, opcion):
        posicion = []   # Lo hago array por si hay mas de una opcion
        for index in range(len(self.TOpciones)):
            if(self.TOpciones[index] == opcion):
                posicion.append(index)
        return posicion

    # Le pasamos las posiciones del pais, busca las filas corresponcientes, las suma y nos devuelve el array resultado, si no encuentra nada devuelve el array con un cero
    def searchRow(self,posicion):
        primera = True
        rows = [0]
        for i in posicion:
            if(primera):
                primera = False
                rows = self.ejey[i]
                continue
            rows += self.ejey[i]
        return rows

    #Array con las distintas opciones de lo que se puede representar
    def setOpciones(self, opciones_):
        self.opciones= opciones_

    def getOpciones(self):
        return self.opciones

    def setSeleccionados(self, selec):
        self.seleccionados = selec

    def getSeleccionados(self):
        return self.seleccionados

    # Los datos para cada eje
    def addElementoMatrizOpcionesEje(self,opciones):
        self.matrizEje.append(opciones)

    # Las opciones para cada eje
    def setArrayOpcionesEje(self,array ):
        self.OpcionesEje = array


#asdfasf
