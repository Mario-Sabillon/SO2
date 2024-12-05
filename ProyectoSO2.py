import threading
import random
import time

def obtener_num_filosofos():
    while True:
        try:
            cantidad = int(input("Ingrese la cantidad de filósofos (entre 2 y 10): "))
            if 2 <= cantidad <= 10:
                return cantidad
            else:
                print("El valor debe estar dentro del rango especificado.")
        except ValueError:
            print("Por favor, ingrese un número válido.")

def Sentarse(filosofo_id, total_filosofos, plato):
    
    #Referencia los tenedores izquierdo y derecho de cada filosofo
    
    tenedor_izq = tenedores[filosofo_id]
    tenedor_der = tenedores[(filosofo_id + 1) % total_filosofos]
    
    print(f"{filosofos[filosofo_id]} se sentó en la mesa, su plato tiene {plato} porciones.")
    time.sleep(1)
    
    
    while plato > 0:
        
        # Intentar adquirir ambos tenedores
        
        tenedor_izq.acquire() # Toma el tenedor izquierdo
        print(f"{filosofos[filosofo_id]} toma el tenedor izquierdo.")

        if  tenedor_der.acquire(timeout=1) == False:  # Intentar adquirir el tenedor derecho con un tiempo de espera
            tenedor_izq.release() # solto el tenedor izquierdo
            print(f"{filosofos[filosofo_id]} no pudo tomar el tenedor derecho y suelta el tenedor izquierdo.")
            time.sleep(random.uniform(1, 2))  # Esperar un tiempo aleatorio antes de volver a intentar
            continue
        else:
            print(f"{filosofos[filosofo_id]} toma el tenedor derecho.")
        try:
            # Comer aleatoriamente entre 1 y 2 bocados
            bocados = random.randint(1, 2)
            if plato >= bocados:
                plato -= bocados
                print(f"{filosofos[filosofo_id]} está comiendo {bocados} bocados. Bocados restantes en el plato de {filosofos[filosofo_id]}: {plato}")
            else:
                print(f"{filosofos[filosofo_id]} está comiendo {plato} bocados. Bocados restantes en el plato de {filosofos[filosofo_id]}: 0 ")
                plato = 0
        finally:
            # Liberar tenedores
                tenedor_izq.release()
                tenedor_der.release()
                print(f"{filosofos[filosofo_id]} suelta ambos tenedores.")
                print(f"{filosofos[filosofo_id]} está pensando.")
                
                time.sleep(random.uniform(1, 2))
    else:
        print(f"********************************{filosofos[filosofo_id]} Ha terminado de cenar**********************")

if __name__ == "__main__":
    cantidad_filosofos = obtener_num_filosofos()
    
    # Se crea una lista de filosofos con sus nombres
    filosofos = ["(1. Socrates)", "(2. Aristoteles)", "(3. Kant)", "(4. Descartes)", "(5. Nietzsche)", "(6. Locke)", "(7. Hegel)", "(8. Sartre)", "(9. Hume)", "(10. Platon)"]
    
    # Se crean los tenedores semaforos
    tenedores = [threading.Semaphore(1) for _ in range(cantidad_filosofos)]  
    
    # Se crean los Filosofos Hilos, ademas platos con cantidades aleatorias de porciones de comida
    Filosofos_Hilos = []
    for i in range(cantidad_filosofos):
        plato = random.randint(1, 10) 
        hilo = threading.Thread(target=Sentarse, args=(i, cantidad_filosofos,plato))
        Filosofos_Hilos.append(hilo)
        hilo.start()

    for hilo in Filosofos_Hilos:
        hilo.join()
