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

        # Cambio el porcentaje de entrenamiento y testeo
        porcentajes = np.arange(0.4, 0.9, 0.05)
        for porcentaje in porcentajes:    # Bucle para hacer la gráfica

            # El primero seran los datos el segundo las etiquetas
            X_train, X_test, y_train, y_test = train_test_split(matriz, tipos, test_size=porcentaje , random_state=0)
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



class Gausian:

    def show(data):
        Representacion.show(data,GaussianNB)



class Kneighbors:

    def show(data):
        Representacion.show(data,KNeighborsClassifier)



class Tree:

    def show(data):
        Representacion.show(data,DecisionTreeClassifier)