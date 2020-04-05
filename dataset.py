

# Clase que contendra los datos del parse
class Dataset:

    def __init__(self,title):
        self.title = title

    def setEjeY(self,matriz):
        self.ejey = matriz

    def getEjeY(self,eleccion):
        #return self.ejex # Hay que parametrizar el tipo de pais
        return self.searchRow(self.searchIndex(eleccion))

    def setEjeX(self,array):
        self.ejex = array


    def getEjeX(self):
        return self.ejex


    def getTitle(self):
        return self.title

    def setPaises(self, array):
        self.paises = array

    # Le pasamos un pais y nos devulve un array con la posición o posiciones del pais
    def searchIndex(self, pais):
        posicion = []
        for index in range(self.paises.size):
            if(self.paises[index] == pais):
                posicion.append(index)
        return posicion

    # Le pasamos las posiciones del pais, busca las filas corresponcientes, las suma y nos devuelve el array resultado
    def searchRow(self,posicion):
        primera = True
        #print(self.ejey)
        for i in posicion:
            if(primera):
                primera = False
                rows = self.ejey[i]
                continue
            rows += self.ejey[i]
        return rows

#asdfasf
