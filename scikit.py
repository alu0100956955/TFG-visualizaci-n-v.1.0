# Librerias
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.isotonic import IsotonicRegression
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
import math
import itertools
from sklearn.metrics import mean_squared_error, mean_absolute_error
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.preprocessing import LabelEncoder
import random # para poder generar los colores de forma random

# Para mostrar la matriz de confusion con matplolib
# https://stackoverflow.com/questions/19233771/sklearn-plot-confusion-matrix-with-labels

class Scikit:
    # Metodo para poder obtener las labels en tipo int de los ejes que sean de tipo string
    # Ya que los ejes de tipo string no los admite los metodos que estan desarrollados
    def StringAxis(eje):
        columna='label'
        lab = LabelEncoder()
        df = pd.DataFrame(eje,columns=[columna])
        df[columna] = lab.fit_transform(df[columna]) 
        return df[columna].tolist()

    #Metodo para verificar si el eje es de tipo String
    # En caso de ser tipo string devuelve solo el string original
    def VerificarEje(ejeOriginal):
        ejeLabel= False
        if(isinstance(ejeOriginal[0],str) ): # Si es de tipo string lo pone tipo label
            return Scikit.StringAxis(ejeOriginal),ejeOriginal # Como el eje orignal tiene los string lo mando como label
        return ejeOriginal, ejeLabel
    
    # ejes viene en tupla
    def VerificarEjes(ejes):
        ejex, ejey = list(zip(*ejes))
        ejex,xlabels= Scikit.VerificarEje(ejex)
        ejey,ylabels= Scikit.VerificarEje(ejey)
        ejes= list(zip(ejex,ejey))
        #ejesLabel= list(zip(xlabels,ylabels)) # solo devuelvo el eje por que la etiquetas ya estan en los metodos que lo usan
        return ejes

    def dibujarDispersionInicial(data,dimension1,dimension2, posicion, titulo):
        seleccionados = data.getSeleccionados()
        plt.subplot(dimension1, dimension2, posicion)
        for i in range(len(seleccionados)):
            r = random.random()
            b = random.random()
            g = random.random()
            colour = (r, g, b)
            color = [colour for i in range(len(data.getEje(data.getSeleccionEjeY(),seleccionados[i])))]
            plt.scatter(data.getEje(data.getSeleccionEjeX(),seleccionados[i]),data.getEje(data.getSeleccionEjeY(),seleccionados[i]),c=color, label=seleccionados[i])
            
        plt.legend()
        plt.title(titulo)
        plt.xlabel(data.getSeleccionEjeX())
        plt.ylabel(data.getSeleccionEjeY())

    def dibujarDispersion(ejex, ejey,titulo, colores, dimension1, dimension2, posicion, xlabel, ylabel,etiqueta):
        #ejex,ejey = zip(*datos)
        color = list(set(colores)) # Los colores es un array que indica con int que clusters colorea según el punto ej [1,1,0,1,0,1,0,0]
        plt.subplot(dimension1, dimension2, posicion)
        #print(colores)
        x = []
        y = []
        co = []
        if(isinstance(etiqueta,str)):
            etiqueta = [etiqueta] * len(color)
        for i in color:
            r = random.random()
            b = random.random()
            g = random.random()
            colour = (r, g, b)
            #co = [colour for _ in range(len(ejex)) ] # Monto el array con el color del mismo len que el eje, ç
            # pero como no todos los elementos son los que quiero no lo puedo hacer asi
            for z in range(len(ejex)): # Solo guardo los elementos de los ejes que ha distinguido el cluster
                if(colores[z] == i ):
                    x.append(ejex[z])
                    y.append(ejey[z])
                    co.append(colour)
            plt.scatter(x,y, c = co,label = etiqueta[i] + str(i+1))
            x.clear()
            y.clear()
            co.clear()

        
        #plt.scatter(ejex,ejey, c = colores)
        plt.title(titulo)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()

    def show():
        pass

