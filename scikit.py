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


# Para mostrar la matriz de confusion con matplolib
# https://stackoverflow.com/questions/19233771/sklearn-plot-confusion-matrix-with-labels

# Como por ahora las tres clases representan de la misma forma por ahora empleo esta clase para representar pasandole el algoritmo
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
        datos, etiquetas = Representacion.DatosEtiquetas(data)


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
        plt.title(data.getTitle() + " + Datos de Testeo")
        plt.ylabel(data.getSeleccionEjeY())
        plt.xlabel(data.getSeleccionEjeX())
        #plt.show() # Solo un show ya que es como un exit()


        plt.subplot(323)
        plt.plot(porcentajes, training_accuracy, label="training accuracy")
        plt.plot(porcentajes, test_accuracy, label="test accuracy")
        plt.ylabel("Accuracy")
        plt.xlabel("Porcentaje de conjunto de pruebas")
        plt.legend()


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


        #plt.subplot(325)
        #plt.plot(porcentajes, mean_squared, label="Error cuadratico")
        #plt.plot(porcentajes, mean_absolute, label="Error absoluto")
        #plt.ylabel("Accuracy")
        #plt.xlabel("Porcentaje de conjunto de pruebas")
        #plt.legend()



        #plt.subplot(224)  # No lo muestra como me gustaria puede deberse a como creo la matriz de confusión
        disp = metrics.plot_confusion_matrix(algoritmo, X_test, y_test, normalize = 'true')
        disp.figure_.suptitle("Confusion Matrix")
        print("Confusion matrix:\n%s" % disp.confusion_matrix)
        
        plt.suptitle(algoritmo_.__name__) # para mostrar el modelo que se esta representando
        plt.show()

        # Devuelve los datos y las etiquetas necesarias para que tire el sistema
    def DatosEtiquetas(data):
        datos = []
        etiquetas = []

        # Buble que por cada escogido se mezclaran los datos y añadiremos a datos, junto a su etiqueta en etiquetas
        seleccionados = data.getSeleccionados()
        for selec in seleccionados:
            aux = list(zip(data.getEje(data.getSeleccionEjeX(),selec),data.getEje(data.getSeleccionEjeY(),selec) ))
            for i in range(len(aux)):
                etiquetas.append(selec)
            datos += aux 
        return datos, etiquetas

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
            ejex, ejey = Regresion.combinacionDatos(data)
            colores = ['red','green','yellow','cyan','indigo','maroon','teal','gold','orange','coral']

            # Para los datos combinare los datos de los dos ejes empleando zip
            datos, etiquetas = Representacion.DatosEtiquetas(data)
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
                plt.scatter(ejex, ejey , c = colores)
                plt.title("Datos clasificados")

                contador = contador + 1

                

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
            X_train, X_test, y_train, y_test = train_test_split(data.getEje(data.getSeleccionEjeX(),seleccionados[i]), data.getEje(data.getSeleccionEjeY(),seleccionados[i]), test_size=0.6, random_state=0)
            
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

            predict = model.predict(X_train)
            mean_squared.append(mean_squared_error(y_train, predict)) # La y_train tiene los datos originales para comprarlos con la predicción
            mean_absolute.append(mean_absolute_error(y_train, predict))


        # hago una subgrafica con los errores absoluto y cuadratico
        errores = ["Cuadratic","Absolute"]

        plt.subplot(dim, dim, cantidadSeleccionados+1)
        plt.bar(seleccionados,mean_squared, label="Error cuadratico" )
        plt.title("Errorr Cuadratico")

        plt.subplot(dim, dim, dim+dim)
        plt.bar(seleccionados, mean_absolute, label = "Error absoluto")
        plt.title("Errorr Absoluto")

        plt.suptitle(modelo.__name__)

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
                ejex = data.getEje(data.getSeleccionEjeX(),seleccionados[i])
                ejey = data.getEje(data.getSeleccionEjeY(),seleccionados[i])
            ejex += data.getEje(data.getSeleccionEjeX(),seleccionados[i])
            ejey += data.getEje(data.getSeleccionEjeY(),seleccionados[i])
            
        return ejex, ejey

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
        cantidadSeleccionados = len(seleccionados)
        indiceSubgrafica = 1
        for i in range(len(seleccionados)):
            ejex = data.getEje(data.getSeleccionEjeX(),seleccionados[i])
            ejey = data.getEje(data.getSeleccionEjeY(),seleccionados[i])

            X_train, X_test, y_train, y_test = train_test_split( ejex , ejey , test_size=0.6, random_state=0) # dimensiones de los X-train
            
            #print(np.shape(X_train))
            for j in range(len(modelos)):
                # TODO: Tendria que controlar si se pasa un eje no numerico
                plt.subplot(cantidadSeleccionados, len(modelos), indiceSubgrafica)  # Para marcar los subplots de las graficas
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

                
                plt.scatter(X_train,y_train)
                plt.plot(X_test, regresion_y,c = colores[i]) # repretar varias, cada una con su leyenda, con color <----------------
                plt.title(model)


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
        #print("sin terminar") 
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

        ejex, ejey , colores = Clustering.combinacionDatos(data)
        Clustering.dibujardatos(ejex, ejey,"Datos entrenamiento" +data.getTitle(), colores,2,2,1) # cableado por que habra un numero fijo de subventanas

        

        # metodo clustering
        puntos = list(zip(ejex,ejey))
        model = modelo(n_clusters = cantidadSeleccionados).fit(puntos)
        # entrenarlo
        
        y_km = model.fit_predict(puntos)
        # representarlo
        plt.subplot(2,2,2)
        colores = ['red','green','yellow','cyan','indigo','maroon','teal','gold','orange','coral']
        for i in range(cantidadSeleccionados):
            # podria combertir la i en float y sumarle un 0,1 para la segunda
            primero = i+0,0
            segundo = i+0,1
            #plt.scatter(puntos[y_km == primero], puntos[y_km == segundo], color = colores[i])   # tengo que generar los float de otra manera| pueden ser slices
        plt.scatter(ejex, ejey, c = y_km)
        plt.title("Clustering")
        # Representar mediciones
        
        plt.suptitle(modelo.__name__)
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
    def dibujardatos(ejex, ejey,titulo, colores, dimension1, dimension2, posicion):
        #ejex,ejey = zip(*datos)
        plt.subplot(dimension1, dimension2, posicion)
        plt.scatter(ejex,ejey, c = colores)
        plt.title(titulo)
    

class AllClustering:

    def show(data):

        plt.clf() # Para limpiar las gracicas anteriores y que no se mezcle
        seleccionados = data.getSeleccionados() # Las opciones seleccionadas
        cantidadSeleccionados = len(seleccionados) # la cantidad de opciones seleccionadas

        ejex, ejey , colores = Clustering.combinacionDatos(data)

        puntos = list(zip(ejex,ejey))
        
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
            Clustering.dibujardatos(ejex,ejey,modelo,y_km,1,3,i)
            i += 1

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