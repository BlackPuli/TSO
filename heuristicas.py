import sys
import json
from pprint import pprint
from pathlib import Path
import operator
from time import time
import threading

tardanza = 0
tiempo = 0

#Guardar información en archivo JSON

def saveJSON(trabajos, i, maquina, heuristica):
     with open('solucion_'+str(len(trabajos))+'_'+str(heuristica)+'_'+str(i)+'.json','w') as outfile:
        json.dump(maquina,outfile, indent=4, separators=(',', ': '))

#Ordenar array
def generarArray(trabajos,parametro):
    arrayTrabajos={}
    for x in range(1,len(trabajos)+1):
        arrayTrabajos[x]=(trabajos[str(x)][parametro])
    return(arrayTrabajos)

#Llenar mochila
def llenarMaquina(arrayTrabajos, traTiempos,traPesos, traProcesamiento, trabajos,i):
    global tardanza
    global tiempo
    tardanzaLocal=0
    tiempoActual = 0
    maquina =[]
    tardanzas={}
    tiempos={}
    for objeto in arrayTrabajos:
        tiempoActual += int(traProcesamiento[objeto[0]])
        tardanzaLocal= 0 if tiempoActual < int(traTiempos[objeto[0]]) else tiempoActual-int(traTiempos[objeto[0]])
        tardanzas[objeto[0]]=tardanzaLocal
        if(tardanzaLocal>0):
            tardanzaLocal = tardanzaLocal*(int(traPesos[objeto[0]]))
            tardanza+=tardanzaLocal
        tiempos[objeto[0]]=tiempoActual
        maquina.append(objeto)
    data = {}
    data["Solucion"]={}
    for x in maquina:
        trabajos[str(x[0])]["Tardanza"]=tardanzas[x[0]]
        trabajos[str(x[0])]["TiempoAcabado"]=tiempos[x[0]]
        data["Solucion"][x[0]]= trabajos[str(x[0])]
    data["TTP"]=tardanza
    return(data)

#Heuristica por valor
def H1_peso(traPesos,traTiempos, trabajos,traProcesamiento,i,ejecucion):
    global tardanza
    global tiempo
    arrayTrabajos = sorted(traPesos.items(), key=operator.itemgetter(1), reverse=True)
    # print("ORDENADO:")
    # print(arrayTrabajos)
    maquina=llenarMaquina(arrayTrabajos,traTiempos,traPesos, traProcesamiento,trabajos,i)
    # data = {}
    # data["Solucion"]={}
    # for x in maquina:
    #     data["Solucion"][x[0]]= trabajos[str(x[0])]
    # data["Tardanza"]=tardanza
    # data["TTP"]=tiempo
    # print("HEURISTICA POR PESO")
    # print("Tiempo de ejecucion = "+str(time()-ejecucion)+" segundos")
    # print("TARDANZA=================> "+str(tardanza))
    tJson = threading.Thread(name="JSONThread", target=saveJSON, args=(trabajos, i, maquina, "peso"))
    tJson.start()
    # with open('solucion_'+str(len(trabajos))+'_peso_'+str(i)+'.json','w') as outfile:
    #     json.dump(maquina,outfile, indent=4, separators=(',', ': '))
    # print("MAQUINA:")
    # print(maquina)
    tardanza = 0


#Heuristica por peso
def H2_tiempo(traTiempos,traPesos , trabajos, traProcesamiento,i,ejecucion):
    global tardanza
    global tiempo
    arrayTrabajos = sorted(traTiempos.items(), key=operator.itemgetter(1))
    # print("ORDENADO:")
    # print(arrayTrabajos)
    maquina=llenarMaquina(arrayTrabajos,traTiempos,traPesos, traProcesamiento,trabajos,i)
    # data = {}
    # data["Solucion"]={}
    # for x in maquina:
    #     data["Solucion"][x[0]]= trabajos[str(x[0])]
    # data["Tardanza"]=tardanza
    # data["TTP"]=tiempo
    # print("HEURISTICA POR TIEMPO")
    # print("Tiempo de ejecucion = "+str(time()-ejecucion)+" segundos")
    # print("TARDANZA=================> "+str(tardanza))
    tJson = threading.Thread(name="JSONThread", target=saveJSON, args=(trabajos, i, maquina, "tiempo"))
    tJson.start()
    # with open('solucion_'+str(len(trabajos))+'_tiempo_'+str(i)+'.json','w') as outfile:
    #     json.dump(maquina,outfile, indent=4, separators=(',', ': '))
    # print("MAQUINA:")
    # print(maquina)

    tardanza = 0