# Como por ahora las tres clases representan de la misma forma por ahora empleo esta clase para representar pasandole el algoritmo
# Clase para representar los metodos de clasificacion
class Representacion:

    def show(data, algoritmo_):

        plt.clf() # Para limpiar las gracicas anteriores y que no se mezcle
        algoritmo = algoritmo_()
        training_accuracy = []
        test_accuracy = []
        dimensionx = 2
        dimensiony = 2
        porcentajeTesteo = 0.4


        # Para los datos combinare los datos de los dos ejes empleando zip
        # Las etiquetas seran las opciones escogidas
        datos, etiquetas, Xlabels, Ylabels = Representacion.DatosEtiquetas(data,True)


        # Cambio el porcentaje de entrenamiento y testeo
        porcentajes = np.arange(0.3, 0.9, 0.05)
        for porcentaje in porcentajes:    # Bucle para hacer la gr�fica


            # El primero seran los datos el segundo las etiquetas
            X_train, X_test, y_train, y_test = train_test_split(datos, etiquetas, test_size=porcentaje , random_state=0)
            algoritmo.fit(X_train, y_train)    
            # record training set accuracy    
            training_accuracy.append(algoritmo.score(X_train, y_train))    
            # record generalization accuracy    
            test_accuracy.append(algoritmo.score(X_test, y_test))
            


        
        # En los datos estan los datos de los ejes por lo que en X_train y X_test estan los datos para representar los ejes
        # En y_test e y_train estan las etiquetas, por lo que ojo cuidado a la hora de usar estas variables
        # Para cambiar el tamaño del set de pruebas | el test_size es bueno que sea más pequeño que el train set
        datos, etiquetas, Xlabels, Ylabels = Representacion.DatosEtiquetas(data,False) # False para no verificar los ejes y que vengan en string
        X_train, X_test, y_train, y_test = train_test_split(datos, etiquetas, test_size=porcentajeTesteo , random_state=0)

        # 1º grafiaca Representacion de los datos de entrenamiento

        ejex, ejey = zip(*X_train)
        ejex=list(ejex)
        ejey=list(ejey)
        #https://stackoverflow.com/questions/8528178/list-of-zeros-in-python
        #colores = [0] * len(ejex)
        colores= Representacion.coloresClasificacion(y_train ,len(ejex))
        plt.subplot(dimensionx, dimensiony, 1)

        plt.scatter(ejex,ejey,c=colores, label= "Entrenamiento")
        plt.title(" Datos de entrenamiento " + str(((1- porcentajeTesteo) * 100))  + "%" )
        plt.ylabel(data.getSeleccionEjeY())
        plt.xlabel(data.getSeleccionEjeX())

        # 2º grafica Representacion de los datos de testeo
        auxX,auxY = zip(*X_test)
        colores2 = Representacion.coloresClasificacion(y_test ,len(auxX))
        Scikit.dibujarDispersion(auxX,auxY, "Datos a clasificar" + str(( porcentajeTesteo * 100))  + "%" ,
                                 colores2, dimensionx,dimensiony,2, data.getSeleccionEjeX(),data.getSeleccionEjeY(),
                                 list(set(y_train))) # Uso y_train para seguir el orden inicial de posicion de los colores
       
        #Ahora le añado los valores de testeo, para que? | osea tendría que mostar solo los de testeo y pasarlos por el modelo
        #ejex.extend(auxX) 
        #ejey.extend(auxY)
        #colores.extend(Representacion.coloresClasificacion(y_test ,len(auxX)))

        #3º gráfica representacion del accuraci del metodo con los diferentes porcentajes en las pruebas
        plt.subplot(dimensionx, dimensiony, 3)
        plt.plot(porcentajes, training_accuracy, label="training accuracy")
        plt.plot(porcentajes, test_accuracy, label="test accuracy")
        plt.ylabel("Accuracy")
        plt.xlabel("Porcentaje de conjunto de pruebas")
        plt.legend()
        plt.title("Precisión")

        # 4º gráfica, representación de los datos de testeo con las etiquetas que precide el modelo
        # Como los datos pueden estar en formato string tengo que verificar los ejes para poder 
        X_train = Scikit.VerificarEjes(X_train)
        algoritmo.fit(X_train, y_train) # Entreno el modelo  
        ejex,ejey = list(zip(*X_test)) # Separa X_test por que es la que contiene los datos de los dos ejes 
        X_test = Scikit.VerificarEjes(X_test)
        colores = Representacion.coloresClasificacionFit(algoritmo.predict(X_test), data.getSeleccionados()) # Hago el predict con los datos de testeo
        
        Scikit.dibujarDispersion(ejex,ejey, "Datos clasificados",colores, dimensionx,dimensiony,4, data.getSeleccionEjeX(),data.getSeleccionEjeY(),list(set(y_train))) # Uso y_train para seguir el orden inicial de posicion de los colores


        plt.suptitle(algoritmo_.__name__) # para mostrar el modelo que se esta representando
        plt.tight_layout() # Para dar espacio a las subgraficas

        # 5º gráfica, la matriz de confusión
        disp = metrics.plot_confusion_matrix(algoritmo, X_test, y_test, normalize = 'true')
        disp.figure_.suptitle("Confusion Matrix")

        plt.show()

        # Devuelve los datos y las etiquetas necesarias para que tire el sistema
    def DatosEtiquetasAntiguo(data):
        datos = []
        etiquetas = []

        # Buble que por cada escogido se mezclaran los datos y añadiremos a datos, junto a su etiqueta en etiquetas
        seleccionados = data.getSeleccionados()
        for selec in seleccionados:
            EjeX,Xlabels = Scikit.VerificarEje(data.getEje(data.getSeleccionEjeX(),selec))
            EjeY,Ylabels = Scikit.VerificarEje(data.getEje(data.getSeleccionEjeY(),selec))
            aux = list(zip(EjeX,EjeY ))
            for i in range(len(aux)):
                etiquetas.append(selec)
            datos += aux 
        return datos, etiquetas, Xlabels, Ylabels

    def DatosEtiquetas(data,verificar):
        etiquetas = []

        # Verificare los datos fuera para poder tener los ejes sin transformar y poderlos representar
        seleccionados = data.getSeleccionados()
        if(verificar):
            EjeX,Xlabels = Scikit.VerificarEje(data.getEjes(data.getSeleccionEjeX(),seleccionados))
            EjeY,Ylabels = Scikit.VerificarEje(data.getEjes(data.getSeleccionEjeY(),seleccionados))
        else:
            EjeX = data.getEjes(data.getSeleccionEjeX(),seleccionados)
            EjeY = data.getEjes(data.getSeleccionEjeY(),seleccionados)
        Xlabels= False
        Ylabels = False
        datos = list(zip(EjeX,EjeY ))
        # Este doble bucle no me gusta pero voy muy justo de tiempo
        for selec in seleccionados:
            for i in range(len(data.getEje(data.getSeleccionEjeX(),selec))):
                etiquetas.append(selec) 
        return datos, etiquetas, Xlabels, Ylabels


    def coloresClasificacion(labels,lenth):
        # Le pasaremos el array con todos las labels y el tamaño del ejex, 
        # Devolvemos la lista de colores
        #print("Colores clasificacion")
        colores = []
        uniqueLabel = list(set(labels)) # Obtengo una lista sin duplicados de las etiqutas
        for i in range(lenth):
            colores.append(uniqueLabel.index(labels[i-1])) # Guardo la posición dentro del vector de unicos 
            # De esta forma tendre un array de "colores" del mismo tamaño del ejex
        return colores
    def coloresClasificacionFit(clasificacion,opciones):
        # Le pasaremos el array con todos los datos clasificados y las opciones escogias, crearemos un metodo que recorra las opciones escogidas y dependiendo de que pos este le de esa num de pos a esa etiqueta
        # Recorreremos el array y por cada componente llameros la funcion, guardaremos el resultado en una lista
        # Devolvemos la lista
        colores = []
        for i in clasificacion:
            colores.append(opciones.index(i))

        return colores


