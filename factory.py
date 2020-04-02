from leerDatos import Lector
from grafica_mat import Linea_mat
from grafica_bokeh import Grafica_bokeh
from grafica_pygal import Linea_pygal, Box_pygal
from clases_base import Grafica
from grafica_ploty import Lineas_plotly, Barras_plotly

class Factory:

    # este metodo devolvera el tipo de parse dependiendo de la ruta
    # To do analizar la ruta para decidir el tipo de parse | para esto primero hay que arreglar la estructura de los parse
    def parse(ruta):
        return Lector(ruta)

# tengo que hacer varias funciones y en funcion de la eleccion en el switch llarmarlas, ya que si intento devolver la clase directamente no me deja

    def lineas_mat() -> Grafica:
        return Linea_mat
    def lineas_pygal() -> Grafica:
        return Linea_pygal
    def lineas_bokeh() -> Grafica:
        return Grafica_bokeh
    def lineas_plotly() -> Grafica:
        return Lineas_plotly
    def barras_plotly() -> Grafica:
        return Barras_plotly

    # Nos devolera el tipo de grafica dependiendo de la eleccion
    # todavia esta muy rudo pero es que no esta definido correctamente la cantidad de grafica y como van a estar estructuradas
    def grafica(eleccion) -> Grafica:
        switcher = {
             1: Factory.lineas_mat(),
             2: Factory.lineas_pygal(),
             3: Factory.lineas_bokeh()
        }
        #print (type(switcher.get(eleccion)))
        fun = switcher.get(eleccion)
        print (type(fun))
        #aux = fun()
        #aux = Factory.lineas_mat()
        #aux = Factory.lineas_plotly()
        aux = Factory.barras_plotly()
        #print (type(aux))
        #return fun
        return aux


    # To do comprobar porque si encuentra la primera opcion por que me hace la segunda
    def grafica(eleccion,contexto) -> Grafica:
        switcher = {
             1: Factory.mat(contexto)#,
             #2: Factory.pygal(contexto)
        }
        elec = switcher.get(eleccion)
        # no se si hacer return del propio contexto o con cambiar su atributo basta

    def mat(contexto):
        contexto.setGrafica(Linea_mat)

    def pygal(contexto):
        contexto.setGrafica(Linea_pygal)




#gfsdfgsdf