def H3_cociente( traTiempos, traPesos, trabajos, traProcesamiento,i,ejecucion):
    global tardanza
    global tiempo
    cocientes={}
    for x in range (1,len(trabajos)+1):
        cocientes[x]=float(traPesos[x])/float(traTiempos[x])
    cocientes = sorted(cocientes.items(), key=operator.itemgetter(1), reverse=True)
    # print("ORDENADOS")
    # print(cocientes)
    maquina=llenarMaquina(cocientes,traTiempos,traPesos, traProcesamiento,trabajos,i)
    # data = {}
    # data["Solucion"]={}
    # for x in maquina:
    #     data["Solucion"][x[0]]= trabajos[str(x[0])]
    # data["Tardanza"]=tardanza
    # data["TTP"]=tiempo
    # print("HEURISTICA POR COCIENTE")
    # print("Tiempo de ejecucion = "+str(time()-ejecucion)+" segundos")
    # print("TARDANZA=================> "+str(tardanza))
    tJson = threading.Thread(name="JSONThread", target=saveJSON, args=(trabajos, i, maquina, "cociente"))
    tJson.start()
    # with open('solucion_'+str(len(trabajos))+'_cociente_'+str(i)+'.json','w') as outfile:
    #     json.dump(maquina,outfile, indent=4, separators=(',', ': '))
    # print("MAQUINA:")
    # print(maquina)

    tardanza=0

def execThread(path, listaPath,i,trabajosT):
    json_load=json.load(open(path))
    trabajos = json_load["Trabajos"]
    if(trabajosT != 0 and len(trabajos) != trabajosT):
        i=1
    trabajosT=len(trabajos)
    # print("INSTANCIA #"+str(listaPath.index(path)+1))
    traPesos=generarArray(trabajos,"peso")
    traTiempo = generarArray(trabajos,"tiempolimite")
    traProcesamiento=generarArray(trabajos,"procesamiento")
    tiempoTotal = time()
    tiempoInicial = time()
    # H1_peso(traPesos,traTiempo,trabajos, traProcesamiento, i,tiempoInicial)

    # tiempoInicial = time()

    # H2_tiempo(traTiempo,traPesos,trabajos, traProcesamiento, i, tiempoInicial)
    # tiempoInicial = time()

    # H3_cociente(traTiempo,traPesos,trabajos,traProcesamiento, i, tiempoInicial)
    tPeso = threading.Thread(name="pesoThread", target=H1_peso, args=(traPesos, traTiempo, trabajos,traProcesamiento,i, tiempoInicial,))
    tTiempo = threading.Thread(name="tiempoThread", target=H2_tiempo, args=(traTiempo, traPesos, trabajos,traProcesamiento,i, tiempoInicial,) )
    tCociente = threading.Thread(name="cocienteThread", target=H3_cociente, args=(traTiempo, traPesos, trabajos,traProcesamiento,i, tiempoInicial,))
    tPeso.start()
    tTiempo.start()
    tCociente.start()
    tPeso.join()
    tTiempo.join()
    tCociente.join()
    print("Tiempo total instancia #"+str(i)+" "+str(time() - tiempoTotal) +" segundos")
    print("="*30)

#Main
def main():
    tiempoInicial = 0
    tiempoFinal=0
    p = Path('.')
    listaPath=list(p.glob('*.json'))
    i=1
    trabajosT=0
    for path in listaPath:
        t1=threading.Thread(name="threadPath", target=execThread, args=(path, listaPath, i, trabajosT))
        t1.start()
        # execThread(path,listaPath,i, trabajosT)
        i+=1
main()