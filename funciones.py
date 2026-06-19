import csv
import os
import unicodedata
import questionary

def escribir_csv(paises):
    campos=["nombre","poblacion","superficie","continente"]
    with open("paises.csv","w",newline="",encoding="utf-8-sig") as archivo:
        writer=csv.DictWriter(archivo,fieldnames=campos)
        writer.writeheader()
        writer.writerows(paises)

paises=[
    {"nombre":"Argentina","poblacion":45376763,"superficie":2780400,"continente":"América"},  
{"nombre":"Japón","poblacion":125800000,"superficie":377975,"continente":"Asia" }, 
{"nombre":"Brasil","poblacion":213993437,"superficie":8515767,"continente":"América" }, 
{"nombre":"Alemania","poblacion":83149300,"superficie":357022,"continente":"Europa"}  
]
def menu():
    opcion= questionary.select(
        message="Selecciona: ",
        choices=["1. Agregar país",
"2. Actualizar población y superficie",
"3. Buscar país",
"4. Filtrar país",
"5. Ordenar países",
"6. Mostrar estadísticas",
"7. Salir"]
    ).ask()
    return opcion

def filtrar_menu():
    opcion= questionary.select(
        message="Selecciona: ",
        choices= ["1. Continente",
"2. Rango de población",
"3. Rango de superficie",
"4. Salir"]
).ask()
    return opcion
def ordenar_menu():
    opcion= questionary.select(
        message="Selecciona: ",
        choices= ["1. Nombre",
"2. Población",
"3. Superficie",
"4. Salir"]
).ask()
    return opcion
def estadistica_menu():
    opcion= questionary.select(
        message="Selecciona: ",
        choices= ["1. País con mayor y menor población",
"2. Promedio de población",
"3. Promedio de superficie",
"4. Cantidad de países por continente",
"5. Salir"]
).ask()
    return opcion
#Menú de continentes y por medio de un diccionario busco la clave y obtengo el contienete como un string
def menu_continentes():
    opcion= questionary.select(
        message="Selecciona el continente: ",
        choices=["1. África",
"2. América",
"3. Asia",
"4. Europa",
"5. Oceanía"]
    ).ask()
    continentes = {
    "1. África": "África",
    "2. América": "América",
    "3. Asia": "Asia",
    "4. Europa": "Europa",
    "5. Oceanía": "Oceanía"}
    continente=continentes[opcion]
    return continente

#Limpiar la consola
def limpiar_consola():
    os.system("cls")

#La funcion normalizar recibe un texto y lo tranforma para poder trabajar
def normalizar(texto):
    #''.join vulve a unir los caracteres sin dejar espacios para formar el texto después de analizarlo
    return ''.join(
        #En esta parte separa el texto en caracteres y tambien separa las tildes
        c for c in unicodedata.normalize('NFD', texto)
        #Acá se analiza cada tipo de caracter y si es una tilde no lo guarda
        if unicodedata.category(c) != 'Mn'
    ).lower() #convierto todo a minúscula
#verifico que sea un número y que no sea negativo
def verificar_numero(mensaje):
    while True:
        try:
            num=int(input(mensaje))
            if num<0:
                raise ValueError("El valor ingresado no puede ser negativo")
            return num
        except ValueError as e:
            #utilice este if porque quiero un mensaje personalizado para los distintos ValueError y no el que sale por defecto
            if "invalid literal" in str(e):
                print("El valor ingresado es incorrecto")
            else:
                print(f"Error: {e}")

def verificar_texto(mensaje):
    while True:
        try:
            texto=input(mensaje).capitalize().strip()
            if texto=="":
                raise ValueError("El campo no puede quedar vacío")
            return texto
        except ValueError as e:
            print(f"Error: {e}")