class AllClasification:

    def show(data):
            plt.clf() # Para limpiar las gracicas anteriores y que no se mezcle
            seleccionados = data.getSeleccionados() # Las opciones seleccionadas
            cantidadSeleccionados = len(seleccionados) # la cantidad de opciones seleccionadas
            #dim = Regresion.dimensiones(cantidadSeleccionados) # con la cantidad de seleccionados genero las dimensiones para el subplot

            modelos = [GaussianNB, KNeighborsClassifier, DecisionTreeClassifier] # modelos de clasificacion
            #ejex, ejey, Xlabels, Ylabels  = Regresion.combinacionDatos(data) # Y esto aqui?
            colores = ['red','green','yellow','cyan','indigo','maroon','teal','gold','orange','coral']

            # Para los datos combinare los datos de los dos ejes empleando zip
            datos, etiquetas, Xlabels, Ylabels = Representacion.DatosEtiquetas(data,False)
            datosV = Scikit.VerificarEjes(datos)
            contador = 1 # VAriable para controlar la subgrafica actual

            dimensionx = len(modelos)
            dimensiony = 2 # dos columnas para cada metodo de grafica
            for i in range(len(modelos)):
                algoritmo = modelos[i]()
                training_accuracy = []
                test_accuracy = []

                # Cambio el porcentaje de entrenamiento y testeo
                porcentajes = np.arange(0.4, 0.9, 0.05)
                for porcentaje in porcentajes:    # Bucle para hacer la gr�fica


                    # El primero seran los datos el segundo las etiquetas
                    X_train, X_test, y_train, y_test = train_test_split(datosV, etiquetas, test_size=porcentaje , random_state=0)
                    algoritmo.fit(X_train, y_train)    
                    # record training set accuracy    
                    training_accuracy.append(algoritmo.score(X_train, y_train))    
                    # record generalization accuracy    
                    test_accuracy.append(algoritmo.score(X_test, y_test))

                # La primera grafica la encargada de ver como de eficiente es el algoritmo
                plt.subplot(len(modelos),2,contador)
                plt.plot(porcentajes, training_accuracy, label="training accuracy")
                plt.plot(porcentajes, test_accuracy, label="test accuracy")
                plt.ylabel("Accuracy")
                plt.xlabel("Porcentaje de conjunto de pruebas")
                plt.legend()

                contador = contador + 1 # para la siguiente sub grafica
                #La segunda gráfica 
                #plt.subplot(len(modelos),2,contador)
                
                colores = Representacion.coloresClasificacionFit(algoritmo.predict(datosV), data.getSeleccionados())
                ejex, ejey = list(zip(*datos))

                Scikit.dibujarDispersion(ejex,ejey, algoritmo.__class__.__name__,colores, dimensionx,dimensiony,contador, data.getSeleccionEjeX(),data.getSeleccionEjeY(),data.getSeleccionados())

                contador = contador + 1
  
            plt.tight_layout() # Para dar espacio a las subgraficas
            plt.show()



