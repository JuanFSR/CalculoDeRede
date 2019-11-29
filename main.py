ipv4="256.192.10.1"
mask="10.52.75.2"

ip=ipv4.split(".")
for i in range(4):
  ip[i]=int(ip[i])

doct1=ip[0]
doct2=ip[1]
doct3=ip[2]
doct4=ip[3]

netmask = mask.split(".")
for i in range(4):
  netmask[i]=int(netmask[i])

moct1=netmask[0]
moct2=netmask[1]
moct3=netmask[2]
moct4=netmask[3]

def dec2bin(n):
    b = ''
    while n != 0:
        b = b + str(n % 2)
        n = int(n / 2)
    return b[::-1]