#función para agregar paises abro en archivo en modo "a" para agregar al final el nuevo pais en paises.csv     
def agregar_pais():
    with open("paises.csv","a",newline="",encoding="utf-8-sig") as archivo:
        nombre=verificar_texto("Ingrese el nombre del país: ")
        poblacion=verificar_numero("Ingrese el valor de la población: ")
        superficie=verificar_numero("Ingrese el valor de la superficie: ")
        continente=menu_continentes()
        archivo.write(f"{nombre},{poblacion},{superficie},{continente}\n")
        print("País agregado con éxito\n")

def actualizar():
    opcion= questionary.select(
        message="Selecciona: ",
        choices=["1. Actualizar población",
"2. Actualizar superficie"]
    ).ask()
    #abro el archivo en modo lectura "r" guardo los campos y los paises que contiene el archivo en una lista
    pais_buscado=verificar_texto("Ingrese el país que desea actualizar: ")
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        lector=csv.DictReader(archivo)
        campos=lector.fieldnames
        filas=[]
        encontrado=False
        match (opcion):
            case "1. Actualizar población":
                for linea in lector:
                    #busco si el pais buscado exite en el archivo y si es asi le paso el nuevo valor
                    #de la población y lo guardo en la lista filas
                    if normalizar(pais_buscado)==normalizar(linea["nombre"]):
                        poblacion_nueva=verificar_numero("Ingrese el valor de la poblacion: ")
                        linea["poblacion"]=poblacion_nueva
                        encontrado=True
                    filas.append(linea)
                if encontrado:
                    #como se encontro el pais y se modificó, vuelvo a abrir el archivo csv en modo escritura
                    #para pasarle la modificacion pero como estoy reescribiendo le paso todas las filas con
                    #la lista filas y los fielnames guardados en la varible campos y me queda el archivo con todos
                    #los paises que existían junto con el país modificado
                    with open("paises.csv","w",newline="",encoding="utf-8-sig") as archivo:
                        escritor=csv.DictWriter(archivo,fieldnames=campos)
                        escritor.writeheader()
                        escritor.writerows(filas)
                        print("Pais actualizado con éxito\n")
                else:
                    raise ValueError("El país ingresado no se encuentra en el registro\n")
            case "2. Actualizar superficie":
                for linea in lector:
                    if normalizar(pais_buscado)==normalizar(linea["nombre"]):
                        superficie_nueva=verificar_numero("Ingrese el valor de la superficie: ")
                        linea["superficie"]=superficie_nueva
                        encontrado=True
                    filas.append(linea)
                if encontrado:
                    with open("paises.csv","w",newline="",encoding="utf-8-sig") as archivo:
                        escritor=csv.DictWriter(archivo,fieldnames=campos)
                        escritor.writeheader()
                        escritor.writerows(filas)
                        print("Pais actualizado con éxito\n")
                else:
                    raise ValueError("El país ingresado no se encuentra en el registro\n")


def buscar_pais():
    pais_buscado=verificar_texto("Ingrese el país que desea buscar: ")
    
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        #Cada fila la representa como un diccionario
        lector=csv.DictReader(archivo)
        encontrado=False
        for fila in lector:
            # Starswith verifica si el pais empieza por los caracteres ingresados y tambien tomo la palabra completa
            if (normalizar(fila["nombre"])).startswith(normalizar(pais_buscado)):
                print(f"\nPais: {fila["nombre"]}")
                print(f"Población: {fila["poblacion"]}")
                print(f"Superficie: {fila["superficie"]} km²")
                print(f"Contienente: {fila["continente"]}\n")
                print("-"*30)
                encontrado=True
        if not encontrado:
            raise ValueError("El país ingresado no existe en el registro")   
def filtrar_pais_continente():
    #llamo a la función que muesta el menu de los continentes y me devuelve el continente seleccionado
    continente_elegido = menu_continentes()
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        #interpreta cada fila del CSV como un diccionario
        # utilizando los nombres de las columnas como claves
        lector=csv.DictReader(archivo)
        encontrado=False
        for fila in lector:
            if fila["continente"]==continente_elegido:
                print(f"\nPaís: {fila['nombre']}")
                print(f"Población: {fila['poblacion']}")
                print(f"Superficie: {fila['superficie']} km²\n")
                print("-" * 30)
                encontrado=True
        if not encontrado:
            raise ValueError("No hay países registrados en ese continente")
            

