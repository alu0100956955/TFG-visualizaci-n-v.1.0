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
import math


# Como por ahora las tres clases representan de la misma forma por ahora empleo esta clase para representar pasandole el algoritmo
class Representacion:

    def show(data, algoritmo_):

        algoritmo = algoritmo_()
        training_accuracy = []
        test_accuracy = []

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
        plt.subplot(221)

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
    
        plt.subplot(222)
        # CODIGO DUPLICADO, podria hacer esto en un bucle y que lo otro fuese un metodo para añadir nuevos datos al scatter TODO
        plt.scatter(ejex,ejey, c=colores)
        plt.title(data.getTitle() + " + Datos de Testeo")
        plt.ylabel(data.getSeleccionEjeY())
        plt.xlabel(data.getSeleccionEjeX())
        #plt.show() # Solo un show ya que es como un exit()


        plt.subplot(223)
        plt.plot(porcentajes, training_accuracy, label="training accuracy")
        plt.plot(porcentajes, test_accuracy, label="test accuracy")
        plt.ylabel("Accuracy")
        plt.xlabel("Porcentaje de conjunto de pruebas")
        plt.legend()

        #plt.show()    
    
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
            aux = list(zip(data.getEje(data.getSeleccionEjeX(),selec),data.getEje(data.getSeleccionEjeY(),selec) ))
            for i in range(len(aux)):
                etiquetas.append(selec)
            datos += aux 
        return datos, etiquetas






class Gausian:

    def show(data):
        Representacion.show(data,GaussianNB)



class Kneighbors:

    def show(data):
        Representacion.show(data,KNeighborsClassifier)



class Tree:

    def show(data):
        Representacion.show(data,DecisionTreeClassifier)



class Regresion:
    # https://matplotlib.org/3.1.0/gallery/color/named_colors.html Lista de colores de matplotlib
    def show(data, modelo,reshape): # Arreglar el parametro extra
        # Si pasan varias opciones se podria hacer un bucle que habra varias veces estas graficas
        # Tambien podria representar solo la grafica final, siendo un color para los datos de entrenamiento otro para los datos de testeo y la linea

        seleccionados = data.getSeleccionados() # Las opciones seleccionadas
        cantidadSeleccionados = len(seleccionados) # la cantidad de opciones seleccionadas
        dim = Regresion.dimensiones(cantidadSeleccionados) # con la cantidad de seleccionados genero las dimensiones para el subplot

        for i in range(cantidadSeleccionados):
            # TODO: Tendria que controlar si se pasa un eje no numerico
            X_train, X_test, y_train, y_test = train_test_split(data.getEje(data.getSeleccionEjeX(),seleccionados[i]), data.getEje(data.getSeleccionEjeY(),seleccionados[i]), test_size=0.6, random_state=0)
            

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
            plt.plot(X_test, regresion_y,c = 'red')
            plt.title(seleccionados[i])


        plt.show()

        # Metodo para calcular la dimension de los subplot
    def dimensiones(cantidad):
        # devuelvo la raiz redondeada hacia arriba de 
        return math.ceil(math.sqrt(cantidad))

        


class Linear:

    def show(data):
        Regresion.show(data,LinearRegression,True)


class Gradient: # falta incluirlo en las referencias y los import

    def show(data):
        Regresion.show(data,GradientBoostingRegressor,True)  # Habria que añadir parametros extra

class Isotonic:

    def show(data):
        Regresion.show(data,IsotonicRegression,False)





class Clustering:

    def show(data, modelo):
        print("sin terminar")
        # Separar los datos
        # representar los datos del dataset con el metodo
        # Declarar el modelo
        # Entrenar el modelo
        # Representar los datos que usare para predecir, ya con los clusters
        # Representar los centros de cluster

    # Metodo para dibujar los datos den entrenamiento y los de predecir, deberia usarlo con el de arriba
    def dibujardatos(datos,titulo):
        ejex,ejey = zip(*datos)
        plt.scatter(ejex,ejey)
        plt.title(titulo)
    



class Kmeans:

    def show(data):
        Clustering.show(data,Kmeans)

class Mixture:

    def show(data):
        Clustering.show(data,GaussianMixture)


class DBscan:

    def show(data):
        Clustering.show(data,DBSCAN)