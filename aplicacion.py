import psycopg2
import geopy.distance
import pandas as pd

# coords_1 = (-34.78674379818736,-55.41825873144979) 
# coords_2 = (-34.34318652402254,-55.76535772399475)
# print(round(geopy.distance.geodesic(coords_1, coords_2).km,2))

print("\033[1;34;40mBIENVENIDO AL SISTEMA DE CONSULTAS DE BODEGAS \033[0;0m \n")

salir = False
while(not salir):
    print("\nIngrese el número de la consulta que desee realizar: \n")
    print("  \033[1;31;40m1-\033[0;0m Obtener lineas de omnibus para una bodega y origen (departamento) dado \n")
    print("  \033[1;31;40m2-\033[0;0m Obtener excursiones disponibles para una bodega dada \n")
    nro_consulta = int(input())

    try:
        conn = psycopg2.connect(
            host="localhost",
            database="tareafinal",
            user="postgres",
            password="tareaidatos")

        cur = conn.cursor()

        if nro_consulta == 1:

            cur.execute("""SELECT id, nombre_fantasia
                        FROM bodegas""")
            listado_bodegas = cur.fetchall()
            print("\033[1;35;40mIngrese el número de la bodega que desea consultar: \033[0;0m \n")
            for row in listado_bodegas:
                print(" " + str(row[0]) + "- " + row[1])
            id_bodega = int(input())

            print("\033[1;35;40mIngrese el nombre del departamento donde se encuentre: \033[0;0m \n")
            nombre_depto = input().upper()
            
            cur.execute("""SELECT lo.empresa, lo.depto_origen, lo.depto_destino, lo.lugar, lo.h_salida, lo.h_llegada, t.nombre
                        FROM lineas_omnibus AS lo
                        JOIN bodegas_omnibus AS bo ON lo.id = bo.id_omnibus
                        JOIN bodegas AS b ON b.id = bo.id_bodega AND b.id = %s
                        JOIN omnibus_terminales AS ot ON ot.id_omnibus = lo.id
                        JOIN terminales AS t ON t.id = ot.id_terminal
                        WHERE lo.depto_origen = %s """,(id_bodega,nombre_depto))
            
            result = cur.fetchall()
            if result != []:
                ini = 0
                fin = 20
                df = pd.DataFrame(result,columns = ["Empresa transporte", "Depto. Origen", "Depto. Destino", "Parada Intermedia", "Hora Salida", "Hora Llegada", "Terminal Destino"])
                largo = len(df)
                ver_mas = False
                if largo < 20:
                    print(df.to_markdown())
                else:
                    while(fin <= largo):
                        print(df.iloc[ini:fin].to_markdown())
                        print("\n Desea ver mas? (s/n)")
                        resp = input()
                        if resp == "s":
                            ini = fin
                            fin = fin + 20
                            if fin > largo:
                                print(df.iloc[ini:largo - 1].to_markdown())
                                print("\nNo existen mas resultados")
                                break;
                        else:
                            break;
            else:
                print("\nLo sentimos, no hay lineas de omnibus disponibles para su consulta")
        
        elif nro_consulta == 2:
            cur.execute("""SELECT id, nombre_fantasia
                        FROM bodegas""")
            listado_bodegas = cur.fetchall()
            print("\033[1;35;40mIngrese el número de la bodega que desea consultar: \033[0;0m \n")
            for row in listado_bodegas:
                print(" " + str(row[0]) + "- " + row[1])
            id_bodega = int(input())

            cur.execute("""SELECT ex.nombre, ex.hora_salida, ex.duracion, ex.hora_fin,
                           ex.actividades, ter.nombre, ter.ciudad, ter.departamento
                           FROM excursiones AS ex JOIN terminales AS ter ON ex.id_terminal = ter.id
                           WHERE ex.id_bodega = %s """,(id_bodega,))
            result = cur.fetchall()
            if result != []:
                df = pd.DataFrame(result,columns = ["Nombre", "H.Salida", "Duracion", "H.Llegada", "Actividades","Terminal Partida", "Ciudad", "Depto."])
                print(df.to_markdown())
            else:
                print("Lo sentimos, no hay excursiones disponibles para la bodega seleccionada")

        else:
            print("\033[1;31;40mPor favor ingrese uno de los número indicados\033[0;0m \n")
        
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
        
    print("Desea salir? (s/n)")
    resp = input()
    if(resp == "s"):
        print("\n Gracias por utilizar nuestro servicio!")
        salir = True
