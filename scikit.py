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

        plt.plot(porcentajes, training_accuracy, label="training accuracy")
        plt.plot(porcentajes, test_accuracy, label="test accuracy")
        plt.ylabel("Accuracy")
        plt.xlabel("Porcentaje de conjunto de pruebas")
        plt.legend()

        plt.show()    
    
        
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