# Librerias
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier


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