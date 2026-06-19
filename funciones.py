import csv
import os
from funciones import*
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

def verificar_numero(mensaje):
    while True:
        try:
            num=int(input(mensaje))
            if num<0:
                raise ValueError("El valor ingresado no puede ser negativo")
            return num
        except ValueError as e:
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
    pais_buscado=verificar_texto("Ingrese el país que desea actualizar: ")
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        lector=csv.DictReader(archivo)
        campos=lector.fieldnames
        filas=[]
        encontrado=False
        match (opcion):
            case "1. Actualizar población":
                for linea in lector:
                    if normalizar(pais_buscado)==normalizar(linea["nombre"]):
                        poblacion_nueva=verificar_numero("Ingrese el valor de la poblacion: ")
                        linea["poblacion"]=poblacion_nueva
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
    continente_elegido = menu_continentes()
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
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
    poblacion_menor=verificar_numero("Ingrese el rango inferior: ")
    poblacion_sup=verificar_numero("Ingrese el rango superior: ")
    if poblacion_menor<0 or poblacion_sup<0:
        raise ValueError("El valor de la población no puede ser negativo")
    if poblacion_menor>poblacion_sup:
        raise ValueError("El rango inferior no puede ser mayor al rango superior")
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        lector=csv.DictReader(archivo)
        encontrado=False
        for fila in lector:
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
    if superficie_menor<0 or superficie_sup<0:
        raise ValueError("El valor de la superficie no puede ser negativo")
    if superficie_menor>superficie_sup:
        raise ValueError("El rango inferior no puede ser mayor al rango superior")
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        lector=csv.DictReader(archivo)
        encontrado=False
        for fila in lector:
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
        lector=csv.DictReader(archivo)
        paises=list(lector)
        match opcion:
            case "1. Ordenar nombres de paises de A -> Z":
                paises_ordenados = sorted(paises, key=lambda pais: normalizar(pais["nombre"]))
                for pais in paises_ordenados:
                    print(f"\nPais: {pais["nombre"]}")
                    print(f"Población: {pais["poblacion"]}")
                    print(f"Superficie: {pais["superficie"]} km²")
                    print(f"Contienente: {pais["continente"]}\n")
                    print("-"*30)
            case "2. Ordenar nombres de paises de Z -> A":
                paises_ordenados = sorted(paises, key=lambda pais: normalizar(pais["nombre"]),reverse=True)
                for pais in paises_ordenados:
                    print(f"\nPais: {pais["nombre"]}")
                    print(f"Población: {pais["poblacion"]}")
                    print(f"Superficie: {pais["superficie"]} km²")
                    print(f"Contienente: {pais["continente"]}\n")
                    print("-"*30)
            case _:
                print("La opción ingresada es incorrecta")

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
        paises=list(lector)
        mayor_poblacion=max(paises,key=lambda pais:pais["nombre"])
        print(f"El país con mayor población es {mayor_poblacion["nombre"]}")
        menor_poblacion=min(paises,key=lambda pais:pais["nombre"])
        print(f"El país con menor población es {menor_poblacion["nombre"]}\n")

def promedio_poblacion():
    with open("paises.csv","r",newline="",encoding="utf-8-sig") as archivo:
        lector=csv.DictReader(archivo)
        paises=list(lector)
        suma=0
        for pais in paises:
            suma+=int(pais["poblacion"])
        promedio=suma/len(paises)
        print(f"El promedio de la población es {promedio}\n")

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
        africa=0
        america=0
        asia=0
        europa=0
        oceania=0
        for pais in lector:
            if pais["continente"]=="África":
                africa+=1
            elif pais["continente"]=="América":
                america+=1
            elif pais["continente"]=="Asia":
                asia+=1
            elif pais["continente"]=="Europa":
                europa+=1
            elif pais["continente"]=="Oceanía":
                oceania+=1
        print(f"La cantidad de paises que hay de África es: {africa} ")
        print(f"La cantidad de paises que hay de Asia es: {asia} ")
        print(f"La cantidad de paises que hay de América es: {america} ")
        print(f"La cantidad de paises que hay de Europa es: {europa} ")
        print(f"La cantidad de paises que hay de Oceanía es: {oceania} ")
