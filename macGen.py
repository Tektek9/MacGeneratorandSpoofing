from generate_mac import generate_mac
import subprocess
from termcolor import colored
import regex as re
import string
import random
import wmi
import sys

lokasiiface = r"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}"
regexiface = re.compile("{.+}")
mac_address_regex = re.compile(r"([A-Z0-9]{2}[:-]){5}([A-Z0-9]{2})")

def gaweMacRandom():
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    return random.choice(uppercased_hexdigits) + random.choice("24AE") + "".join(random.sample(uppercased_hexdigits, k=10))

def nicBisadiModif():
    cek = subprocess.check_output("getmac /V").decode()
    filterlagi = [line for line in cek.split('\n') if "Media disconnected" not in line]
    for hasil in filterlagi:
        print(hasil)

def ngrijikiMac(mac):
    return "".join(c for c in mac if c in string.hexdigits).upper()  

def nyambungMac():
    nyambungadapterMac = []
    for targetMac in subprocess.check_output("getmac /V").decode().splitlines():
        mac_address = mac_address_regex.search(targetMac)
        transport_name = regexiface.search(targetMac)
        if mac_address and transport_name:
            nyambungadapterMac.append((mac_address.group(), transport_name.group()))
    return nyambungadapterMac

def milihAdapter(nyambungadapterMac):
    print("\nNo      Alamat Mac                Nama Transport")
    for i, option in enumerate(nyambungadapterMac):
        print(f"{i} : {option[0]}, {option[1]}")
    if len(nyambungadapterMac) <= 1:
        return nyambungadapterMac[0]
    try:
        choice = int(input(colored("Silahkan pilih interface yang mau diganti mac addressnya: ", "yellow")))
        return nyambungadapterMac[choice]
    except:
        print(colored("\nInputan gk jelas, program auto close ya :V\n", "red"))
        exit()

def gantiMac(adapter_transport_name, new_mac_address):
    output = subprocess.check_output(f"reg QUERY " +  lokasiiface.replace("\\\\", "\\")).decode()
    for interface in re.findall(rf"{lokasiiface}\\\d+", output):
        indexAdapter = int(interface.split("\\")[-1])
        interface_content = subprocess.check_output(f"reg QUERY {interface.strip()}").decode()
        if adapter_transport_name in interface_content:
            changing_mac_output = subprocess.check_output(f"reg add {interface} /v NetworkAddress /d {new_mac_address} /f").decode()
            print(changing_mac_output)
            break
    return indexAdapter

def disableAdapter(indexAdapter):
    disable_output = subprocess.check_output(f"wmic path win32_networkadapter where index={indexAdapter} call disable").decode()
    return disable_output

def enableAdapter(indexAdapter):
    enable_output = subprocess.check_output(f"wmic path win32_networkadapter where index={indexAdapter} call enable").decode()
    return enable_output

print(colored("\n/--Haram-Code-----------------------------------------\\","green"))
print(colored("|","green").ljust(11),end='')
print(colored("Mac Address Generator & Spoofing, by Kulionline0011 ","white").ljust(15),end='')
print(colored("|","green").ljust(15), end='')
print(colored("\n\-----------------------------------------Haram-Code--/","green"))

try:
    if len(sys.argv) < 2:
        print("Untuk bantuan: python3 macGen.py -h")
        print("               python3 macGen.py --help\n")
    elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("1. Tampilkan semua NIC")
        print("2. Tampilkan NIC yang bisa diganti mac addressnya")
        print("3. Buat mac address baru")
        print("4. Validasi mac address")
        print("5. Dapatkan VID mac address")
        print("6. Buat mac address berdasarkan VID")
        print("7. Spoofing manual")
        print("8. Spoofing otomatis")
    elif sys.argv[1] == "1":
        c = wmi.WMI()
        print("\n")
        listnic = c.Win32_NetworkAdapter()
        for nic in listnic:
            print(colored(f"NIC : {nic.Description}","green"))
            print(colored(f"MAC : {nic.MACAddress}","yellow"))
        print("\n")
    elif sys.argv[1] == "2":
        nicBisadiModif()
    elif sys.argv[1] == "3":
        wow = generate_mac.total_random()
        print(colored(f"\nMac Baru: {wow}\n","green"))
    elif sys.argv[1] == "4":
        b = str(input("Silahkan masukan mac address: "))
        wkwk = generate_mac.is_mac_address(b)
        t2kestrip = re.sub(r"-", ":", b)
        wkwk2 = generate_mac.is_mac_address(t2kestrip)
        if str(wkwk) == "True":
            print(colored("\nFormat Mac address valid\n","green"))
        elif str(wkwk2) == "True":
            print(colored("\nFormat Mac address valid\n","green"))
        else:
            print(colored(f"\nFormat Mac address tidak valid\n","red"))
    elif sys.argv[1] == "5":
        b = str(input("Silahkan masukan mac address: "))
        try:
            vid = generate_mac.get_vid_bytes(b)
            print(colored(f"\nVID Mac: {vid}\n","green"))
        except ValueError as ve:
            t2kestrip = re.sub(r"-", ":", b)
            vid = generate_mac.get_vid_bytes(t2kestrip)
            print(colored(f"\nVID Mac: {vid}\n","green"))
    elif sys.argv[1] == "6":
        c = str(input("Silahkan masukan VID mac address: "))
        try:
            newmac = generate_mac.vid_provided(c)
            print(colored(f"\nMac Baru: {newmac}\n","green"))
        except ValueError as ve:
            t2kestrip = re.sub(r"-", ":", c)
            newmac = generate_mac.vid_provided(t2kestrip)
            print(colored(f"\nMac Baru: {newmac}\n","green"))
    elif sys.argv[1] == "7":
        macbaru = str(input("Silahkan masukan mac baru: "))
        filterampuh = re.sub(r"[:\-]", "", macbaru)
        meknampilnotok = re.sub(r"[:\-]", "-", macbaru)
        nyambungadapterMac = nyambungMac()
        macLawas, jenengtargetTransport = milihAdapter(nyambungadapterMac)
        print(colored(f"\nMac address lama: {macLawas}\n", "red"))
        adapterIndex = gantiMac(jenengtargetTransport, filterampuh)
        print(colored(f"Mac address baru: {meknampilnotok}","green"))
        disableAdapter(adapterIndex)
        print("Disable adapter")
        enableAdapter(adapterIndex)
        print("Enable adapter\n")
    elif sys.argv[1] == "8":
        gaweMac = gaweMacRandom()
        nyambungadapterMac = nyambungMac()
        macLawas, jenengtargetTransport = milihAdapter(nyambungadapterMac)
        macAnyar = '-'.join(gaweMac[i:i+2] for i in range(0, len(gaweMac), 2))
        print(colored(f"\nMac address lama: {macLawas}\n", "red"))
        adapterIndex = gantiMac(jenengtargetTransport, gaweMac)
        print(colored(f"Mac address baru: {macAnyar}","green"))
        disableAdapter(adapterIndex)
        print("Disable adapter")
        enableAdapter(adapterIndex)
        print("Enable adapter\n")
    else:
        print("Inputan Gak jelas Blass :V")
except KeyboardInterrupt:
    print(colored("\n\nProgram close ya :V\n","yellow"))