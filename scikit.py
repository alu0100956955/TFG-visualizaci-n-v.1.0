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

class auxiliar:
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
            return auxiliar.StringAxis(ejeOriginal),ejeOriginal # Como el eje orignal tiene los string lo mando como label
        return ejeOriginal, ejeLabel

# Como por ahora las tres clases representan de la misma forma por ahora empleo esta clase para representar pasandole el algoritmo
# Clase para representar los metodos de clasificacion
class Representacion:

    def show(data, algoritmo_):

        plt.clf() # Para limpiar las gracicas anteriores y que no se mezcle
        algoritmo = algoritmo_()
        training_accuracy = []
        test_accuracy = []
        #mean_squared = []
        #mean_absolute = []

        # Para los datos combinare los datos de los dos ejes empleando zip
        # Las etiquetas seran las opciones escogidas
        datos, etiquetas, Xlabels, Ylabels = Representacion.DatosEtiquetas(data)


        # Cambio el porcentaje de entrenamiento y testeo
        porcentajes = np.arange(0.4, 0.9, 0.05)
        for porcentaje in porcentajes:    # Bucle para hacer la gr�fica


            # El primero seran los datos el segundo las etiquetas
            X_train, X_test, y_train, y_test = train_test_split(datos, etiquetas, test_size=porcentaje , random_state=0)
            algoritmo.fit(X_train, y_train)    
            # record training set accuracy    
            training_accuracy.append(algoritmo.score(X_train, y_train))    
            # record generalization accuracy    
            test_accuracy.append(algoritmo.score(X_test, y_test))
            #predict = algoritmo.predict(X_train)
            #print(predict.shape())
            #print(len(X_train))
            #mean_squared = mean_squared_error(y_train, predict) # Necesita la Y que contiene las etiquetas ya que el predict al ser clasificacion devulve etiquetas
            #mean_absolute = mean_absolute_error(X_train, predict)


        

        # Para cambiar el tamaño del set de pruebas
        X_train, X_test, y_train, y_test = train_test_split(datos, etiquetas, test_size=0.7 , random_state=0)

        # Representacion de los datos de entrenamiento
        #print(X_train)
        #print(y_train)
        ejex, ejey = zip(*X_train)
        ejex=list(ejex)
        ejey=list(ejey)
        #print(type(ejex))
        #https://stackoverflow.com/questions/8528178/list-of-zeros-in-python
        colores = [0] * len(ejex)

        # Los 3 numeros representan: los dos primeros las dimensiones el tercero la posicion
        plt.subplot(321)

        plt.scatter(ejex,ejey,c=colores)
        plt.title(data.getTitle() + " Datos de entrenamiento")
        plt.ylabel(data.getSeleccionEjeY())
        plt.xlabel(data.getSeleccionEjeX())
        #if(isinstance(Xlabels,list)): 
        #    plt.xticks(ejex,Xlabels)
        #if(isinstance(Ylabels,list)):
        #    plt.yticks(ejey,Ylabels)
        #plt.show() # solo un show() ya que es como un exit()

        #Ahora le añado los valores de testeo

        auxX,auxY = zip(*X_test)
        for i in range(len(X_test)):
            colores.append(1)
            ejex.append(auxX[i])
            ejey.append(auxY[i])
    
        plt.subplot(322)
        # CODIGO DUPLICADO, podria hacer esto en un bucle y que lo otro fuese un metodo para añadir nuevos datos al scatter TODO
        plt.scatter(ejex,ejey, c=colores)
        plt.title(data.getTitle() + " Datos de Testeo")
        plt.ylabel(data.getSeleccionEjeY())
        plt.xlabel(data.getSeleccionEjeX())
        #if(isinstance(Xlabels,list)): 
        #    plt.xticks(ejex,Xlabels)
        #if(isinstance(Ylabels,list)):
        #    plt.yticks(ejey,Ylabels)
        #plt.show() # Solo un show ya que es como un exit()


        plt.subplot(323)
        plt.plot(porcentajes, training_accuracy, label="training accuracy")
        plt.plot(porcentajes, test_accuracy, label="test accuracy")
        plt.ylabel("Accuracy")
        plt.xlabel("Porcentaje de conjunto de pruebas")
        plt.legend()
        plt.title("Precisión")


        #plt.subplot(224)
        #coloresClasificacion
        #plt.scatter(ejex,ejey,c=coloresClasifiacion)
        #plt.title(data.getTitle() + " Clasificados")
        #plt.ylabel(data.getSeleccionEjeY())
        #plt.xlabel(data.getSeleccionEjeX())
        #plt.legend()
        #plt.show()    
    
        # https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/scatter_with_legend.html
        # fig, ax = 
        seleccionados = data.getSeleccionados()
        plt.subplot(324)
        colores = Representacion.coloresClasificacion(algoritmo.predict(datos), data.getSeleccionados())
        ejex, ejey = list(zip(*datos))
        plt.scatter(ejex, ejey , c = colores)
        #plt.legend(seleccionados)
        plt.title("Datos clasificados")
        plt.ylabel(data.getSeleccionEjeY())
        plt.xlabel(data.getSeleccionEjeX())
        #if(isinstance(Xlabels,list)): 
        #    plt.xticks(ejex,Xlabels)
        #if(isinstance(Ylabels,list)):
        #    plt.yticks(ejey,Ylabels)


        #plt.subplot(325)
        #plt.plot(porcentajes, mean_squared, label="Error cuadratico")
        #plt.plot(porcentajes, mean_absolute, label="Error absoluto")
        #plt.ylabel("Accuracy")
        #plt.xlabel("Porcentaje de conjunto de pruebas")
        #plt.legend()

        plt.suptitle(algoritmo_.__name__) # para mostrar el modelo que se esta representando
        plt.tight_layout() # Para dar espacio a las subgraficas

        #plt.subplot(224)  # No lo muestra como me gustaria puede deberse a como creo la matriz de confusión
        disp = metrics.plot_confusion_matrix(algoritmo, X_test, y_test, normalize = 'true')
        disp.figure_.suptitle("Confusion Matrix")
        print("Confusion matrix:\n%s" % disp.confusion_matrix)
        
        
        plt.show()

        # Devuelve los datos y las etiquetas necesarias para que tire el sistema
    def DatosEtiquetas(data):
        datos = []
        etiquetas = []

        # Buble que por cada escogido se mezclaran los datos y añadiremos a datos, junto a su etiqueta en etiquetas
        seleccionados = data.getSeleccionados()
        for selec in seleccionados:
            EjeX,Xlabels = auxiliar.VerificarEje(data.getEje(data.getSeleccionEjeX(),selec))
            EjeY,Ylabels = auxiliar.VerificarEje(data.getEje(data.getSeleccionEjeY(),selec))
            aux = list(zip(EjeX,EjeY ))
            for i in range(len(aux)):
                etiquetas.append(selec)
            datos += aux 
        return datos, etiquetas, Xlabels, Ylabels

    def coloresClasificacion(clasificacion,opciones):
        # Le pasaremos el array con todos los datos clasificados y las opciones escogias, crearemos un metodo que recorra las opciones escogidas y dependiendo de que pos este le de esa num de pos a esa etiqueta
        # Recorreremos el array y por cada componente llameros la funcion, guardaremos el resultado en una lista
        # Devolvemos la lista
        #print("Colores clasificacion")
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
            datos, etiquetas, Xlabels, Ylabels = Representacion.DatosEtiquetas(data)
            contador = 1 # VAriable para controlar la subgrafica actual
            for i in range(len(modelos)):
                algoritmo = modelos[i]()
                training_accuracy = []
                test_accuracy = []

                # Cambio el porcentaje de entrenamiento y testeo
                porcentajes = np.arange(0.4, 0.9, 0.05)
                for porcentaje in porcentajes:    # Bucle para hacer la gr�fica


                    # El primero seran los datos el segundo las etiquetas
                    X_train, X_test, y_train, y_test = train_test_split(datos, etiquetas, test_size=porcentaje , random_state=0)
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
                plt.subplot(len(modelos),2,contador)
                colores = Representacion.coloresClasificacion(algoritmo.predict(datos), data.getSeleccionados())
                ejex, ejey = list(zip(*datos))
                plt.scatter(ejex, ejey , c = colores, label=seleccionados )
                plt.title(algoritmo.__class__.__name__)
                plt.xlabel(data.getSeleccionEjeX())
                plt.ylabel(data.getSeleccionEjeY())

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