def filtrar_por_población():
    #Llamo a la función verificar número y me devuelve un número
    poblacion_menor=verificar_numero("Ingrese el rango inferior: ")
    poblacion_sup=verificar_numero("Ingrese el rango superior: ")
    #verifico que los rangos sean correctos, osea que el rango menor no sea mayo que el rango superior
    if poblacion_menor>poblacion_sup:
        raise ValueError("El rango inferior no puede ser mayor al rango superior")
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        lector=csv.DictReader(archivo)
        encontrado=False
        for fila in lector:
            #busco las poblaciones que esten entre los rangos solicitados e imprimo sus datos
            if poblacion_menor<int(fila["poblacion"])<poblacion_sup:
                print(f"\nPais: {fila["nombre"]}")
                print(f"Población: {fila["poblacion"]}")
                print(f"Superficie: {fila["superficie"]} km²")
                print(f"Contienente: {fila["continente"]}\n")
                print("-"*30)
                encontrado=True
        if not encontrado:
            raise ValueError("No se encuentraron países en el rango de población ingresado")

def filtrar_por_superficie():
    superficie_menor=verificar_numero("Ingrese el rango inferior: ")
    superficie_sup=verificar_numero("Ingrese el rango superior: ")
    #verifico que los rangos estén bien. que el rango inferior no sea mayor al rango superior
    if superficie_menor>superficie_sup:
        raise ValueError("El rango inferior no puede ser mayor al rango superior")
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        lector=csv.DictReader(archivo)
        encontrado=False
        for fila in lector:
            #busco las superficies que esten entre los rangos solicitados
            if superficie_menor<int(fila["superficie"])<superficie_sup:
                print(f"\nPais: {fila["nombre"]}")
                print(f"Población: {fila["poblacion"]}")
                print(f"Superficie: {fila["superficie"]} km²")
                print(f"Contienente: {fila["continente"]}\n")
                print("-"*30)
                encontrado=True
        if not encontrado:
            raise ValueError("No se encuentraron países en el rango de superficie ingresado")

def ordenar_por_pais():
    opcion= questionary.select(
        message="Selecciona: ",
        choices=["1. Ordenar nombres de paises de A -> Z",
"2. Ordenar nombres de paises de Z -> A"]
    ).ask()
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        #convierte el csv en un diccionario utilizando las columnas como claves
        lector=csv.DictReader(archivo)
        #convierte al lector en una lista para posteriormente ordenar los paises
        paises=list(lector)
        match opcion:
            case "1. Ordenar nombres de paises de A -> Z":
                #ordena la lista de manera ascendente comparando los nombres
                paises_ordenados = sorted(paises, key=lambda pais: normalizar(pais["nombre"]))
                for pais in paises_ordenados:
                    print(f"\nPais: {pais["nombre"]}")
                    print(f"Población: {pais["poblacion"]}")
                    print(f"Superficie: {pais["superficie"]} km²")
                    print(f"Contienente: {pais["continente"]}\n")
                    print("-"*30)
            case "2. Ordenar nombres de paises de Z -> A":
                #reverse=True invierte el orden para poder obtener un orden de Z->A
                paises_ordenados = sorted(paises, key=lambda pais: normalizar(pais["nombre"]),reverse=True)
                for pais in paises_ordenados:
                    print(f"\nPais: {pais["nombre"]}")
                    print(f"Población: {pais["poblacion"]}")
                    print(f"Superficie: {pais["superficie"]} km²")
                    print(f"Contienente: {pais["continente"]}\n")
                    print("-"*30)
