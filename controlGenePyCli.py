#!/usr/bin/env python
import serial
import minimalmodbus
import serial.tools.list_ports as port_list
import time,sys
"""
                                 WITH A POLLING WATCHDOG (NO THREAD OR RACE)
class geneControler : can connect and read/write registers, also it has a mode simulation
at initialization one can provide, or not, a function to treat the error,
connect: if *exactly* one port connected to a board is found the connection is established at BAUD,'N',8,1, TIMEOUT to SLAVE
         else (ie no port  at all, no port connected or more thanone) no connection is performed
         In all case the variable messageConction is set.
read/write : if the timeout is exceeded then an error code is returned (1: write, 2: read) and the connected becomes false

An infinite loop tests the keyboard in a NON blocking way therefore the loop is short.
At each beginning of the loop the current time is compared to the time of the last test of the connection.
If the last test is too old a new test is performed.

SIMULATION MODE
fake values are initialized at pseudo-connect with fixed values (see the connect() method)
Every second (see line 272 threading.Timer(1,...)) the output values (power 0x6b, flow 0x68,
current 0x7f tension 0x72) are randomly modified inside the admissible range.
Moreover with probability 1/100 (see ) a critical default (0x65) and  emergency stop (0x65)
are set.
"""

TIMEOUT = 0.1 # for reading/writing register a real number in secondes 
BAUD = 9600
SLAVE = 3
ALIVE_ADDRESS = 205
ALIVE_VALUE = 303
WATCHDOGTIMESEC = 1  # a float in second, a new test is made is 