class Gausian:

    def show(data):
        Representacion.show(data,GaussianNB)


class Kneighbors:

    def show(data):
        Representacion.show(data,KNeighborsClassifier)


class Tree:

    def show(data):
        Representacion.show(data,DecisionTreeClassifier)

# ///////////////////////////////////////////////////// REGRESION ////////////////////////////////////////////////////////////////////////

class Regresion:
    # https://matplotlib.org/3.1.0/gallery/color/named_colors.html Lista de colores de matplotlib
    def show(data, modelo,reshape): # Arreglar el parametro extra
        # Si pasan varias opciones se podria hacer un bucle que habra varias veces estas graficas
        # Tambien podria representar solo la grafica final, siendo un color para los datos de entrenamiento otro para los datos de testeo y la linea

        plt.clf() # Para limpiar las gracicas anteriores y que no se mezcle
        seleccionados = data.getSeleccionados() # Las opciones seleccionadas
        cantidadSeleccionados = len(seleccionados) # la cantidad de opciones seleccionadas
        dim = Regresion.dimensiones(cantidadSeleccionados) # con la cantidad de seleccionados genero las dimensiones para el subplot

        mean_squared = [] # para guardar el error cuadratico
        mean_absolute = [] # para guardar el error absoluto

        for i in range(cantidadSeleccionados):
            # TODO: Tendria que controlar si se pasa un eje no numerico
            #EjeX,Xlabels = Scikit.VerificarEje(data.getEje(data.getSeleccionEjeX(),seleccionados[i]))
            #EjeY,Ylabels = Scikit.VerificarEje(data.getEje(data.getSeleccionEjeY(),seleccionados[i]))

            #X_train, X_test, y_train, y_test = train_test_split( EjeX, EjeY, test_size=0.6, random_state=0)
            X_train, X_test, y_train, y_test = train_test_split(data.getEje(data.getSeleccionEjeX(),seleccionados[i]),data.getEje(data.getSeleccionEjeY(),seleccionados[i]), test_size=0.6, random_state=0)
            # Para meter las strin, tengo que hacer que el split sea como en la clasificacion
            # Que el ejeX tenga los datso y zipearlos mientras en el y las labels

            model = modelo()
            X_train,ejex = Scikit.VerificarEje(X_train)
            y_train,ejey = Scikit.VerificarEje(y_train)
            if(reshape):
                X_train = np.reshape(X_train, (-1, 1))
            model.fit(X_train,y_train) # FIT ¡¡¡
            
            X_test,ejex_t = Scikit.VerificarEje(X_test)
            X_test =  np.sort(X_test, kind = 'mergesort') # Ordeno de menor a mayor, antes de hacer el reshape por que sino no me deja ordenar con este metodo
            if(reshape):    # if es de tipo isotonic no hago el reshape
                X_test = np.reshape(X_test, (-1, 1))
            regresion_y = model.predict(X_test) # PREDICT ¡¡¡
            plt.subplot(dim, dim, i+1)
            if isinstance( ejex,bool):
                ejex = X_train
            if isinstance( ejey,bool):
                ejey = y_train
            plt.scatter(ejex,ejey)
            plt.plot(X_test, regresion_y,c = 'red') 
            plt.title(seleccionados[i])
            plt.xlabel(data.getSeleccionEjeX())
            plt.ylabel(data.getSeleccionEjeY())
            

            predict = model.predict(X_train)
            mean_squared.append(mean_squared_error(y_train, predict)) # La y_train tiene los datos originales para comprarlos con la predicción
            mean_absolute.append(mean_absolute_error(y_train, predict))


        # hago una subgrafica con los errores absoluto y cuadratico
        errores = ["Cuadratic","Absolute"]

        plt.subplot(dim, dim, cantidadSeleccionados+1)
        plt.bar(seleccionados,mean_squared, label="Error cuadratico" )
        plt.title("Error Cuadratico")
        plt.xlabel(data.getSeleccionEjeX())
        plt.ylabel(data.getSeleccionEjeY())

        plt.subplot(dim, dim, cantidadSeleccionados+2)
        plt.bar(seleccionados, mean_absolute, label = "Error absoluto")
        plt.title("Error Absoluto")
        plt.xlabel(data.getSeleccionEjeX())
        plt.ylabel(data.getSeleccionEjeY())
        
        plt.suptitle(modelo.__name__)
        plt.tight_layout() # Para dar espacio a las subgraficas

        plt.show()

        # Metodo para calcular la dimension de los subplot
    def dimensiones(cantidad):
        # devuelvo la raiz redondeada hacia arriba de 
        return math.ceil(math.sqrt(cantidad+2)) # Se le suma 2 para poder meter la subgrafica de los errores medio y cuadratico

    def combinacionDatos(data):
        ejex = []
        ejey = []
        seleccionados = data.getSeleccionados()
        for i in range(len(seleccionados)):
            if i == 0:
                ejex,Xlabels = Scikit.VerificarEje(data.getEje(data.getSeleccionEjeX(),seleccionados[i]))
                ejex,Ylabels = Scikit.VerificarEje(data.getEje(data.getSeleccionEjeY(),seleccionados[i]))
            EjeX,Xlabels = Scikit.VerificarEje(data.getEje(data.getSeleccionEjeX(),seleccionados[i]))
            EjeY,Ylabels = Scikit.VerificarEje(data.getEje(data.getSeleccionEjeY(),seleccionados[i]))
            ejex += EjeX
            ejey += EjeY
            
        return ejex, ejey , Xlabels, Ylabels



 # slice notation https://stackoverflow.com/questions/509211/understanding-slice-notation
 # Una gráfica por metodo y opcion seleccionada
 # https://stackoverflow.com/questions/5993206/is-it-possible-to-have-multiple-pyplot-windows-or-am-i-limited-to-subplots
