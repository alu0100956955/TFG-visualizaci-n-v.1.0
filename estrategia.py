

class ContextoGrafica:

    # Para cambiar el tipo de grafica que se emplea
    def setGrafica(self,Grafica):
        self.grafica = Grafica

    # la operacion de las graficas es el show por eso este nombre
    def show(self,parse):
         data = parse.getDataset()
         data.setSeleccionados(self.seleccionados) # añadimos al dataset los seleccionados para las graficas que lo necesiten
         self.grafica.show(data) # le pasamos el dataset

    def setSeleccionados(self,p):
        self.seleccionados = p

#hgsfhsd
