import numpy as np
import sys
import random

def leeArchivo(archivo):
    with open(archivo, "r") as f:
        linea= f.readline();
        matriz=[]
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

def calcula_equivocacion_canal(matriz,probabilidades_simbolos):
    equivocacion_canal=0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if(matriz[i][j]!=0):
                equivocacion_canal+=matriz[i][j]*probabilidades_simbolos[i]*np.log2(1/matriz[i][j]) #H(A/B)= sum (P(a,b) * log ( 1/P (a /b))) || P(a,b)=P(b/a)*P(b)
    return equivocacion_canal

def calcula_entropia_fuente(probabilidades_simbolos):
    entropia_fuente=0
    for i in range(len(probabilidades_simbolos)):
        if probabilidades_simbolos[i]!=0:
            entropia_fuente+=probabilidades_simbolos[i]*np.log2(1/probabilidades_simbolos[i])
    return entropia_fuente

def calcula_entropia_canal(probabilidades_salidas):
    entropia_canal=0
    for i in range(len(probabilidades_salidas)): 
        if probabilidades_salidas[i]!=0:
            entropia_canal+=probabilidades_salidas[i]*np.log2(1/probabilidades_salidas[i])       
    return entropia_canal

def calcula_probabilidades_salidas(matriz,probabilidades_simbolos): #No tiene mucho sentido el calculo porque el canal es binario, 
    #            se podria hacer el calculo de probabilidad de un simbolo y luego hacer 1-probabilidad para obtener la probabilidad del otro simbolo
    probabilidades_salidas=[]
    transpose=np.transpose(matriz)
    for i in range(len(transpose)):
        probabilidades_salidas.append(np.array(probabilidades_simbolos) @ np.array(transpose[i])) #Producto Escalar entre probabilidades de entrada y probabilidad de salida de uno de los simbolos
    return probabilidades_salidas

def calcula_matriz_probabilidades_sucesos_simultaneos(matriz,probabilidades_simbolos):
    matriz_probabilidades_sucesos_simultaneos=np.zeros((len(matriz),len(matriz[0])))
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            matriz_probabilidades_sucesos_simultaneos[i,j]=(matriz[i][j]*probabilidades_simbolos[i])
    return matriz_probabilidades_sucesos_simultaneos

def calcula_entropias_a_posteriori(probabilidades_salidas,matriz_probabilidades_sucesos_simultaneos):
    entropias_a_posteriori=[]
    print(matriz_probabilidades_sucesos_simultaneos)
    print(probabilidades_salidas)
    
    for j in range(len(matriz_probabilidades_sucesos_simultaneos[0])):
        x=0
        for i in range(len(matriz_probabilidades_sucesos_simultaneos)):
            aux=matriz_probabilidades_sucesos_simultaneos[i][j]/probabilidades_salidas[j]
            x+=aux*np.log2(1/aux)
        entropias_a_posteriori.append(x)
    print(entropias_a_posteriori)
    return entropias_a_posteriori

def calcula_paridad_cruzada(mensaje):
    mensaje_con_paridad_cruzada=[]
    contador_columnas=0
    contador_filas=0
    for i in range(len(mensaje)): # Primero calcula paridad de las filas
        contador=0
        for j in range(len(mensaje[i])):
            if mensaje[i][j]==1:
                contador+=1
        if contador%2==0:
            mensaje_con_paridad_cruzada.append(np.append(mensaje[i],0))
        else:
            mensaje_con_paridad_cruzada.append(np.append(mensaje[i],1))
            contador_filas+=1
    nuevo_mensaje=[] #Luego calcula la paridad de las columnas

    for i in range(len(mensaje[0])): 
        contador=0
        for j in range(len(mensaje)):
            if mensaje[j][i]==1:
                contador+=1
        if contador%2==0:
            nuevo_mensaje.append(0)
        else:
            nuevo_mensaje.append(1)
            contador_columnas+=1

    if contador_columnas%2==0 != contador_filas%2==0: # EL != SERIA LA OPERACION XOR.  Si son iguales va 0, si son distintos va 1
        nuevo_mensaje.append(1)
    else:
        nuevo_mensaje.append(0)
        
    mensaje_con_paridad_cruzada.append(nuevo_mensaje)
    for i in range(len(mensaje_con_paridad_cruzada)-1):
        print(mensaje_con_paridad_cruzada[i])
        #print(mensaje[i])
        print(" ")
    print(mensaje_con_paridad_cruzada[len(mensaje_con_paridad_cruzada)-1])
    return mensaje_con_paridad_cruzada