# ////////////////////////////// REGRESION ////////////////////////////////////

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
            EjeX,Xlabels = auxiliar.VerificarEje(data.getEje(data.getSeleccionEjeX(),seleccionados[i]))
            EjeY,Ylabels = auxiliar.VerificarEje(data.getEje(data.getSeleccionEjeY(),seleccionados[i]))

            X_train, X_test, y_train, y_test = train_test_split( EjeX, EjeY, test_size=0.6, random_state=0)
            
            if(reshape):
                X_train = np.reshape(X_train, (-1, 1))
            X_test =  np.sort(X_test, kind = 'mergesort') # Ordeno de menor a mayor, antes de hacer el reshape por que sino no me deja ordenar con este metodo
            if(reshape):    # if es de tipo isotonic no hago el reshape
                X_test = np.reshape(X_test, (-1, 1))
            #print(X_train)
            #print(y_train)

            model = modelo()
            model.fit(X_train,y_train)
            regresion_y = model.predict(X_test)
            plt.subplot(dim, dim, i+1)
            plt.scatter(X_train,y_train)
            plt.plot(X_test, regresion_y,c = 'red') # repretar varias, cada una con su leyenda, con color <----------------
            plt.title(seleccionados[i])
            plt.xlabel(data.getSeleccionEjeX())
            plt.ylabel(data.getSeleccionEjeY())
            if(isinstance(Xlabels,list)): 
                plt.xticks(EjeX,Xlabels)
            if(isinstance(Ylabels,list)):
                plt.yticks(EjeY,Ylabels)

            predict = model.predict(X_train)
            mean_squared.append(mean_squared_error(y_train, predict)) # La y_train tiene los datos originales para comprarlos con la predicción
            mean_absolute.append(mean_absolute_error(y_train, predict))

            # Linear regression y = xm + n
            #peso = model.coef_ # La pendiente, lo que multiplica por x
            #intercep = model.intercept_ # Intercep


            # Gradient regression y = 

            # Isotonic regresion y = 

        # hago una subgrafica con los errores absoluto y cuadratico
        errores = ["Cuadratic","Absolute"]

        plt.subplot(dim, dim, cantidadSeleccionados+1)
        plt.bar(seleccionados,mean_squared, label="Error cuadratico" )
        plt.title("Error Cuadratico")

        plt.subplot(dim, dim, dim+dim)
        plt.bar(seleccionados, mean_absolute, label = "Error absoluto")
        plt.title("Error Absoluto")
        
        plt.suptitle(modelo.__name__)
        plt.tight_layout() # Para dar espacio a las subgraficas
        # Para meter las subgraficas en la ventana 
        #root = tk.Tk() # para mostrar las subgraficas
        #root.wm_title("Regresiones")
        #canvas = FigureCanvasTkAgg(plt, master=root)
        #canvas.show()

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
                ejex,Xlabels = auxiliar.VerificarEje(data.getEje(data.getSeleccionEjeX(),seleccionados[i]))
                ejex,Ylabels = auxiliar.VerificarEje(data.getEje(data.getSeleccionEjeY(),seleccionados[i]))
            EjeX,Xlabels = auxiliar.VerificarEje(data.getEje(data.getSeleccionEjeX(),seleccionados[i]))
            EjeY,Ylabels = auxiliar.VerificarEje(data.getEje(data.getSeleccionEjeY(),seleccionados[i]))
            ejex += EjeX
            ejey += EjeY
            
        return ejex, ejey , Xlabels, Ylabels


    # Una gráfica por modelo, se combinan los datos de todas las opciones seleccionadas
