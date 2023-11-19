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

def calcula_equivocacion_canal(matriz,probabilidades_simbolos):
    entropia_canal=0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if(matriz[i][j]!=0):
                equivocacion_canal+=matriz[i][j]*probabilidades_simbolos[i]*np.log2(1/matriz[i][j]) #H(A/B)= sum (P(a,b) * log ( 1/P (a /b))) || P(a,b)=P(b/a)*P(b)
    return entropia_canal

def calcula_entropia_fuente(probabilidades_simbolos):
    entropia_fuente=0
    for i in range(len(probabilidades_simbolos)):
        entropia_fuente+=probabilidades_simbolos[i]*np.log2(1/probabilidades_simbolos[i])
    return entropia_fuente


if (len(sys.argv) ==4 or len(sys.argv) ==5):
    n_mensajes=int(sys.argv[2])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    m_mensajes=int(sys.argv[3])
    flag_paridad_cruzada= ((len(sys.argv) == 5) and (sys.argv[4]=="-p"))
    
    #Leer del archivo probs.txt las probabilidades de la fuente binaria (primera línea) y la matriz del canal binario (segunda y tercera línea).
    probabilidades_simbolos,matriz=leeArchivo(sys.argv[1]) 
 

    #Calcular las entropías del canal, la equivocación y la información mutua.
    entropia_fuente=calcula_entropia_fuente() #listo
    equivocacion_canal=calcula_equivocacion_canal() #listo
    entropia_canal=
    informacion_mutua=entropia_fuente-equivocacion_canal #listo

#   P(a=0)=txt P(a=1)=txt
#   P00=P(b=0/a=0) P01=P(b=1/a=0) 
#   P10=P(b=0/a=1) P11=P(b=1/a=1)

    simulacion_mensajes=simular_mensajes(matriz,probabilidades_simbolos,n_mensajes,m_mensajes)