def enviar_mensaje_por_canal(matriz,mensaje_con_paridad_cruzada): #Solo vale para binario
    mensaje_enviado_por_canal=[]
    for i in range(len(mensaje_con_paridad_cruzada)):
        mensaje_enviado_por_canal.append([])
        for j in range(len(mensaje_con_paridad_cruzada[i])):
            if random.uniform(0,1) < matriz[mensaje_con_paridad_cruzada[i,j],0]: 
                mensaje_enviado_por_canal[i].append(0)
            else:
                mensaje_enviado_por_canal[i].append(1)
    print("Mensaje enviado por canal")
    for i in range(len(mensaje_enviado_por_canal)):
        print(mensaje_enviado_por_canal[i])
    return mensaje_enviado_por_canal
                

def main():
    if (True or len(sys.argv) ==4 or len(sys.argv) ==5): #SACAR EL 1--------------------------------------
        #n_mensajes=int(sys.argv[2])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        #m_mensajes=int(sys.argv[3])
       #flag_paridad_cruzada= ((len(sys.argv) == 5) and (sys.argv[4]=="-p"))
        #archivo=sys.argv[1]
        flag_paridad_cruzada= True
        archivo="tp4_sample6.txt"
        n_mensajes=5
        m_mensajes=10
        random.seed(2)
        print("Simulacion de mensajes")
        for i in range(10):  
            print(random.uniform(0.0,1.0))
        #Leer del archivo probs.txt las probabilidades de la fuente binaria (primera línea) y la matriz del canal binario (segunda y tercera línea).
        probabilidades_simbolos,matriz=leeArchivo(archivo)
        matriz_probabilidades_sucesos_simultaneos=calcula_matriz_probabilidades_sucesos_simultaneos(matriz,probabilidades_simbolos) #listo

        #Calcular las entropías del canal, la equivocación y la información mutua.
        probabilidades_salidas=calcula_probabilidades_salidas(matriz,probabilidades_simbolos) #Obtengo las probabilidades de salida de cada simbolo FUNCIONA
        entropia_fuente=calcula_entropia_fuente(probabilidades_simbolos) # H(A)
        
        
        entropia_a_posteriori=calcula_entropias_a_posteriori(probabilidades_salidas,matriz_probabilidades_sucesos_simultaneos) #MAL
        
        print("Entropias del canal")
            #Entropias del canal
        
        entropia_canal=calcula_entropia_canal(probabilidades_salidas) # H(B)
        print("H(B) = "+str(entropia_canal))
        print("Entropias a posteriori")
        
            #Equivocacion
        equivocacion_canal=calcula_equivocacion_canal(matriz,probabilidades_simbolos) #listo
            #Informacion Mutua
        informacion_mutua=entropia_fuente-equivocacion_canal #listo

    #   P(a=0)=txt P(a=1)=txt
    #   P00=P(b=0/a=0) P01=P(b=1/a=0) 
    #   P10=P(b=0/a=1) P11=P(b=1/a=1)

        simulacion_mensajes=simular_mensajes(matriz,probabilidades_simbolos,n_mensajes,m_mensajes)


        #simulacion_mensajes=[[0, 1, 1, 1, 1, 1, 1, 0, 0, 0],# 0
        #                     [0, 0, 1, 1, 1, 0, 0, 1, 1, 1],# 0
        #                     [1, 1, 1, 1, 0, 1, 1, 0, 0, 0],# 0
        #                     [0, 1, 0, 0, 1, 1, 0, 1, 0, 0],# 0
        #                     [0, 0, 1, 0, 1, 0, 1, 1, 0, 1]]# 1
        #                    # 1  1  0  1  0  1  1  1  1  0    0
        mensaje_con_paridad_cruzada=calcula_paridad_cruzada(simulacion_mensajes)

        mensaje_enviado_por_canal=enviar_mensaje_por_canal(matriz,mensaje_con_paridad_cruzada)
    else:
        print("Error en los parametros de entrada")
        print("Ejemplo: python3 tp4.py probs.txt 100 100 -p")

main()