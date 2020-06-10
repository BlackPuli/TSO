import sys
import json
from time import time
from pathlib import Path
from copy import copy

def reevaluar(trabajos, solucion):
    tiempoActual = 0
    tardanzaLocal = 0
    tardanza=0
    for objeto in trabajos:
        tiempoActual += int(trabajos[objeto[0]]["procesamiento"])
        tardanzaLocal= 0 if tiempoActual < int(trabajos[objeto[0]]["tiempolimite"]) else tiempoActual-int(trabajos[objeto[0]]["tiempolimite"])
        if(tardanzaLocal>0):
            tardanzaLocal = tardanzaLocal*(int(trabajos[objeto[0]]["peso"]))
            tardanza+=tardanzaLocal
        trabajos[objeto[0]]["Tardanza"]=tardanzaLocal
        trabajos[objeto[0]]["TiempoAcabado"]=tiempoActual
    solucion["TTP"]=tardanza
    solucion["Solucion"] = trabajos
    return solucion

def busqueda(trabajos, solucion):
    mejor={}
    TTP = int(solucion["TTP"])
    for objeto in trabajos:
        aux={}
        evaluada={}
        visited = []
        for trabajo in trabajos:
            if(trabajo != objeto and not visited.__contains__(trabajo[0])):
                visited.append(trabajo[0])
                aux =copy(trabajos[objeto[0]])
                trabajos[objeto[0]] = trabajos[trabajo[0]]
                trabajos[trabajo[0]]=aux
                evaluada = reevaluar(copy(trabajos), copy(solucion))
                if(evaluada != solucion):
                    mejor = evaluada
    if(mejor != {}):
        return mejor if int(mejor["TTP"]) < TTP else solucion
    else:
        return solucion



def main():
    tiempo = 0
    tiempoFinal = 0
    p = Path('.')
    listapath = list(p.glob('solucion_*.json'))
    for path in listapath:
        print(path)
        json_load= json.load(open(path))
        trabajos = json_load["Solucion"]
        tiempo = time()
        mejora = busqueda(copy(trabajos),copy(json_load))
        tiempoFinal = time()
        print(json_load["TTP"])
        if(json_load == mejora):
            print("No hubo mejora")
        else:
            json_load = mejora
            print("Hubo mejora "+str(json_load["TTP"]))
            with open('mejora_'+str(path),'w') as outfile:
                json.dump(json_load,outfile,sort_keys=False, indent=4, separators=(',', ': '))
        print("Tiempo de ejecucion = "+str(tiempoFinal-tiempo)+" segundos")
        

main()