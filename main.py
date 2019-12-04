ipv4="192.128.130.3"
mask="255.255.255.0"

#Função decimal para binário
def dec2bin(n):
    b = ''
    while n != 0:
        b = b + str(n % 2)
        n = int(n / 2)
    return b[::-1]
    
#Função que realiza a operação AND entre binário
def p_and(a,b):
  aux=[]
  for i in range(32):
    aux.append(int(a[i]) and (int(b[i])))
  return aux

#Função que realiza a operação OR entre binário
def p_or(a,b):
  aux=[]
  for i in range(32):
    aux.append(int(a[i]) or (int(b[i])))
  return aux
  
#Função que realiza a operação NOT entre binário
def p_not(a):
  aux=[]
  for i in range(32):
    aux.append(int(not(int(a[i]))))
  return aux

#substituir os pontos por vazio
repl=ipv4.replace('.',' ')

#Separa o IP e NETMASK em 4 octetos 
ip=ipv4.split(".")
netmask=mask.split(".")

for i in range(4):
  ip[i]=int(ip[i])
  netmask[i]=int(netmask[i])

doct1=dec2bin(ip[0]).zfill(8)
doct2=dec2bin(ip[1]).zfill(8)
doct3=dec2bin(ip[2]).zfill(8)
doct4=dec2bin(ip[3]).zfill(8)
moct1=dec2bin(netmask[0]).zfill(8)
moct2=dec2bin(netmask[1]).zfill(8)
moct3=dec2bin(netmask[2]).zfill(8)
moct4=dec2bin(netmask[3]).zfill(8)

#Concatenação dos 4 octetos do IP e da Mascara
ipconc=doct1+doct2+doct3+doct4
maskconc=moct1+moct2+moct3+moct4

#Calcula o IP da rede
def calcNetwork(ipBin,maskBin):
  ipRede=p_and(ipBin,maskBin)
  return ipRede

#Calcula o IP de Broadcast
def calcBroadcast(ipBin, maskBin):  
  ipBroadcast=p_not(p_and(p_not(ipBin), maskBin))
  return ipBroadcast

#adiciona ponto para separar os octetos
def addPonto(ip):
  ip.insert(8,".")
  ip.insert(17,".")
  ip.insert(26,".")
  return ip

#Adicionando pontos nos Ip's e calculando IP's de Rede e Broadcast
ipRede=addPonto(calcNetwork(ipconc, maskconc))
ipBroad=addPonto(calcBroadcast(ipconc, maskconc))



#Tranformar em decimal cada octeto
#teste=ipRede.split(".")
def bin2dec(a):
    n=0
    for d in a:
        n=n*2+d

    return n

string1=[]
for i in range(8):
  string1.append(ipRede[i])
valor=bin2dec(string1)
print(valor)

string2=[]
for i in range(8):
  string2.append(ipRede[i+9])
valor2=bin2dec(string2)
print(valor2)

string3=[]
for i in range(8):
  string3.append(ipRede[i+18])
valor3=bin2dec(string3)
print(valor3)

string4=[]
for i in range(8):
  string4.append(ipRede[i+27])
valor4=bin2dec(string4)
print(valor4)
