from funciones import*
escribir_csv(paises)

while True:
    opcion=menu()
    try:
        match(opcion):
            case "1. Agregar país":
                agregar_pais()
                input("\nPresione enter para continuar")
                limpiar_consola()
            case "2. Actualizar población y superficie":
                input("\nPresione enter para continuar")
                limpiar_consola()
            case "3. Buscar país":
                buscar_pais()
                input("\nPresione enter para continuar")
                limpiar_consola()
            case "4. Filtrar país":
                while True:
                    opcion=filtrar_menu()
                    match(opcion):
                        case "1. Continente":
                            filtrar_pais_continente()
                        case "2. Rango de población":
                            filtrar_por_población()
                        case "3. Rango de superficie":
                            filtrar_por_superficie()
                        case "4. Salir":
                            print("Volviendo al menú principal")
                            break
                input("\nPresione enter para continuar")
                limpiar_consola()
            case "5. Ordenar países":
                while True:
                    opcion=ordenar_menu()
                    match(opcion):
                        case "1. Nombre":
                            ordenar_por_pais()
                        case "2. Población":
                            ordenar_por_poblacion()
                        case "3. Superficie":
                            ordenar_por_superficie()
                        case "4. Salir":
                            print("Volviendo al menú principal")
                            break
                input("\nPresione enter para continuar")
                limpiar_consola()
            case "6. Mostrar estadísticas":
                while True:
                    opcion=estadistica_menu()
                    match (opcion):
                        case "1. País con mayor y menor población":
                            pass
                        case "2. Promedio de población":
                            pass
                        case "3. Promedio de superficie":
                            pass
                        case "4. Cantidad de países por continente":
                            pass
                        case "5. Salir":
                            print("Volviendo al menú principal")
                            break
                input("\nPresione enter para continuar")
                limpiar_consola()
            case "7. Salir":
                print("Hasta luego!")
                break
    except FileNotFoundError:
        print("Error: No se encontró el archivo paises.csv")
    except KeyError:
        print("Error: el archivo no contiene las columnas esperadas")
    except PermissionError:
        print("Error: El archivo esta siendo utilizado en otro programa")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: ocurrió un error inesperado {e}")