class AllRegresion:

    def show(data):
        
        
        plt.clf() # Para limpiar las gracicas anteriores y que no se mezcle
        seleccionados = data.getSeleccionados() # Las opciones seleccionadas
        cantidadSeleccionados = len(seleccionados) # la cantidad de opciones seleccionadas
        dim = Regresion.dimensiones(cantidadSeleccionados) # con la cantidad de seleccionados genero las dimensiones para el subplot

        modelos = [LinearRegression, GradientBoostingRegressor, IsotonicRegression]
        ejex, ejey = Regresion.combinacionDatos(data)
        colores = ['red','green','yellow','cyan','indigo','maroon','teal','gold','orange','coral']
        for i in range(len(modelos)):
            # TODO: Tendria que controlar si se pasa un eje no numerico
            EjeX,Xlabels = auxiliar.VerificarEje(data.getEje(data.getSeleccionEjeX(),seleccionados[i]))
            EjeY,Ylabels = auxiliar.VerificarEje(data.getEje(data.getSeleccionEjeY(),seleccionados[i]))
            X_train, X_test, y_train, y_test = train_test_split(ejex, ejey, test_size=0.6, random_state=0)
            #print(np.shape(X_train))
            if(i != 2):
                X_train = np.reshape(X_train, (-1, 1))
            X_test =  np.sort(X_test, kind = 'mergesort') # Ordeno de menor a mayor, antes de hacer el reshape por que sino no me deja ordenar con este metodo
            if(i != 2):    # if es de tipo isotonic no hago el reshape
                X_test = np.reshape(X_test, (-1, 1))

            model = modelos[i]()
            #print(np.shape(X_train))
            model.fit(X_train,y_train)
            regresion_y = model.predict(X_test)
            plt.subplot(1, len(modelos), i+1)
            plt.scatter(X_train,y_train)
            plt.plot(X_test, regresion_y,c = colores[i]) # repretar varias, cada una con su leyenda, con color <----------------
            plt.title(model.__name__)
            if(isinstance(Xlabels,list)): 
                plt.xticks(EjeX,Xlabels)
            if(isinstance(Ylabels,list)):
                plt.yticks(EjeY,Ylabels)

        plt.tight_layout() # Para dar espacio a las subgraficas
        plt.show()

 # slice notation https://stackoverflow.com/questions/509211/understanding-slice-notation
 # Una gráfica por metodo y opcion seleccionada
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
        for i in range(len(seleccionados)):
            EjeX,Xlabels = auxiliar.VerificarEje(data.getEje(data.getSeleccionEjeX(),seleccionados[i]))
            EjeY,Ylabels = auxiliar.VerificarEje(data.getEje(data.getSeleccionEjeY(),seleccionados[i]))

            X_train, X_test, y_train, y_test = train_test_split( EjeX , EjeY , test_size=0.6, random_state=0) # dimensiones de los X-train
            
            mean_squared = [] # para guardar el error cuadratico
            mean_absolute = [] # para guardar el error absoluto
            plt.figure(i) # Sera una ventana por cada opción
            #print(np.shape(X_train))
            for j in range(len(modelos)):
                
                #plt.subplot(cantidadSeleccionados, cantidadModelos, indiceSubgrafica)  # Para marcar los subplots de las graficas
                plt.subplot(1, cantidadModelos, j+1) # El indice no puede ser 0
                indiceSubgrafica = indiceSubgrafica + 1
                if(j != 0):
                    #print(j)
                    X_train = np.reshape(X_train, (-1, 1))
                #if (j == 2):  # Problema de 1d array https://stackoverflow.com/questions/35812074/shortest-syntax-to-use-numpy-1d-array-as-sklearn-x
                 #   X_train = np.reshape(X_train, (1,-1))
                 #   X_train = list(itertools.chain(X_train))
                 #   X_train = X_train[:, None]
                 #   X_train = np.matrix(X_train).T.A
                X_test =  np.sort(X_test, kind = 'mergesort') # Ordeno de menor a mayor, antes de hacer el reshape por que sino no me deja ordenar con este metodo
                if(j != 0):    # if es de tipo isotonic no hago el reshape
                    X_test = np.reshape(X_test, (-1, 1))
                #if(j == 2):    # if es de tipo isotonic tengo que rehacer el reshape
                  #  X_test = list(itertools.chain(X_test))
                  #  X_test = X_test[:, None]
                  #  X_test = np.matrix(X_test).T.A

                model = modelos[j]()
                #print(np.shape(X_train))
                model.fit(X_train,y_train)
                regresion_y = model.predict(X_test)

                predict = model.predict(X_train)
                mean_squared.append(mean_squared_error(y_train, predict)) # La y_train tiene los datos originales para comprarlos con la predicción
                mean_absolute.append(mean_absolute_error(y_train, predict))

                
                plt.scatter(X_train,y_train)
                plt.plot(X_test, regresion_y,c = colores[i]) # repretar varias, cada una con su leyenda, con color <----------------
                plt.title(model.__class__.__name__)
                plt.xlabel(data.getSeleccionEjeX())
                plt.ylabel(data.getSeleccionEjeY())
                if(isinstance(Xlabels,list)): 
                    plt.xticks(EjeX,Xlabels)
                if(isinstance(Ylabels,list)):
                    plt.yticks(EjeY,Ylabels)
                

            #plt.figure() # Un ultima ventana para los errores
            graficas = ["Isotonic", "Linear", "Gradient"]
            #plt.subplot(cantidadSeleccionados, cantidadModelos, indiceSubgrafica)
            plt.subplot(1, cantidadModelos, len(modelos)+1)
            indiceSubgrafica = indiceSubgrafica + 1
            plt.bar(graficas,mean_squared, label="Error cuadratico" )
            plt.title("Error Cuadratico")

            #plt.subplot(cantidadSeleccionados, cantidadModelos, indiceSubgrafica)
            plt.subplot(1, cantidadModelos, len(modelos)+2)
            indiceSubgrafica = indiceSubgrafica + 1
            plt.bar(graficas, mean_absolute, label = "Error absoluto")
            plt.title("Error Absoluto")

            plt.suptitle(seleccionados[i])


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
        # En total quiero que haya 4 graficas que aporten informacion
        # Separar los datos
        # representar los datos del dataset con el metodo
        # Declarar el modelo
        # Entrenar el modelo
        # Representar los datos que usare para predecir, ya con los clusters
        # Representar los centros de cluster
        # Usar al metodo de medicion de clustering para otra grafica

        plt.clf() # Para limpiar las gracicas anteriores y que no se mezcle
        seleccionados = data.getSeleccionados() # Las opciones seleccionadas
        cantidadSeleccionados = len(seleccionados) # la cantidad de opciones seleccionadas
        dimensionx = 1 # La cantidad de filas para los subplots
        dimensiony = 2 # La cntidad de columnas para los subplots
        Clustering.dibujarDatosIniciales(data,dimensionx,dimensiony,1)
        ejex, ejey , colores = Clustering.combinacionDatos(data) # Combinar para que?, si despues es más dificil mostrar las etiquetas
        # cableado por que habra un numero fijo de subventanas
        #Clustering.dibujardatos(ejex, ejey,"Datos entrenamiento" +data.getTitle(), colores,2,2,1, data.getSeleccionEjeX(),data.getSeleccionEjeY()) 

        

        # metodo clustering
        EjeX,Xlabels = auxiliar.VerificarEje(ejex)
        EjeY,Ylabels = auxiliar.VerificarEje(ejey)
        puntos = list(zip(EjeX,EjeY))
        #model = modelo(n_clusters = cantidadSeleccionados).fit(puntos)# solo se puede hacer esto si es KMeans
        model = modelo().fit(puntos)
        # entrenarlo
        
        y_km = model.fit_predict(puntos)
        # representarlo
        plt.subplot(dimensionx,dimensiony,2)
        colores = ['red','green','yellow','cyan','indigo','maroon','teal','gold','orange','coral']
        for i in range(cantidadSeleccionados):
            # podria combertir la i en float y sumarle un 0,1 para la segunda
            primero = i+0,0
            segundo = i+0,1
            #plt.scatter(puntos[y_km == primero], puntos[y_km == segundo], color = colores[i])   # tengo que generar los float de otra manera| pueden ser slices
        plt.scatter(ejex, ejey, c = y_km) # Muestro los ejes originales ya los verificados es solo para entrenar el modelo
        plt.title("Clustering")
        plt.xlabel(data.getSeleccionEjeX())
        plt.ylabel(data.getSeleccionEjeY())
        #if(isinstance(Xlabels,list)): 
        #    plt.xticks(EjeX,Xlabels)
        #if(isinstance(Ylabels,list)):
        #    plt.yticks(EjeY,Ylabels)
        
        
        # Representar mediciones
        
        plt.suptitle(modelo.__name__)
        plt.tight_layout() # Para dar espacio a las subgraficas
        plt.legend(seleccionados)
        plt.show()


    # Metodo para combinar todos los datos de las opciones
    def combinacionDatos(data):
        ejex = []
        ejey = []
        colores = []
        seleccionados = data.getSeleccionados()
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



    # Metodo para dibujar los datos den entrenamiento y los de predecir, deberia usarlo con el de arriba
    def dibujardatos(ejex, ejey,titulo, colores, dimension1, dimension2, posicion, xlabel, ylabel):
        #ejex,ejey = zip(*datos)
        plt.subplot(dimension1, dimension2, posicion)
        plt.scatter(ejex,ejey, c = colores)
        plt.title(titulo)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    def dibujarDatosIniciales(data,dimension1,dimension2, posicion):
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
        plt.title("Datos Pre Clustering" +data.getTitle())
        plt.xlabel(data.getSeleccionEjeX())
        plt.ylabel(data.getSeleccionEjeY())
        #plt.show() # Si hago un show aqui ya no muestra más

