from leerDatos import ParseCasosConfirmados
from grafica_mat import Linea_mat
from grafica_pygal import Linea_pygal, Box_pygal
from clases_base import Grafica
from grafica_ploty import Lineas_plotly, Barras_plotly

# NO ES UN PATRON FACTORY, tengo que cambiarle el nombre y actualizar las referencias
class Factory:

    # este metodo devolvera el tipo de parse dependiendo de la ruta
    # To do analizar la ruta para decidir el tipo de parse | para esto primero hay que arreglar la estructura de los parse
    def parse(ruta):
        return ParseCasosConfirmados(ruta)

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
    # Antiguo metodo que no funcina
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
    def grafica(eleccion,contexto):
        # Funcionamiento del switch: declaramos un diccionario con las funciones, ( fijarse que en la declaracion de las funciones no estan los parentesis para que no las ejecute si no que las pase en tipo str)
        # con el get sacamos la funcion
        # Con la cadena le ponemos los parentesis para ejecutarla
        switcher = {
             1: Factory.lineaMat,
             2: Factory.lineaPygal,
             3: Factory.lineaPlotly,
             4: Factory.barrasPlotly,
             0: Factory.finPrograma
        }
        #print(type(eleccion))
        elec = switcher.get(int(eleccion))
        elec(contexto)

        # no se si hacer return del propio contexto o con cambiar su atributo basta

    def lineaMat(contexto):
        contexto.setGrafica(Linea_mat)

    def lineaPygal(contexto):
        contexto.setGrafica(Linea_pygal)

    def lineaPlotly(contexto):
        contexto.setGrafica(Lineas_plotly)

    def barrasPlotly(contexto):
        contexto.setGrafica(Barras_plotly)

    def finPrograma(a):
        print("Fin de la ejecución")




#gfsdfgsdf
