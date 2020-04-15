from leerDatos import ParseCasosConfirmados
import seaborn as sns
from clases_base import Grafica

#To DO: hacer la clase de linea_sea, hacer funcionar la grafica de tipo linea

#df = sns.load_dataset("casos_2019")
l = Lector('data/casos_2019.csv')

# no pilla los datos de como los tengo generados, mirar que tipo de dataframe necesita
sns.relplot(x='dias',y='casos Confirmados',data=l.getdf())