#Hago lo mismo que en la función ordenar_por_pais() nada mas que tranformo el dato a un
#int porque cuando me devuelve los valores directos del archivo csv me los trae como string
def ordenar_por_poblacion():
    opcion= questionary.select(
        message="Selecciona: ",
        choices=["1. Ordenar de manera ascendente",
"2. Ordenar de manera descendente"]
    ).ask()
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        lector=csv.DictReader(archivo)
        paises=list(lector)
        match opcion:
            case "1. Ordenar de manera ascendente":
                paises_ordenados = sorted(paises, key=lambda pais: int(pais["poblacion"]))
                for pais in paises_ordenados:
                    print(f"\nPais: {pais["nombre"]}")
                    print(f"Población: {pais["poblacion"]}\n")
                    print("-"*30)
            case "2. Ordenar de manera descendente":
                paises_ordenados = sorted(paises, key=lambda pais: int(pais["poblacion"]),reverse=True)
                for pais in paises_ordenados:
                    print(f"\nPais: {pais["nombre"]}")
                    print(f"Población: {pais["poblacion"]}\n")
                    print("-"*30)
            case _:
                print("La opción ingresada es incorrecta")

def ordenar_por_superficie():
    opcion= questionary.select(
        message="Selecciona: ",
        choices=["1. Ordenar de manera ascendente",
"2. Ordenar de manera descendente"]
    ).ask()
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        lector=csv.DictReader(archivo)
        paises=list(lector)
        match opcion:
            case "1. Ordenar de manera ascendente":
                paises_ordenados = sorted(paises, key=lambda pais: int(pais["superficie"]))
                for pais in paises_ordenados:
                    print(f"\nPais: {pais["nombre"]}")
                    print(f"Superficie: {pais["superficie"]} km²\n")
                    print("-"*30)
            case "2. Ordenar de manera descendente":
                paises_ordenados = sorted(paises, key=lambda pais: int(pais["superficie"]),reverse=True)
                for pais in paises_ordenados:
                    print(f"\nPais: {pais["nombre"]}")
                    print(f"Superficie: {pais["superficie"]} km²\n")
                    print("-"*30)
            case _:
                print("La opción ingresada es incorrecta")

def pais_moyor_menor_pablacion():
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        lector=csv.DictReader(archivo)
        #convierte al lector en una lista para poder utilizar max y min
        paises=list(lector)
        #busco el país con mayor poblacion comparando los valores de la columna población 
        mayor_poblacion=max(paises,key=lambda pais:int(pais["poblacion"]))
        print(f"El país con mayor población es {mayor_poblacion["nombre"]}")
        menor_poblacion=min(paises,key=lambda pais:int(pais["poblacion"]))
        print(f"El país con menor población es {menor_poblacion["nombre"]}\n")

def promedio_poblacion():
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        lector=csv.DictReader(archivo)
        #tranformo el lector en lista para utilizar len
        paises=list(lector)
        suma=0
        #recorro cada pais en el lista y busco los valores de sus poblaciones y las sumo
        for pais in paises:
            suma+=int(pais["poblacion"])
        #hago el promedio en base a la suma obtenida de las poblaciones y la cantidad de países
        promedio=suma/len(paises)
        print(f"El promedio de la población es {promedio}\n")
#hago lo mismo que en promedio_población pero con los valores de la columna superficie
def promedio_superficie():
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        lector=csv.DictReader(archivo)
        paises=list(lector)
        suma=0
        for pais in paises:
            suma+=int(pais["superficie"])
        promedio=suma/len(paises)
        print(f"El promedio de la superficie es de {promedio} km²\n")

def cantidad_por_continente():
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        lector=csv.DictReader(archivo)
        #genero una diccionario y le asigno el valor 0 a cada continente
        contador_continentes={"África":0,"América":0,"Asia":0,"Europa":0,"Oceanía":0}
        for pais in lector:
            #recorro los paises del archivo y cada vez que encuentre un continente le suma 1
            if pais["continente"] in contador_continentes:
                contador_continentes[pais["continente"]]+=1
        print(f"Los pasises por continentes son: {contador_continentes}\n")