class AllRegresion2:

    def show(data):

        plt.clf() # Para limpiar las gracicas anteriores y que no se mezcle
        seleccionados = data.getSeleccionados() # Las opciones seleccionadas
        cantidadSeleccionados = len(seleccionados) # la cantidad de opciones seleccionadas
        dim = Regresion.dimensiones(cantidadSeleccionados) # con la cantidad de seleccionados genero las dimensiones para el subplot
        ejex = []
        ejey = []
        modelos = [IsotonicRegression, LinearRegression, GradientBoostingRegressor ]
        #ejex, ejey = Regresion.combinacionDatos(data)
        colores = ['red','green','yellow','cyan','indigo','maroon','teal','gold','orange','coral']
        seleccionados = data.getSeleccionados()
        cantidadSeleccionados = len(seleccionados) # no creo que haga falta sumar + 2 # sumo dos para poder mostrar los erroes
        cantidadModelos = len(modelos) + 2 # sumo dos para poder mostrar los errores
        indiceSubgrafica = 1
        dimensionx = 2
        dimensiony = len(modelos)
        for i in range(len(seleccionados)):
            #EjeX,Xlabels = Scikit.VerificarEje(data.getEje(data.getSeleccionEjeX(),seleccionados[i]))
            #EjeY,Ylabels = Scikit.VerificarEje(data.getEje(data.getSeleccionEjeY(),seleccionados[i]))

            #X_train, X_test, y_train, y_test = train_test_split( EjeX , EjeY , test_size=0.6, random_state=0) # dimensiones de los X-train
            X_train, X_test, y_train, y_test = train_test_split(data.getEje(data.getSeleccionEjeX(),seleccionados[i]),data.getEje(data.getSeleccionEjeY(),seleccionados[i]), test_size=0.6, random_state=0)
            
            mean_squared = [] # para guardar el error cuadratico
            mean_absolute = [] # para guardar el error absoluto
            plt.figure(i) # Sera una ventana por cada opción
            #print(np.shape(X_train))

            X_train,ejex = Scikit.VerificarEje(X_train)
            y_train,ejey = Scikit.VerificarEje(y_train)
            X_test,ejex_t = Scikit.VerificarEje(X_test)
            for j in range(len(modelos)):
                
                #plt.subplot(cantidadSeleccionados, cantidadModelos, indiceSubgrafica)  # Para marcar los subplots de las graficas
                plt.subplot(dimensionx, dimensiony, j+1) # El indice no puede ser 0
                indiceSubgrafica = indiceSubgrafica + 1
                model = modelos[j]()
                
                if(j != 0):
                    X_train = np.reshape(X_train, (-1, 1))
                model.fit(X_train,y_train) # FIT ¡¡¡

                
                X_test =  np.sort(X_test, kind = 'mergesort') # Ordeno de menor a mayor, antes de hacer el reshape por que sino no me deja ordenar con este metodo
                if(j != 0):    # if es de tipo isotonic no hago el reshape
                    X_test = np.reshape(X_test, (-1, 1))

                regresion_y = model.predict(X_test)

                predict = model.predict(X_train)
                mean_squared.append(mean_squared_error(y_train, predict)) # La y_train tiene los datos originales para comprarlos con la predicción
                mean_absolute.append(mean_absolute_error(y_train, predict))

                if isinstance( ejex,bool):
                    ejex = X_train
                if isinstance( ejey,bool):
                    ejey = y_train
                plt.scatter(ejex,ejey)
                plt.plot(X_test, regresion_y,c = colores[i]) # repretar varias, cada una con su leyenda, con color <----------------
                plt.title(model.__class__.__name__)
                plt.xlabel(data.getSeleccionEjeX())
                plt.ylabel(data.getSeleccionEjeY())
                
                

            #plt.figure() # Un ultima ventana para los errores
            graficas = ["Isotonic", "Linear", "Gradient"]
            #plt.subplot(cantidadSeleccionados, cantidadModelos, indiceSubgrafica)
            plt.subplot(dimensionx, dimensiony, len(modelos)+1)
            indiceSubgrafica = indiceSubgrafica + 1
            plt.bar(graficas,mean_squared, label="Error cuadratico" )
            plt.title("Error Cuadratico")
            plt.xlabel(data.getSeleccionEjeX())
            plt.ylabel(data.getSeleccionEjeY())

            #plt.subplot(cantidadSeleccionados, cantidadModelos, indiceSubgrafica)
            plt.subplot(dimensionx, dimensiony, len(modelos)+2)
            indiceSubgrafica = indiceSubgrafica + 1
            plt.bar(graficas, mean_absolute, label = "Error absoluto")
            plt.title("Error Absoluto")
            plt.xlabel(data.getSeleccionEjeX())
            plt.ylabel(data.getSeleccionEjeY())

            plt.suptitle(seleccionados[i])
            plt.tight_layout()


        #plt.tight_layout() # Para dar espacio a las subgraficas | no va bien
        #plt.subplots_adjust(left=0.05,right=1.05,top=0.8)
        #plt.subplots_adjust(hspace=0.23)
        #plt.subplots_adjust(left=0.06,bottom=0.08, right=0.95,top=0.93)
        plt.show()


