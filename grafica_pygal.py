from leerDatos import ParseCasosConfirmados
import pygal
from clases_base import Grafica



class Linea_pygal(Grafica):

# TO DO
# probar mas tipos de graficas
# Cambiar la forma de pedir los datos en las graficas
#Comprobar el self de show
    def show(data, seleccionados):
        chart = pygal.Line(x_label_rotation=60) # de tipo linea la grafica
        #chart = pygal.bar() # de tipo barras

        chart.title = data.getTitle()
        chart.x_labels = data.getEjeX()  #para añadirle datos al ejex, se ve muy pequeño pero si se pasa el raton se ve bien
        for selec in seleccionados:
            chart.add(selec, data.getEjeY(selec))

        #chart.x_labels = l.labelsX(l.ejeX()) # no los reconoce como valores asique los apila igual pero como son menos pos quedan todos apretados al principio
        chart.render_to_file('output/lineas_pygal.html')

    # del array de labels para el eje x, como no puedo alterar los espacios voy a dejar vacias las posiciones que no me interesan para que quede limpio en la grafica
    def espaciar(valores):
        for i in np.arange(0,valores.size):
            #if(): # si esta en el rango de valorees iniciales
                # añadir espacio
            print('Sin terminar')
        # devolver el array con las fechas sobreescritas


class Box_pygal(Grafica):

        # es lo mismo pero solo varia la primera linea es decir la instancia pero en python tengo problemas para devolver nuevas instancias
    def show(l):
        chart = pygal.Box(box_mode="pstdev")
        chart.add('Casos España', l.ejeY('Spain'))
        chart.add('Casos Italia',l.ejeY('Italy'))
        chart.add('Casos China', l.ejeY('China'))
        chart.render_to_file('output/box_coronavirus.svg')


#parse = Factory.parse('data/casos_2019.csv')
#Box_pygal.show(parse)

#asdfasdf
