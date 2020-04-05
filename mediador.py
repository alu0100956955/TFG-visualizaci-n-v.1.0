from leerDatos import ParseCasosConfirmados
#from grafica_mat import Linea_mat
#from grafica_bokeh import Grafica_bokeh
#from grafica_pygal import Linea_pygal, Box_pygal
from interfaz_usuario import Usuario
from factory import Factory
from estrategia import ContextoGrafica

# La clase mediador debe de tener todas las clases ya que sera la que medie entre ellas

class Mediador:
    # el mediador no deberia de ser inicializado con la ruta ya que esa no es su principal labor o puede ser alterada mas adelante
    #def __init__(self,ruta): # con la ruta le pediremos al factory el parse
        #self.parse = Factory.parse(ruta)  # le pedimos al factory el parse que necesitamos dependiendo del fichero que le pasemos | Podria inicializarlo con la ruta

    # Llamo a la interfaz de usuario, esta me devuelve los valores del usuario, se los paso al parse, que me devulve las clases que necesito y ejecuto los metodos principales
    # TO DO: parametrizar la ruta de los datos
    def show():
        aux = 20
        contextoG = ContextoGrafica()
        paises = ['Spain','Italy','China','Portugal']
        while int(aux) != 0:
            #print(aux)
            contextoG.setPaises(paises)  # le pasamos al contexto los paises que se van a representar
            aux = Usuario.pedirGrafica() # Pedimos al usuario el tipo de grafica que quiere
            #print(type(aux))
            #grafica = Factory.grafica(aux) #El primer metodo que probe para el factory
            Factory.grafica(aux,contextoG)  # Le pasamos el contexto para que le indique que tipo de grafica usara
            #print(type(grafica))
            ruta = 'data/casos_2019.csv'
            ruta2 = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
            parse = Factory.parse(ruta2) # la ruta la pongo a mano por ahora ya vere como parametrizarla | hay que habilitar el contexto para los parse
            #grafica.show(parse)

            contextoG.show(parse)




# fsadgfsgfdg
