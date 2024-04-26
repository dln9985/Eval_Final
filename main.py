import threading
import time
import pandas as pd

def leer_archivo(archivo):
    Sheet = pd.read_excel(archivo, header=None, index_col=None)
    numeros = Sheet.values.flatten()
    
    print("Todos los números en el archivo:")
    for i in range(0, len(numeros), 20):
        for j in range(i, min(i + 20, len(numeros))):
            numero = numeros[j]
            print(f"{numero:6d}", end='')
        print()
    
    print()
    return numeros

def suma_parcial(numeros, inicio, fin, resultado):
    suma = 0
    for i in range(inicio, fin):
        suma += numeros[i]
    resultado.append(suma)

def suma_total(numeros, num_hilos):
    tamano = len(numeros)
    tamano_por_hilo = tamano // num_hilos
    hilos = []
    sumas_parciales = []
    inicio = 0

    print("")
    print(f"Cantidad de hilos a emplear: {num_hilos}")
    
    for i in range(num_hilos):
        fin = inicio + tamano_por_hilo if i < tamano % num_hilos else inicio + tamano_por_hilo
        print(f"Hilo {i+1}: {inicio + 1} - {fin}") 
        
        hilo = threading.Thread(target=suma_parcial, args=(numeros, inicio, fin, sumas_parciales))
        hilos.append(hilo)
        inicio = fin

    start_time = time.time()
    
    for hilo in hilos:
        hilo.start()
        
    for hilo in hilos:
        hilo.join()

    tiempo_de_ejecucion = time.time() - start_time

    return sum(sumas_parciales), tiempo_de_ejecucion, sumas_parciales

if __name__ == "__main__":
    while True:
        nombre_archivo = input("Ingrese el nombre del archivo Excel: ")
        if nombre_archivo == "datos-Eval-Final.xlsx":
            break
        else:
            print("El archivo que se solicita no está disponible. Intente nuevamente.")

    numeros = leer_archivo(nombre_archivo)
        
    if numeros is not None and len(numeros) > 0:
        while True:
            num_hilos = input("Ingrese el número de hilos a emplear (entre 2 y 10): ")
            if num_hilos.isdigit():
                num_hilos = int(num_hilos)
                if 2 <= num_hilos <= 10:
                    break

        suma_total, tiempo_ejecucion, sumas_parciales = suma_total(numeros, num_hilos)

        print("")
        print("Sumas parciales de cada hilo:")
        for i in range(len(sumas_parciales)):
            print(f"Hilo {i+1}: {sumas_parciales[i]}")
        print("")
        print("Suma Total:", suma_total)
        print("Tiempo de ejecución:", tiempo_ejecucion)
        print("")