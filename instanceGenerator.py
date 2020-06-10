import sys
import json
import random
from time import sleep

#Progress bar
def _printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    if iteration == total: 
        print()

#Generador
def _generarData(n, k):
    try:
        _printProgressBar(0, int(k)*int(n), prefix = 'Progreso:', suffix = 'Completado.', length = 50)
        for y in range (0,int(k)):
            data={}
            data["Trabajos"]={}
            tiempo=0            
            for x in range(1,int(n)+1):
                data["Trabajos"][x] ={}
                tiempo=random.randint(int(int(n)),int(int(n)*1.4))
                data["Trabajos"][x]["tiempolimite"]= tiempo
                data["Trabajos"][x]["procesamiento"]=random.randint(int(1), int(n))
                data["Trabajos"][x]["peso"]=random.randint(int(1),int(100))
                _printProgressBar((int(n)*int(y))+int(x),int(k)*int(n), prefix = 'Progreso:', suffix = 'Completado.', length = 50)
            data["TrabajosTotales"]=n
            with open('data_trabajos'+n+'_'+str(y+1)+'.json','w') as outfile:
                json.dump(data,outfile,sort_keys=True, indent=4, separators=(',', ': '))
            sleep(0.01)
        print(k+' instancias generadas correctamente.')
    except IOError as e:
        print(str(e.errno))

#Main
def main():
    while True:
        n = input('Trabajos: ')
        if(int(n)>0):
            break
        else:
            print('Ingrese una cantidad de trabajos mayor a cero.')
    while True:
        k = input('Ingresa el numero de instancias que deseas generar: ')
        if(int(k)>0):
            break
        else:
            print('El numero de instancias debe ser mayor a cero.')
    _generarData(n,k)
    
main()