class Linear:


    def show(data):
        Regresion.show(data,LinearRegression,True)

class Gradient: # falta incluirlo en las referencias y los import

    def show(data):
        Regresion.show(data,GradientBoostingRegressor,True)  # Habria que añadir parametros extra

class Isotonic:

    def show(data):
        Regresion.show(data,IsotonicRegression,False)

# //////////////////////////// CLUSTERING ///////////////////////////////////

class Clustering:

    def show(data, modelo):

        plt.clf() # Para limpiar las gracicas anteriores y que no se mezcle
        seleccionados = data.getSeleccionados() # Las opciones seleccionadas, pero para que guardarlo si puede llamar a este procedimiento?
        cantidadSeleccionados = len(seleccionados) # la cantidad de opciones seleccionadas
        dimensionx = 1 # La cantidad de filas para los subplots
        dimensiony = 2 # La cntidad de columnas para los subplots
        #Clustering.dibujarDatosIniciales(data,dimensionx,dimensiony,1)
        Scikit.dibujarDispersionInicial(data,dimensionx,dimensiony,1, "Datos Pre Clustering" +data.getTitle())
        ejex, ejey , colores = Clustering.combinacionDatos(data) # Combinar para que?, si despues es más dificil mostrar las etiquetas
       
        

        # metodo clustering
        EjeX,Xlabels = Scikit.VerificarEje(ejex)
        EjeY,Ylabels = Scikit.VerificarEje(ejey)
        puntos = list(zip(EjeX,EjeY))
        
        if( isinstance(modelo(),KMeans)): # si el modelo es kmeans
            model = modelo(n_clusters = cantidadSeleccionados).fit(puntos)# solo se puede hacer esto si es KMeans
        if( isinstance(modelo(),GaussianMixture)): # si el modelo es Mixture
            model = modelo(n_components = cantidadSeleccionados)
        if( isinstance(modelo(),DBSCAN)): # si el modelo es DBscan
            model = modelo().fit(puntos)
        # entrenarlo
        y_km = model.fit_predict(puntos)
        # representarlo
        Scikit.dibujarDispersion(ejex, ejey, "Clustering", y_km,dimensionx,dimensiony,2,
                                  data.getSeleccionEjeX(),data.getSeleccionEjeY(),"Cluster ")
        
        plt.suptitle(modelo.__name__)
        plt.tight_layout() # Para dar espacio a las subgraficas
        #plt.legend(seleccionados)
        plt.show()


    # Metodo para combinar todos los datos de las opciones
    def combinacionDatos(data):
        ejex = []
        ejey = []
        colores = []
        seleccionados = data.getSeleccionados()
        if(data.pandas):
            for i in range(len(seleccionados)):
                if i == 0:
                    ejex = data.getEje(data.getSeleccionEjeX(),seleccionados[i])
                    ejey = data.getEje(data.getSeleccionEjeY(),seleccionados[i])
                ejex = np.append( ejex,  data.getEje(data.getSeleccionEjeX(),seleccionados[i]))
                ejey = np.append( ejey, data.getEje(data.getSeleccionEjeY(),seleccionados[i]))
                # Para tener los distintos colores de cada cluster
                for j in range(len(data.getEje(data.getSeleccionEjeY(),seleccionados[i]))):
                    colores.append(i)

            return ejex, ejey, colores
        else:
            for i in range(len(seleccionados)):
                if i == 0:
                    ejex = data.getEje(data.getSeleccionEjeX(),seleccionados[i])
                    ejey = data.getEje(data.getSeleccionEjeY(),seleccionados[i])
                ejex += data.getEje(data.getSeleccionEjeX(),seleccionados[i])
                ejey += data.getEje(data.getSeleccionEjeY(),seleccionados[i])
                # Para tener los distintos colores de cada cluster
                for j in range(len(data.getEje(data.getSeleccionEjeY(),seleccionados[i]))):
                    colores.append(i)

            return ejex, ejey, colores

