import pandas as pd
import psycopg2
import geopy.distance


def omnibus_terminales():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="tareafinal",
            user="postgres",
            password="tareaidatos")

        cur = conn.cursor()
        cur.execute("""INSERT INTO omnibus_terminales (id_omnibus,id_terminal) 
                            SELECT lo.id as id_omnibus, t.id as id_terminal 
                            FROM lineas_omnibus as lo 
                            JOIN terminales as t ON lo.destino = t.ciudad;""")
        # display the PostgreSQL database server version
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

omnibus_terminales()


def bodegas_omnibus():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="tareafinal",
            user="postgres",
            password="tareaidatos")

        cur = conn.cursor()
        cur.execute(""" SELECT id,latitud,longitud
                        FROM bodegas""")
        coordenadas_bodegas = cur.fetchall()
        
        cur.execute(""" SELECT id,latitud,longitud
                        FROM terminales""")
        coordenadas_terminales = cur.fetchall()

        ids_bodegas_terminales = []

        for row_b in coordenadas_bodegas:
            coords_1 = (row_b[1], row_b[2])
            ids_terminales = []
            for row_t in coordenadas_terminales:
                coords_2 = (row_t[1], row_t[2])
                dist = round(geopy.distance.geodesic(coords_1, coords_2).km,2)
                if dist <= 50:
                    ids_terminales.append(row_t[0])

            ids_bodegas_terminales.append((row_b[0],ids_terminales))

        tuplas_bodegas_terminales = []
        for row in ids_bodegas_terminales:
            for t in row[1]:
                tuplas_bodegas_terminales.append((row[0],t)) # (id_bodega, id_terminal)

        cur.execute(""" SELECT id_omnibus,id_terminal
                        FROM omnibus_terminales""")
        omnibus_terminales = cur.fetchall()
        
        bodegas_omnibus = []

        for bod_ter in tuplas_bodegas_terminales:
            id_ter = bod_ter[1]
            for omb_ter in omnibus_terminales:
                if id_ter == omb_ter[1]:
                    bodegas_omnibus.append((bod_ter[0],omb_ter[0])) #(id_bodega,id_omnibus)
        
        #insertamos los datos de la tabla bodegas_omnibus
        args_str = ','.join(cur.mogrify("(%s,%s)", x).decode('utf-8') for x in bodegas_omnibus)
        
        cur.execute("INSERT INTO bodegas_omnibus (id_bodega,id_omnibus) VALUES " + args_str)
        conn.commit()

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


bodegas_omnibus()








# for row in mobile_records:
#             print("Id = ", row[0], )
#             print("Model = ", row[1])
#             print("Price  = ", row[2])