class geneControler:
    ou = []
    quoi = []
    index= dict()
    vals = []
    types = [] # "led", "button", "output", "input"
    addToIndex = {}
    instrument = "";
    connected = False;
    messageConnection = "";
    simul = False;
    def __init__(self,myFun="",simul=False):
        self.errorTreat = myFun;
        
        self.simul = simul;

        self.quoi.append("Arret d'urgence");
        self.ou.append(0x65);
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.index["Arret d'urgence"] = len(self.ou)-1;
        self.vals.append(-1)
        self.types.append("led")

        self.quoi.append("Defaut critique");
        self.ou.append(0x66);
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.index["Defaut critique"] = len(self.ou)-1;
        self.vals.append(-1)
        self.types.append("led")

        self.quoi.append("Mesure debit");
        self.ou.append(0x68);
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.index["Mesure debit"] = len(self.ou)-1;
        self.vals.append(-1)
        self.types.append("output")

        self.quoi.append("Mesure puissance");
        self.ou.append(0x6B);
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.index["Mesure puissance"] = len(self.ou)-1;
        self.vals.append(-1)
        self.types.append("output")

        self.quoi.append("Etat du procede");
        self.ou.append(0x6E);
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.index["Etat du procede"] = len(self.ou)-1;
        self.vals.append(-1)
        self.types.append("led")

        self.quoi.append("Tension PFC ");
        self.ou.append(0x72);
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.index["Tension PFC "] = len(self.ou)-1;
        self.vals.append(-1)
        self.types.append("output")

        self.quoi.append("Courant pont");
        self.ou.append(0x7F);
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.index["Courant pont"] = len(self.ou)-1;
        self.vals.append(-1)
        self.types.append("output")

        self.quoi.append("Puissance limite basse");
        self.ou.append(0x96);
        self.index["Puissance limite basse"] = len(self.ou)-1;
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.vals.append(-1)
        self.types.append("input")

        self.quoi.append("Puissance limite haute");
        self.ou.append(0x97);
        self.index["Puissance limite haute"] = len(self.ou)-1;
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.vals.append(-1)
        self.types.append("input")

        self.quoi.append("Debit bas");
        self.ou.append(0xA0);
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.index["Debit bas"] = len(self.ou)-1;
        self.vals.append(-1)
        self.types.append("input")

        self.quoi.append("Debit haut");
        self.ou.append(0xA1);
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.index["Debit haut"] = len(self.ou)-1;
        self.vals.append(-1)
        self.types.append("input")

        self.quoi.append("Consigne puissance");
        self.ou.append(0xB2);
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.index["Consigne puissance"] = len(self.ou)-1;
        self.vals.append(-1)
        self.types.append("input")

        self.quoi.append("Consigne debit");
        self.ou.append(0xB3);
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.index["Consigne debit"] = len(self.ou)-1;
        self.vals.append(-1)
        self.types.append("input")

        self.quoi.append("Generateur");
        self.ou.append(0xBB);
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.index["Generateur"] = len(self.ou)-1;
        self.vals.append(-1)
        self.types.append("button")

        self.quoi.append("Gaz");
        self.ou.append(0xBC);
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.index["Gaz"] = len(self.ou)-1;
        self.vals.append(-1)
        self.types.append("button")

        self.quoi.append("Plasma");
        self.ou.append(0xBD);
        self.addToIndex[self.ou[-1]] = len(self.ou)- 1;
        self.index["Plasma"] = len(self.ou)-1;
        self.vals.append(-1)
        self.types.append("button")
        # FIN __init__()
    # ################################################################################

    def __del__(self):
        if self.connected and self.simul:
            self.threadSimul.cancel()
    
    def getRegisters(self):
        """
        set vals and return a string ready to be printed
        if a reading fails an empty string is return instead
        """
        ans = ""
        ok = 1
        for i in range(len(self.ou)):
            v = self.readRegister(self.ou[i])
            self.vals[i] = v
            ans += "%2d Ox%x %3d %26s %5d  %s\n"%(i,self.ou[i],self.ou[i],self.quoi[i],self.vals[i],self.types[i])
        return ans
    # FIN def getRegisters(self):
    # ################################################################################

    def isAlive(self):
        if self.simul:
            return True
        ans = self.readRegister(ALIVE_ADDRESS)
        return ans==ALIVE_VALUE
    # FIN def isAlive():
    # ################################################################################

    def writeRegister(self,add,value):
        """
        call errorTreat or exit if can't write
        """
        # print(f"entering writeRegister {add}")
        if self.simul:
            self.fakeValues[self.addToIndex[add]] = value;
            return ;
        readingPossible = False
        ok = 1
        try:
            self.instrument.write_register(add,value)
        except :
            sys.stdout.writelines("writeRegister: Could not write register at 0x%x = %d\n"%(add,add))
            sys.stdout.flush()
            ok = 0
        if not ok:
            connected = False
            if self.errorTreat!= "":
                self.errorTreat(1)
            else:
                exit(1) # write error
        #print(f"leaving writeRegister {add}")
    # FIN def writeRegister(add,value):
    # ################################################################################

    def readRegister(self,add):
        """
        return the int value read, exit if can't read
        """
        if self.simul:
            k = self.addToIndex[add]
            return self.fakeValues[k];
        # print(f"entering readRegister L230 {add}");
        readingPossible = False    
        ok = 1
        ans = [-1]
        try:
            ans = self.instrument.read_registers(add,1)
        except :
            ok = 0
        if not ok:
            self.connected = False
            if self.errorTreat!= "":
                self.errorTreat(2)
            else:
                exit(2) #read error
        # print(f"leaving readRegister {add}")
        return ans[0]
    # FIN  def readRegister(add)
    # ################################################################################

    def connect(self):
        """
        connect the instrument
        return True if ok
               a string describing the error else
        """
        self.fakeValues = []
        if self.simul:
            import random,threading
            def fakeLife():
                add = 0x65 # emergency stop
                k = self.addToIndex[add]
                self.fakeValues[k] == 0x7f7f if random.randint(0,99)==0 else 0
                add = 0x66 # defaut critique
                k = self.addToIndex[add]
                self.fakeValues[k] == 0x7f7f if random.randint(0,99)==0 else 0
                add=0x6b # power
                k = self.addToIndex[add]
                self.fakeValues[k] += random.randint(-1,1)
                if self.fakeValues[k] > self.fakeValues[self.addToIndex[0x97]]:
                    self.fakeValues[k] = self.fakeValues[self.addToIndex[0x97]]
                if self.fakeValues[k] < self.fakeValues[self.addToIndex[0x96]]:
                    self.fakeValues[k] = self.fakeValues[self.addToIndex[0x96]]
                add=0x68 # flow
                k = self.addToIndex[add]
                self.fakeValues[k] += random.randint(-1,1)
                if self.fakeValues[k] > self.fakeValues[self.addToIndex[0xA1]]:
                    self.fakeValues[k] = self.fakeValues[self.addToIndex[0xA1]]
                if self.fakeValues[k] < self.fakeValues[self.addToIndex[0xA0]]:
                    self.fakeValues[k] = self.fakeValues[self.addToIndex[0xA0]]
                add=0x7f #bridge current
                k = self.addToIndex[add]
                self.fakeValues[k] += random.randint(-1,1)
                add=0x72 #tension
                k = self.addToIndex[add]
                self.fakeValues[k] += random.randint(-1,1)
                self.threadSimul = threading.Timer(1,fakeLife) # relance apre 1 sec
                if self.connected:
                    self.threadSimul.start()
            # FIN fakeLife
            self.fakeValues.append(0)   #  arret d'urgence
            self.fakeValues.append(0)   #  defaut cririque
            self.fakeValues.append(10)  #  Mesure debit
            self.fakeValues.append(100) #  Mesure puissance
            self.fakeValues.append(0)   #  Etat du procede
            self.fakeValues.append(20)  #  Tension PFC
            self.fakeValues.append(200) #  Courant pont
            self.fakeValues.append(80)  #  Puissance limite basse
            self.fakeValues.append(120) #  Puissance limite haut
            self.fakeValues.append(5)   #  Debit bas
            self.fakeValues.append(15)  #  Debit haut
            self.fakeValues.append(100) #  Consigne puissance
            self.fakeValues.append(10)  #  Consigne debit
            self.fakeValues.append(0)   #  Generateur
            self.fakeValues.append(0)   #  Gaz
            self.fakeValues.append(0)   #  Plasma
            self.connected = True
            self.messageConnection = "simulation"
            fakeLife()
            # foo()
            return True
        # from here this not a simulation 
        ports = list(port_list.comports())
        # choice of the port to use
        if self.simul:
            self.connectSimul()
            return True
        if len(ports)==0:
             self.messageConnection = "No serial port available"
             self.connected = False
             return False
        lesInstruments = [] # instruments that can be used
        for k,port in enumerate(ports): # try to use all listed ports
            ser = serial.Serial(port.device)
            ser.timeout = TIMEOUT # seconds
            instrument = minimalmodbus.Instrument(ser, SLAVE)
            instrument.serial.baudrate = BAUD
            instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
            instrument.mode = 'rtu'
            # instrument.debug = True
            instrument.timeout = ser.timeout
            try:
                ans = instrument.read_registers(ALIVE_ADDRESS,1)
                lesInstruments.append(instrument)        
            except :
                pass
            ser.close()
        if len(lesInstruments)==0:
            self.messageConnection = "The generator is not connected, altough some serial ports are availables"
            self.connected = False
            return False
        if len(lesInstruments)>1 :
            msg = "%d port connected to a generator, please plug *only* the desired one"%(len(lesInstruments))
            self.messageConnection = msg
            self.connected = False
            return False

        # use the port with index 0
        port = ports[0]
        ser = serial.Serial(port.device)
        ser.timeout = TIMEOUT # seconds
        self.instrument = minimalmodbus.Instrument(ser, SLAVE)
        self.instrument.serial.baudrate = BAUD
        self.instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.instrument.mode = 'rtu'
        self.instrument.timeout = ser.timeout
        # self.instrument.debug = True
        msg = "using %s at %d baud parity %c\n"%(self.instrument.serial.name,self.instrument.serial.baudrate,self.instrument.serial.parity)
        self.messageConnection = msg
        self.connected = True
        return True
    # FIN connect(self)

    def test(self,nTest):
        """
        nTest est la liste du nombre de test souhaite pour le registre d'adresse ou[i]
        """
        import random
        for i,n in enumerate(nTest):
            if n==0:
                continue
            add = self.ou[i]
            S = set()
            for c in range(n):
                val = random.randint(1,32767)
                self.writeRegister(add,val)
                relu = self.readRegister(add)
                dif = relu-val
                S.add(dif)
            print(add,n,S)
    # FIN test(self)
            