class AllClustering:

    def show(data):

        plt.clf() # Para limpiar las gracicas anteriores y que no se mezcle
        seleccionados = data.getSeleccionados() # Las opciones seleccionadas
        cantidadSeleccionados = len(seleccionados) # la cantidad de opciones seleccionadas

        ejex, ejey , colores = Clustering.combinacionDatos(data)
        EjeX,Xlabels = Scikit.VerificarEje(ejex)
        EjeY,Ylabels = Scikit.VerificarEje(ejey)
        puntos = list(zip(EjeX,EjeY))
        
        modelos = [KMeans,GaussianMixture, DBSCAN]  # Los distintos tipos de clustering
        i = 1
        for modelo in modelos:
            if(isinstance(modelo(),KMeans)): 
                model = modelo(n_clusters = cantidadSeleccionados).fit(puntos)
            if(isinstance(modelo(),GaussianMixture)):
                model = modelo(n_components = cantidadSeleccionados)
            if(isinstance(modelo(),DBSCAN)):
                model = modelo()
            y_km = model.fit_predict(puntos)
            #Clustering.dibujardatos(ejex,ejey,model.__class__.__name__,y_km,1,3,i,data.getSeleccionEjeX(),data.getSeleccionEjeY())
            Scikit.dibujarDispersion(ejex,ejey,model.__class__.__name__,y_km,1,3,i,
                                       data.getSeleccionEjeX(),data.getSeleccionEjeY(), data.getSeleccionados())
            i = i+1
        plt.tight_layout() # Para dar espacio a las subgraficas
        plt.show()



class Kmeans:

    def show(data):
        Clustering.show(data,KMeans)

class Mixture:

    def show(data):
        Clustering.show(data,GaussianMixture)


class DBscan:

    def show(data):
        Clustering.show(data,DBSCAN)