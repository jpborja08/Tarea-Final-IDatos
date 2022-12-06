import pandas as pd


df = pd.read_csv("lineas_omnibus.csv",sep=';')

deptos_uruguay = ['ARTIGAS', 'CANELONES', 'CERRO LARGO', 'COLONIA', 'DURAZNO', 'FLORES', 'FLORIDA',
                 'LAVALLEJA', 'MALDONADO', 'MONTEVIDEO', 'PAYSANDU', 'RIO NEGRO', 'RIVERA', 'ROCHA', 
                 'SALTO', 'SAN JOSE', 'SORIANO', 'TACUAREMBO', 'TREINTA Y TRES']

deptos_origen_csv = df["Depto.Origen"].unique()
deptos_destino_csv = df["Depto.Destino"].unique()

# chequeo que todos los deptos. esten en el esquema de omnibus, como depto. origen y depto. destino
deptos_origen_faltantes = []
deptos_destino_faltantes = []

for depto in deptos_uruguay:
    if not (depto in deptos_origen_csv):
        deptos_origen_faltantes.append(depto)
    
    if not (depto in deptos_destino_csv):
        deptos_destino_faltantes.append(depto)
if deptos_origen_faltantes == [] and deptos_destino_faltantes == []:
    print("Estan todos los departamentos")



