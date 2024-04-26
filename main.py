import threading 
import time
import pandas as pd

print("")

def LecturaArchivo(archivo):
    Sheet = pd.read_excel(archivo, header=None, index_col=None)
    numeros = Sheet.values.flatten()
    print("Todos los números contenidos en el archivo:")
    for i in range(0, len(numeros), 20):
        for j in range(i, min(i + 20, len(numeros))):
            numero = numeros[j]
            print(f"{numero:6d}", end='')
        print()
    print()  
    return numeros

def calcular_suma_parcial(numeros, inicio, fin, resultado):
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

    print("\nCantidad de hilos a emplear:", num_hilos)
    for i in range(num_hilos):
        fin = inicio + tamano_por_hilo if i < tamano % num_hilos else inicio + tamano_por_hilo
        print("Hilo", 1+i, ":", inicio + 1, "-", fin) 
        hilo = threading.Thread(target=calcular_suma_parcial, args=(numeros, inicio, fin, sumas_parciales))
        hilos.append(hilo)
        inicio = fin

    start_time = time.time()
    
    for hilo in hilos:
        hilo.start()
        
    for hilo in hilos:
        hilo.join()

    tiempo_de_ejecucion = time.time() - start_time
    suma_total = sum(sumas_parciales)
    return tiempo_de_ejecucion, suma_total

if __name__ == "__main__":
    while True:
        nombre_archivo = input("Ingrese el nombre del archivo Excel: ")
        if nombre_archivo == "datos-Eval-Final.xlsx":
            break
        else:
            print("El archivo que se solicita no esta disponible. Intente nuevamente.")

    numeros = LecturaArchivo(nombre_archivo)
        
    if numeros is not None and len(numeros) > 0:
        while True:
            num_hilos = input("Ingrese el número de hilos a emplear (entre 2 y 10): ")
            if num_hilos.isdigit():
                num_hilos = int(num_hilos)
                if 2 <= num_hilos <= 10:
                    break

        tiempo_ejecucion, suma_total = suma_total(numeros, num_hilos)

        print("")
        print("Suma Total:", suma_total)
        print("Tiempo de ejecución:", tiempo_ejecucion)
        print("")