class AllClustering:

    def show(data):

        plt.clf() # Para limpiar las gracicas anteriores y que no se mezcle
        seleccionados = data.getSeleccionados() # Las opciones seleccionadas
        cantidadSeleccionados = len(seleccionados) # la cantidad de opciones seleccionadas

        ejex, ejey , colores = Clustering.combinacionDatos(data)
        EjeX,Xlabels = auxiliar.VerificarEje(ejex)
        EjeY,Ylabels = auxiliar.VerificarEje(ejey)
        puntos = list(zip(EjeX,EjeY))
        
        modelos = [KMeans,GaussianMixture, DBSCAN]  # Los distintos tipos de clustering
        i = 1
        for modelo in modelos:
            if(i == 1):
                model = modelo(n_clusters = cantidadSeleccionados).fit(puntos)
            if(i == 2):
                model = modelo(n_components = cantidadSeleccionados)
            if(i == 3):
                model = modelo()
            y_km = model.fit_predict(puntos)
            Clustering.dibujardatos(ejex,ejey,model.__class__.__name__,y_km,1,3,i,data.getSeleccionEjeX(),data.getSeleccionEjeY())
            i += 1

        plt.tight_layout() # Para dar espacio a las subgraficas
        #if(isinstance(Xlabels,list)): 
        #    plt.xticks(EjeX,Xlabels)
        #if(isinstance(Ylabels,list)):
        #    plt.yticks(EjeY,Ylabels)
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