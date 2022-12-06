import pandas as pd


#PREPROCESAMIENTO bodegas

df = pd.read_csv("bodegas_coordenadas.csv",sep=',')
columnas = ["Número de Inscripción", "Apartamento", "Spot", "KM", "Telefono 3", "Sitio web 2", 
            "Sitio web 3", "Latitud", "Longitud", "Habitaciones", "Plazas", "Categoría", 
            "Dirección de imagen", "Facebook Link", "Twitter Link", "Google Mas Link", "Descripción"]

#df.drop(columns,axis='columns')
df = df.drop(columnas,axis=1)

coordenadas = df["Coordenadas"]
latitudes = []
longitudes = []
for cor in coordenadas:
    coords = cor.split(", ")
    latitudes.append(float(coords[0]))
    longitudes.append(float(coords[1]))

df = df.drop(["Coordenadas"],axis=1)
df = df.assign(Latitud=latitudes)
df = df.assign(Longitud=longitudes)

df.to_csv("bodegas_preprocesadas.csv",index_label="Id")

print("Preprocesamiento de Bodegas realizado correctamente \n")

#PREPROCESAMIENTO lineas omnibus

df_omnibus = pd.read_csv("lineas_omnibus.csv",sep=';')
df_terminales = pd.read_csv("terminales_deptos.csv",sep=',')

# df_omnibus = df_omnibus.assign(Terminal="")
# df_omnibus = df_omnibus.assign(Latitud_Dest="")
# df_omnibus = df_omnibus.assign(Longitud_Dest="")

# ciudades_terminales = df_terminales["Ciudad"]
# nombres_terminales = df_terminales["Nombre"]
# coordenadas = df_terminales["Coordenadas"]
# latitudes = []
# longitudes = []

# for cor in coordenadas:
#     coords = cor.split(", ")
#     latitudes.append(float(coords[0]))
#     longitudes.append(float(coords[1]))

length = len(df_omnibus)
indices_borrar = []

for i in range(length):
    destino = df_omnibus.iloc[i,3] 
    indice = df_terminales.index[df_terminales["Ciudad"] == destino].tolist()
    # if indice != []:
    #     df_omnibus.iloc[i,15] = nombres_terminales[indice[0]]
    #     df_omnibus.iloc[i,16] = latitudes[indice[0]]
    #     df_omnibus.iloc[i,17] = longitudes[indice[0]]
    # else:
    #     indices_borrar.append(i)
    if indice == []:
        indices_borrar.append(i)

df_omnibus = df_omnibus.drop(indices_borrar,axis=0)
df_omnibus.to_csv("lineas_omnibus_preprocesadas.csv",index_label="Id")

print("Preprocesamiento de Omnibus realizado correctamente")


coordenadas = df_terminales["Coordenadas"]
latitudes = []
longitudes = []
for cor in coordenadas:
    coords = cor.split(", ")
    latitudes.append(float(coords[0]))
    longitudes.append(float(coords[1]))

df_terminales = df_terminales.drop(["Coordenadas"],axis=1)
df_terminales = df_terminales.assign(Latitud=latitudes)
df_terminales = df_terminales.assign(Longitud=longitudes)

df_terminales.to_csv("terminales_preprocesadas.csv",index_label="Id")

print("Preprocesamiento de Terminales realizado correctamente \n")