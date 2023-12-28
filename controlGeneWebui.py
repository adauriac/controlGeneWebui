import serial
import minimalmodbus
import serial.tools.list_ports as port_list
from webui import webui

"""
example d'acces aux registres de la carte + webui = LA TOTALE
"""

def getRegisters():
    global vals
    ans = ""
    for i in range(len(ou)):
        v = instrument.read_registers(ou[i],1)
        vals[i] = v[0]
        ans += "%2d Ox%x %3d %26s %d\n"%(i,ou[i],ou[i],quoi[i],v[0])
    return ans

def my_function2(e : webui.event):
    print(f"entering my_function2 {e.window.get_str(e, 0)}")
    ans = ""
    for k in range(len(ou)):
        ans += "%d %d "%(ou[k],vals[k])
    return ans[:-1]; # suppression du ' ' final

def my_function(e:webui.event):
    global quoi,index
    k = index["Puissance limite basse"] 
    ans = vals[0]
    print(f"hello from python {e} k= {k}, ans={ans}")
    print(f"e.bind_id {e.bind_id}")
    print(f"e.element {e.element}")
    print(f"e.event_num {e.event_num}")
    print(f"e.event_type {e.event_type}")
    print(f"e.window {e.window}")

    return ans

quoi = []
ou = []
index= dict()

quoi.append("Arret d'urgence");
ou.append(0x65);
index["Arret d'urgence"] = len(ou)-1;

quoi.append("Defaut critique");
ou.append(0x66);
index["Defaut critique"] = len(ou)-1;

quoi.append("Mesure debit");
ou.append(0x68);
index["Mesure debit"] = len(ou)-1;

quoi.append("Mesure puissance");
ou.append(0x6B);
index["Mesure puissance"] = len(ou)-1;

quoi.append("Etat du procede");
ou.append(0x6E);
index["Etat du procede"] = len(ou)-1;

quoi.append("Tension PFC ");
ou.append(0x72);
index["Tension PFC "] = len(ou)-1;

quoi.append("Courant pont");
ou.append(0x7F);
index["Courant pont"] = len(ou)-1;

quoi.append("Puissance limite basse");
ou.append(0x96);
index["Puissance limite basse"] = len(ou)-1;

quoi.append("Puissance limite haute");
ou.append(0x97);
index["Puissance limite haute"] = len(ou)-1;

quoi.append("Debit bas");
ou.append(0xA0);
index["Debit bas"] = len(ou)-1;

quoi.append("Debit haut");
ou.append(0xA1);
index["Debit haut"] = len(ou)-1;

quoi.append("Consigne puissance");
ou.append(0xB2);
index["Consigne puissance"] = len(ou)-1;

quoi.append("Consigne debit");
ou.append(0xB3);
index["Consigne debit"] = len(ou)-1;

quoi.append("Generateur");
ou.append(0xBB);
index["Generateur"] = len(ou)-1;

quoi.append("Gaz");
ou.append(0xBC);
index["Gaz"] = len(ou)-1; 

quoi.append("Plasma");
ou.append(0xBD);
index["Plasma"] = len(ou)-1;

vals = list(map(lambda x:-1,quoi))
ports = list(port_list.comports())
for p in ports:
    print(p)
    port = ports[0].device
    ser = serial.Serial(port)
    print("using "+ser.name)
    instrument = minimalmodbus.Instrument(ser, 3)
    break

instrument.serial.baudrate = 9600
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.mode = 'rtu'
# instrument.debug = True
instrument.timeout = 2 # seconds

while True:       
    state = getRegisters()
    print(state)
    break #  !!!!
    ans = input("entrer le numéro du registre et la valeur a y mettre, ou q pour quitter ")
    if ans=='q':
        break
    ans = ans.split()
    if len(ans)!=2:
        continue
    try:
        ans = list(map(int,ans))
    except:
        continue
    o,q = ans

    instrument.write_registers(ou[o],[q])
    # TRAITEMENT DES ERREURS

MyWindow = webui.window()
MyWindow.show("controlGeneWebui.html",webui.browser.firefox)

# MyWindow.bind("powerLowLimit", my_function)
# MyWindow.bind("powerHighLimit", my_function)
MyWindow.bind("my_function2", my_function2) # Geoffroy a prpose ca
MyWindow.bind("go", my_function)
webui.wait()
# wrssdnuw_di
