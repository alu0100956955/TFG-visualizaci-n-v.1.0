

class ContextoGrafica:

    # Para cambiar el tipo de grafica que se emplea
    def setGrafica(self,Grafica):
        self.grafica = Grafica

    # la operacion de las graficas es el show por eso este nombre
    def show(self,parse):
        self.grafica.show(parse.getDataset(),self.seleccionados) # le pasamos el parse (por ahora) y el array de paises

    def setSeleccionados(self,p):
        self.seleccionados = p

#hgsfhsd
