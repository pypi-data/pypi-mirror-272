from ipaddress import ip_address
import subprocess
def validip(ip:str):
        validip = str(ip_address(ip))
        return validip

def paraPing(ip: str) -> bool:
    validip = validip(ip)
    result = str(subprocess.run(['ping', '-c', '3', '-n', validip],stdout = subprocess.DEVNULL))
    output = result.find("0% packet loss")
    if output:
        return True
    else:
        return False