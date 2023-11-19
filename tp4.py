import numpy as np
import sys

def leeArchivo(archivo):
    with open(archivo, "r") as f:
        linea= f.readline();

        if linea :
            probabilidades_simbolos = linea.split()   
            probabilidades_simbolos = [float(probabilidad) for probabilidad in probabilidades_simbolos] # primero lee probabilidad de 1 y 0
     
        for linea in f: #probabilidad de que salga un simbolo despues de otro simbolo
            linea = linea.split()
            linea = [float(valor) for valor in linea]
            matriz.append(linea)

        return probabilidades_simbolos, matriz

def simular_mensajes(matriz,probabilidades_simbolos,N,M):
    mensaje=[]
    for i in range(N):
        mensaje.append(np.random.choice(len(probabilidades_simbolos),M,probabilidades_simbolos)) #Crea N mensajes de longitud M

    return mensaje

matriz=[]

def calcula_entropia_canal(matriz,probabilidades_simbolos):
    entropia_canal=0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if(matriz[i][j]!=0):
                xxx entropia_canal+=matriz[i][j]*probabilidades_simbolos[i]*np.log2(1/matriz[i][j])
    return entropia_canal

def calcula_equivocacion_canal(matriz,probabilidades_simbolos):


if (len(sys.argv) ==4 or len(sys.argv) ==5):
    probabilidades_simbolos,matriz=leeArchivo(sys.argv[1]) #Punto a
    n_mensajes=int(sys.argv[2])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    m_mensajes=int(sys.argv[3])
    flag_paridad_cruzada= ((len(sys.argv) == 5) and (sys.argv[4]=="-p"))


#   P00=P(b=0/a=0) P01=P(b=1/a=0) 
#   P10=P(b=0/a=1) P11=P(b=1/a=1)

    simulacion_mensajes=simular_mensajes(matriz,probabilidades_simbolos,n_mensajes,m_mensajes)


