from leerDatos import Lector
import pygal

#l = Lector('data/casos_2019.csv')
class Grafica_pygal:

# TO DO
# probar mas tipos de graficas
#

    def show(l):
        chart = pygal.Line(x_label_rotation=60) # de tipo linea la grafica
        #chart = pygal.bar() # de tipo barras

        chart.title = 'Casos del coronavirus'
        chart.x_labels = l.ejeX()  #para añadirle datos al ejex, se ve muy pequeño pero si se pasa el raton se ve bien
        chart.add('Casos España', l.ejeY(18))
        chart.add('Casos Italia',l.ejeY(16))
        chart.add('Casos Hong kong', l.ejeY(183))
        chart.add('Casos Zhejiang', l.ejeY(160))
        #chart.x_labels = l.labelsX(l.ejeX()) # no los reconoce como valores asique los apila igual pero como son menos pos quedan todos apretados al principio
        chart.render_to_file('lineas_coronavirus2.svg')

        # del array de labels para el eje x, como no puedo alterar los espacios voy a dejar vacias las posiciones que no me interesan para que quede limpio en la grafica
        def espaciar(valores):
            for i in np.arange(0,valores.size):
                #if(): # si esta en el rango de valorees iniciales
                    # añadir espacio
                print('Sin terminar')
            # devolver el array con las fechas sobreescritas


#asdfasdf
