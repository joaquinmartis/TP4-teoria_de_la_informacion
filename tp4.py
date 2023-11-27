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

def aplica_paridad_cruzada(mensaje,flag_paridad_cruzada):
    if flag_paridad_cruzada==True:
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
        nuevo_mensaje=np.array(nuevo_mensaje)
        mensaje_con_paridad_cruzada.append(nuevo_mensaje)
    else:
        mensaje_con_paridad_cruzada=mensaje
    return mensaje_con_paridad_cruzada

def enviar_mensaje_por_canal(matriz,mensaje_con_paridad_cruzada): #Solo vale para binario
    mensaje_enviado_por_canal=[]
    for i in range(len(mensaje_con_paridad_cruzada)):
        mensaje_enviado_por_canal.append([])
        for j in range(len(mensaje_con_paridad_cruzada[i])):
            if random.uniform(0,1) < matriz[mensaje_con_paridad_cruzada[i][j]][0]: 
                mensaje_enviado_por_canal[i].append(0)
            else:
                mensaje_enviado_por_canal[i].append(1)
    return mensaje_enviado_por_canal
                
def verificaFilas(mensaje_enviado_por_canal):
    filasIncorrectas=[]
    # Obtener las dimensiones de la matriz
    N = len(mensaje_enviado_por_canal)
    M = len(mensaje_enviado_por_canal[0])

    for i in range(N-1):
        suma_fila = sum(mensaje_enviado_por_canal[i][j] for j in range(M-1))
        # Comparar con el elemento en la posición N de la fila
        if suma_fila % 2 != mensaje_enviado_por_canal[i][M-1]:
            filasIncorrectas.append(i)
    return filasIncorrectas               

def verificaColumnas(mensaje_enviado_por_canal):
    columnasIncorrectas=[]
    # Obtener las dimensiones de la matriz
    N = len(mensaje_enviado_por_canal)
    M = len(mensaje_enviado_por_canal[0])

    for j in range(M-1):
        suma_columna = sum(mensaje_enviado_por_canal[i][j] for i in range(N-1))
        # Comparar con el elemento en la posición N de la fila
        if suma_columna % 2 != mensaje_enviado_por_canal[N-1][j]:
            columnasIncorrectas.append(j)
    return columnasIncorrectas    


def verificaBitCruzado(mensaje_enviado_por_canal):
    columnasIncorrectas=[]
    # Obtener las dimensiones de la matriz
    N = len(mensaje_enviado_por_canal)
    M = len(mensaje_enviado_por_canal[0])
    
    bits_control= sum(mensaje_enviado_por_canal[N-1][j] for j in range(M-1)) + sum(mensaje_enviado_por_canal[i][M-1] for i in range(N-1))
    return bits_control % 2 == mensaje_enviado_por_canal[N-1][M-1] 

def verificacion_y_correccion(mensaje_enviado_por_canal,flag_paridad_cruzada,n_mensajes):
    correctos=0
    errores=0
    corregidos=0

    mensaje_corregido=mensaje_enviado_por_canal.copy()
    
    if(flag_paridad_cruzada):
        print("Deteccion de errores con paridad cruzada")
        filas_error= verificaFilas(mensaje_enviado_por_canal)
        columnas_error= verificaColumnas(mensaje_enviado_por_canal)
        bitcruzado=verificaBitCruzado(mensaje_enviado_por_canal)
        print("Filas incorrectas: ",len(filas_error))
        print("Columnas incorrectas: ",len(columnas_error))
        print("Bit de paridad cruzada incorrecto: ",bitcruzado)

        if len(filas_error)==0 :
            if len(columnas_error)==0: #si el bit de cruzado es incorrecto, se considera un unico error (del bit de cruzado)
                correctos = n_mensajes
            elif len(columnas_error)==1 and bitcruzado!=1: #si hay solo una columna no coincidente y el bit cruzado no es correcto (se considera error de bit control de columna y por ende la info esta ok)
                correctos = n_mensajes
            else:
                errores = n_mensajes #una columna abarca todos los mensajes
        elif len(columnas_error)==0:
            if len(filas_error)==1 and bitcruzado!=1:
                correctos = n_mensajes
            else:
                errores = len(filas_error) #los errores se toman en las filas detectadas
        elif (len(columnas_error)+len(filas_error))==2 and bitcruzado==True:
            errores=1
            correctos= n_mensajes-1 
            corregidos=1
            if mensaje_enviado_por_canal[filas_error[0]][columnas_error[0]] == 1:
                 mensaje_corregido[filas_error[0],columnas_error[0]]=0
            else:
                 mensaje_corregido[filas_error[0],columnas_error[0]]=1
            print("Mensaje corregido")
            print("Enviado:   " + str(mensaje_enviado_por_canal[filas_error[0]]))
            print("Corregido: " + str(mensaje_corregido[filas_error[0]]))
        else:
            errores = n_mensajes
        print ("Se recibieron ",n_mensajes, " de los cuales se recibieron correctamente: ",correctos ," y ", errores," fueron errores. Pudieron corregirse ",corregidos," errores.")

