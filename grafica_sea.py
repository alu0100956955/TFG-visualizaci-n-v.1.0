from leerDatos import Lector
import seaborn as sns

#df = sns.load_dataset("casos_2019")
l = Lector('data/casos_2019.csv')

# no pilla los datos de como los tengo generados, mirar que tipo de dataframe necesita
sns.relplot(x='dias',y='casos Confirmados',data=l.getdf())
