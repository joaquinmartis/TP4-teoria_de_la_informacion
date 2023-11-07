import numpy as np

def leeArchivo(archivo):
    with open(archivo, "r") as f:
        linea= f.readline();

        if linea :
            probabilidades_simbolos = linea.split()   
            probabilidades_simbolos = [float(probabilidad) for probabilidad in probabilidades_simbolos]
        for linea in f:
            linea = linea.split()
            linea = [float(valor) for valor in linea]
            matriz.append(linea)

        print(probabilidades_simbolos)
        print(matriz)
        return probabilidades_simbolos, matriz

def simular_mensajes(matriz,probabilidades_simbolos,N,M):
    mensaje=[]
    for i in range(N):
        mensaje.append(np.random.choice(len(probabilidades_simbolos),M,probabilidades_simbolos))
        print(mensaje)
    return mensaje

matriz=[]
probabilidades_simbolos,matriz=leeArchivo("tp4_sample0.txt")

n_mensajes=3
m_mensajes=4
simulacion_mensajes=simular_mensajes(matriz,probabilidades_simbolos,n_mensajes,m_mensajes)