def main():
    if (len(sys.argv) ==4 or len(sys.argv) ==5):
        n_mensajes=int(sys.argv[2])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        m_mensajes=int(sys.argv[3])
        flag_paridad_cruzada= ((len(sys.argv) == 5) and (sys.argv[4]=="-p"))
        archivo=sys.argv[1]

        #Leer del archivo probs.txt las probabilidades de la fuente binaria (primera línea) y la matriz del canal binario (segunda y tercera línea).
        probabilidades_simbolos,matriz=leeArchivo(archivo)
        matriz_probabilidades_sucesos_simultaneos=calcula_matriz_probabilidades_sucesos_simultaneos(matriz,probabilidades_simbolos) #listo

        #Calcular las entropías del canal, la equivocación y la información mutua.
        probabilidades_salidas=calcula_probabilidades_salidas(matriz,probabilidades_simbolos) #Obtengo las probabilidades de salida de cada simbolo FUNCIONA


        entropia_fuente=calcula_entropia_fuente(probabilidades_simbolos) # H(A)
        entropia_canal=calcula_entropia_canal(probabilidades_salidas) # H(B)
        entropia_a_posteriori=calcula_entropias_a_posteriori(probabilidades_salidas,matriz_probabilidades_sucesos_simultaneos) #MAL
            
        #Equivocacion
        equivocacion_canal=calcula_equivocacion_canal(matriz,probabilidades_simbolos) #listo
            
        #Entropía del canal Afín
        entropia_afin= entropia_canal - equivocacion_canal

        #Informacion Mutua
        informacion_mutua=entropia_fuente-equivocacion_canal #listo

        print("Entropía de la fuente o a-priori, H(A) =", entropia_fuente)
        print("Entropia del canal, H(B) =", entropia_canal)
        print("Entropia afín, H(A,B) =", entropia_afin)
        print("Entropía a posteriori:")
        i=0
        for valor in entropia_a_posteriori:
            print("H(A/B=",i,") = ",valor)
            i=i+1
        print("Equivocacion, H(A/B)=",equivocacion_canal)
        print("Información mutua, I(A,B)=", informacion_mutua)

        simulacion_mensajes=simular_mensajes(matriz,probabilidades_simbolos,n_mensajes,m_mensajes)

        mensaje_a_enviar=aplica_paridad_cruzada(simulacion_mensajes,flag_paridad_cruzada)

        print("Mensaje a enviar")
        for i in range(len(mensaje_a_enviar)):
            print(mensaje_a_enviar[i])
        mensaje_enviado_por_canal=enviar_mensaje_por_canal(matriz,mensaje_a_enviar)
        
        print("Mensaje enviado por canal")
        prueba=np.array(mensaje_enviado_por_canal)
        for i in range(len(prueba)):
            print(prueba[i])

        verificacion_y_correccion(mensaje_enviado_por_canal,flag_paridad_cruzada,n_mensajes)
        
    else:
        print("Error en los parametros de entrada")
        print("Ejemplo: python3 tp4.py probs.txt 100 100 -p")

if __name__ == "__main__":
    main()