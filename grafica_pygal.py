from leerDatos import ParseCasosConfirmados
import pygal
from clases_base import Grafica
import numpy as np



class Linea_pygal(Grafica):

# TO DO
# probar mas tipos de graficas
# Cambiar la forma de pedir los datos en las graficas
#Comprobar el self de show
    def show(data):
        seleccionados = data.getSeleccionados()
        chart = pygal.Line(x_label_rotation=1) # de tipo linea la grafica
        #chart = pygal.Line()
        #chart = pygal.bar() # de tipo barras

        chart.title = data.getTitle()
        chart.x_labels = Linea_pygal.espaciar(data.getEjeX())  #para añadirle datos al ejex, se ve muy pequeño pero si se pasa el raton se ve bien
        for selec in seleccionados:
            chart.add(selec, data.getEjeY(selec))

        #chart.x_labels = l.labelsX(l.ejeX()) # no los reconoce como valores asique los apila igual pero como son menos pos quedan todos apretados al principio
        chart.render_to_file('output/lineas_pygal.html')
        #chart.render_in_browser()

    # del array de labels para el eje x, como no puedo alterar los espacios voy a dejar vacias las posiciones que no me interesan para que quede limpio en la grafica
    def espaciar(valores):
        for i in np.arange(0,valores.size):
            if(i%15 != 0): # Cada 10 valores dejo el original para que no este tan aglomerado
                # añadir espcios
                valores[i] = ""
        # devolver el array con las fechas sobreescritas
        return valores


class Box_pygal(Grafica):

        # es lo mismo pero solo varia la primera linea es decir la instancia pero en python tengo problemas para devolver nuevas instancias
    def show(data):
        seleccionados = data.getSeleccionados()
        chart = pygal.Box(box_mode="pstdev")


        chart.title = data.getTitle()
        chart.x_labels = Linea_pygal.espaciar(data.getEjeX())

        for selec in seleccionados:
            chart.add(selec, data.getEjeY(selec))
        chart.render_to_file('output/box_pygal.html')


    # del array de labels para el eje x, como no puedo alterar los espacios voy a dejar vacias las posiciones que no me interesan para que quede limpio en la grafica
    def espaciar(valores):
        tam = valores.size
        z = tam/7   # Este es para la cantidad de ticks, como quiero que solo salgan 7 etiquetas pos el modulo sera con el numero que salga como resultado
        for i in np.arange(0,tam):
            if(i%z != 0): # Cada 10 valores dejo el original para que no este tan aglomerado
                # añadir espcios
                valores[i] = ""
        # devolver el array con las fechas sobreescritas
        return valores

#parse = Factory.parse('data/casos_2019.csv')
#Box_pygal.show(parse)

#asdfasdf
