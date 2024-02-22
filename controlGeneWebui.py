from controlGenePyCli import *
from webui import webui

"""
                                       GENERATOR'S GUI

This is one of (the main) of the 6 files :
frontend: controlGeneWebui.css 
          controlGeneWebui.html
          controlGeneWebui.js
          controlGeneWebUiError.html
backend:
          controlGeneWebui.py
          controlGenePyCli.py

run : "python  controlGeneWebui.py"

It open the controlGeneWebui.html (or controlGeneWebUiError.html in case of error) in a firefox browser.
controlGeneWebui.html run the javascript script controlGeneWebui.js which start a timer.
This timer run a python function 'myFunction' from controlGeneWebui.py.
Python receives a string which contains an even number of integer. It is "address value ... address value".
This function returns also a string with the same convention.
The js script modify accordingly the gui.

In case of connection error controlGeneWebUiError.html which contains a js script is loaded.

In case of lost connection detected by a timeout in read/wrtite procedure) the python backend
controlGeneWebui.py opens an alert and quit.

The way the widget are shown is decide in the frontend controlGeneWebui. This work could be splitted
using some convention not yet defined like led.on led.off led.invisible etc

When val is written in the register 0x66 (102) val+(0,256,512,768) is re-read ?

1) Le bouton generateur sert a mettre en chauffage DOIT ETRE FAIT EN PREMIER
2) Le bouton Gaz declenche le debit d'amorce NE PEUT ETRE FAIT QU'APRES 1)
3) Le bouton plasma debutte le process et NE PEUT ETRE FAIT QU'APRES 2)

"""

def getError(e : webui.event):
    global myGene
    print(f"from python {myGene.messageConnection} ")
    return myGene.messageConnection

def myFunction(e : webui.event):
    """
    1) affecte les registres en accord avec le paramtre contenu dans e
       sous la forme 'add val add val ... add val'
    2) retourne ai JS toutes les valeurs des registres
    """
    global myGene,cpt
    cpt += 1
    param = e.window.get_str(e, 0)
    print(f"python says :entering myFunction for the {cpt} times with |{param}|")
    if not myGene.connected:
        return "error"
    #           WRITE THE REGISTERS AS ASKED BY THE JS THRU THE PARAM
    params = param.split()
    for i in range(0,len(params),2):
        add = int(params[i])
        val = int(params[i+1])
        myGene.writeRegister(add,val)
    #           READ ALL REGISTERS AND SEND THE RESULTS TO JS
    myGene.getRegisters()
    ans = ""
    for k in range(len(myGene.ou)):
        ans += "%d %d "%(myGene.ou[k],myGene.vals[k])
    #BIDON CI-DESSOUS POUR TESTER ON ENVOIE UNE CHAINE CONVENUE:
    if False:
        ans = "101 %d 102 %d 104 %d 107 %d 110 %d 114 %d 127 %d 150 %d 151 %d 160 %d 161 %d 178 %d 179 %d 187 %d 188 %d 189 %d "%(
            0,      # 0 Ox65 101            Arret d'urgence 32639  led
            0x7F7F, # 1 Ox66 102            Defaut critique   768  led
            1020,   # 2 Ox68 104               Mesure debit     0  self.output
            1070,   # 3 Ox6b 107           Mesure puissance     0  output
            12,     # 4 Ox6e 110            Etat du procede     0  led
            123,    # 5 Ox72 114               Tension PFC      0  output
            12221,  # 6 Ox7f 127               Courant pont     0  output
            22,     # 7 Ox96 150     Puissance limite basse   600  input
            55,     # 8 Ox97 151     Puissance limite haute  1200  input
            76,     # 9 Oxa0 160                  Debit bas    28  input
            121,    #10 Oxa1 161                 Debit haut    62  input
            789,    #11 Oxb2 178         Consigne puissance   900  input
            45,     #12 Oxb3 179             Consigne debit    40  input
            0,    #13 Oxbb 187                 Generateur     0  button
            0x7F7F,      #14 Oxbc 188                        Gaz     0  button
            4)      #15 Oxbd 189                     Plasma     0  button

    # print("python says : I will return "+ans[:-1])
    return ans[:-1]; # suppression du ' ' final

def errorTreatement(input):
    global MyWindow
    print("errorTreatement entering with %s !"%input)
    MyWindow.script('alert("Lost connection");window.close();');
    exit(1)

myGene = geneControler(errorTreatement)#,simul=True)
connected = myGene.connect()

if connected != True:
    MyWindowErr = webui.window()
    MyWindowErr.bind("getError", getError )
    MyWindowErr.show("controlGeneWebuiError.html",webui.browser.firefox)
    webui.wait()
    exit(1)

MyWindow = webui.window()
MyWindow.show("controlGeneWebui.html",webui.browser.firefox)
MyWindow.bind("myFunction", myFunction) 
cpt = 0 # just to count the calls 
webui.wait()
# wrssdnuw_di