# FIN class geneControler
# ***********************************************************************************

# ***********************************************************************************
#                                            EN AVANT SIMONE
# ***********************************************************************************
if __name__ == '__main__':
    import msvcrt
    
    class nonBlockingString:
        """
        Cette classe permet une lecture NON bloquente du clavier.
        La chaine se termine par '\\n' ou '\\r', elle n'est retournee
        par getKbd() que lorsqu'elle est complete, sinon None est retourne
        """
        def __init__(self):
            self.str = ""
        def getKbd(self):
            """
            retourne la chaine si elle est complete (finie par \\n ou \\r) None sinon
            """
            if msvcrt.kbhit():
                self.car = msvcrt.getche()
                self.str += self.car.decode()
                if self.car == b'\r' or self.car == b'\n':
                    aux = self.str
                    self.str = ""
                    return aux
    # FIN class nonBlockingString:
    # ***********************************************************************************
    
    def myFun(p):
        """
        function called in case of error, with the parameter p:
        p=1 write error timeouut
        p=2 read error timeout
        p=3 no serial port
        p=4 not alive (ie bad reading by the watchDog)
        """
        print(f"oops j'ai recu la valeur {p}")
        exit(p)
    # FIN myFun(p)
    # ***********************************************************************************
    print("\nRun in simulation mode if called with any argument\n\n")
    myGene = geneControler( simul=len(sys.argv) == 2 )
    ans = myGene.connect()
    if not ans:
        print(myGene.messageConnection)
        exit(1)
    mySt = nonBlockingString() # pour faire une lecture non bloquante du clavier
    somethingNew = True
    lastCheckAlive = 0
    cpt = 0
    while True:
        time.sleep(0.1)
        cpt += 1
        currentTime = time.time()
        if currentTime - lastCheckAlive > WATCHDOGTIMESEC:
            lastCheckAlive = currentTime
            if not myGene.isAlive():
                sys.stdout.writelines("The connection is down !")
                sys.stdout.flush()
                break
        if somethingNew:
            somethingNew = False
            ans = myGene.getRegisters()
            sys.stdout.writelines(ans)
            sys.stdout.writelines("\nenter the register number and the value to set, or q for quit,or 'return' to see current values : ")
            sys.stdout.flush()
        # ans = input("entrer le numéro du registre et la valeur a y mettre, ou q pour quitter ")
        ans = mySt.getKbd()
        if ans==None:
            continue
        somethingNew = True
        sys.stdout.writelines("\n")
        sys.stdout.flush()
        if ans=='q\r':
            break
        ans = ans.split()
        if len(ans)!=2:
            continue
        try:
            ans = list(map(int,ans))
        except:
            continue
        o,q = ans
        sys.stdout.writelines("\n")
        sys.stdout.flush()
        if o<0 or o>=len(myGene.ou):
            sys.stdout.writelines("%d is not the index of a register\n"%o)
            sys.stdout.flush()
            continue
        if q<0 or q>=65536:
            sys.stdout.writelines("the value %d is out of bonds\n"%q)
            sys.stdout.flush()
            continue
        myGene.vals[o] = q
        myGene.writeRegister(myGene.ou[o],q)
    myGene.__del__()
    print("la fonction testRW(myGene) est disponible")
    
    def testRW(myGene):
        n = len(myGene.vals)
        for i in range(16):
            a = myGene.readRegister(myGene.ou[i])
            b = random.randint(0,32767)
            myGene.writeRegister(myGene.ou[i],b)
            c =  myGene.readRegister(myGene.ou[i])
            add = myGene.ou[i]
            quoi = myGene.quoi[i]
            print("En 0x%2x il y avait 0x%04x, je vais mettre 0x%04x, j'ai relu 0x%04x  %s"%(add,a,b,c,quoi))
        
