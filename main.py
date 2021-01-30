import json

conteudo=open('calculo.json').read()
dados=json.loads(conteudo)

ipv4=(dados['ipAddr'])
mask=(dados['netMask'])

#função decimal para binário
def dec2bin(n):
    b = ''
    while n != 0:
        b = b + str(n % 2)
        n = int(n / 2)
    return b[::-1]
    
#função binário para decimal  
def bin2dec(a):
    n=0
    for d in a:
        n=n*2+d

    return n

#função que realiza a operação AND entre binário
def p_and(a,b):
  aux=[]
  for i in range(32):
    aux.append(int(a[i]) and (int(b[i])))
  return aux

#função que realiza a operação OR entre binário
def p_or(a,b):
  aux=[]
  for i in range(32):
    aux.append(int(a[i]) or (int(b[i])))
  return aux
  
#função que realiza a operação NOT entre binário
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

#doct são os octetos do IP em binário e moct são os octetos da mascara em binário
ipbin1=dec2bin(ip[0]).zfill(8)
ipbin2=dec2bin(ip[1]).zfill(8)
ipbin3=dec2bin(ip[2]).zfill(8)
ipbin4=dec2bin(ip[3]).zfill(8)
maskbin1=dec2bin(netmask[0]).zfill(8)
maskbin2=dec2bin(netmask[1]).zfill(8)
maskbin3=dec2bin(netmask[2]).zfill(8)
maskbin4=dec2bin(netmask[3]).zfill(8)

#Concatenação dos 4 octetos do IP e da Mascara
ipconc=ipbin1+ipbin2+ipbin3+ipbin4
maskconc=maskbin1+maskbin2+maskbin3+maskbin4

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

#Adicionando pontos nos IPs e calculando IPs de Rede e Broadcast
ipRede=addPonto(calcNetwork(ipconc, maskconc))
ipBroad=addPonto(calcBroadcast(ipconc, maskconc))

#Tranforma em decimal cada octeto
ipRedeDec1=[]
ipBroadDec1=[]
for i in range(8):
  ipRedeDec1.append(ipRede[i])
  ipBroadDec1.append(ipBroad[i])
valorIp1=str(bin2dec(ipRedeDec1))
valorBroad1=str(bin2dec(ipBroadDec1))

ipRedeDec2=[]
ipBroadDec2=[]
for i in range(8):
  ipRedeDec2.append(ipRede[i+9])
  ipBroadDec2.append(ipBroad[i+9])
valorIp2=str(bin2dec(ipRedeDec2))
valorBroad2=str(bin2dec(ipBroadDec2))

ipRedeDec3=[]
ipBroadDec3=[]
for i in range(8):
  ipRedeDec3.append(ipRede[i+18])
  ipBroadDec3.append(ipBroad[i+18])
valorIp3=str(bin2dec(ipRedeDec3))
valorBroad3=str(bin2dec(ipBroadDec3))

ipRedeDec4=[]
ipBroadDec4=[]
for i in range(8):
  ipRedeDec4.append(ipRede[i+27])
  ipBroadDec4.append(ipBroad[i+27])
valorIp4=str(bin2dec(ipRedeDec4))
valorBroad4=str(bin2dec(ipBroadDec4))

#Juntar os octetos de IP e Broadcast
IP=(valorIp1+"."+valorIp2+"."+valorIp3+"."+valorIp4)
BROADCAST=(valorBroad1+"."+valorBroad2+"."+valorBroad3+"."+valorBroad4)

#classe do IP
def classe(valorIp1):
  classe=[]
  valorIp1=int(valorIp1)
  if valorIp1>=0 and valorIp1 < 127:
    classe="A"
  elif valorIp1 > 127 and valorIp1 < 192:
    classe="B"
  elif valorIp1 > 192 and valorIp1 <240:
    classe="D (Multicasting)"
  else:
    classe="E (Uso Futuro)"
  return classe

#verifica se o IP é válido
def verificaIP(ip):
  status=[]
  for i in range(4):
    if int(ip[i]) < 0 or int(ip[i]) > 255:
      status="inválido"
      return status
    else:
      status="válido"
  return status

#verifica se a máscara é válida
def verificaMask(maskconc, netmask):
  a=0
  status=[]
  status=verificaIP(netmask)
  if(status=="inválida"):
    return status
  else:
    for i in range(31):
      if maskconc[i]=="0" and maskconc[i+1]=="1":
        a+=1
      if a>0:
        status="inválida"
      else:
        status="válida"
    return status

#conta a quantidade HostId da máscara
def qntBitsHost(maskconc, netmask):
  bitsHost=0
  res=[]
  if((verificaMask(maskconc, netmask))=="inválida"):
    res="A máscara é inválida"
    return res
  else:
    for i in range(32):
      if(maskconc[i]=="0"):
        bitsHost=bitsHost+1       
    return bitsHost

#conta a quantidade de NetIda da máscara
def qntBitsRede(maskconc, netmask):
  bitsRede=32
  res=[]
  if((verificaMask(maskconc, netmask))=="inválida"):
    res="A máscara é inválida"
    return res
  else:
    for i in range(32):
      if(maskconc[i]=="0"):
        bitsRede=bitsRede-1        
    return bitsRede

#faixa de IP
def faixa(ipRede, ipBroad):
  ipFaixaU=[]
  ipFaixaL=[]
  faixa=[]
  for i in range(27,35):
    ipFaixaU.append(ipBroad[i])
    ipFaixaL.append(ipRede[i])
  
  ipmax=bin2dec(ipFaixaU)
  ipmin=bin2dec(ipFaixaL)
  MAXtemp=str(ipmax-1)
  MINtemp=str(ipmin+1)

  min1=[]
  max1=[]
  min2=[]
  max2=[]
  min3=[]
  max3=[]

  for i in range(8):
    min1.append(ipRede[i])
    max1.append(ipBroad[i])
    min2.append(ipRede[i+9])
    max2.append(ipBroad[i+9])
    min3.append(ipRede[i+18])
    max3.append(ipBroad[i+18])

  min1=str(bin2dec(min1))
  max1=str(bin2dec(max2))
  min2=str(bin2dec(min2))
  max2=str(bin2dec(max2))
  min3=str(bin2dec(min3))
  max3=str(bin2dec(max3))

  MIN=(min1+"."+min2+"."+min3+"."+MINtemp)
  MAX=(max1+"."+max2+"."+max3+"."+MAXtemp)

  faixa=(MIN+" / "+MAX)
  return faixa

#verifica se o IP é reservado
def ipreservado(ipv4):
  status=[]
  if ipv4>="0.0.0.0" and ipv4<="0.255.255.255":
    status="reservado"
  elif ipv4>="127.0.0.0" and ipv4<="127.255.255.255":
    status="reservado"
  elif ipv4>="10.0.0.0" and ipv4<="10.255.255.255":
    status="reservado"
  elif ipv4>="172.16.0.0" and ipv4<="172.31.255.255":
    status="reservado"
  elif ipv4>="192.168.0.0" and ipv4<="192.168.255.255":
    status="reservado"
  else:
    status="não reservado"  
  return status

#retorna a quantidade de hosts possiveis na rede
def qntHost(bitsHost):
  qntHost=(2**bitsHost)-2
  return qntHost

#Valores a serem mostrados
#print("O IP é:",verificaIP(ip))
validezIP=verificaIP(ip)

#print("A Máscara é:",verificaMask(maskconc, netmask))
validezMascara=verificaMask(maskconc, netmask)

#mostra os atributos
def mostraAtributos():
  print("O IP é:",verificaIP(ip))
  validezIP=verificaIP(ip)
  
  print("A Máscara é:",verificaMask(maskconc, netmask))
  validezMascara=verificaMask(maskconc, netmask)

  print("O IP é:",ipreservado(ipv4))
  ipStatus=ipreservado(ipv4)

  print("IP de Rede:",IP)
  redeIp=IP

  print("IP de Broadcast:",BROADCAST)
  broadcastIp=BROADCAST

  print("Classe do IP: ",classe(valorIp1))
  classeIp=classe(valorIp1)

  print("Bits de Rede da Máscara:",qntBitsRede(maskconc, netmask))
  redebits=qntBitsRede(maskconc, netmask)

  print("Bits de Host da Máscara:",qntBitsHost(maskconc, netmask))
  hostbits=qntBitsHost(maskconc, netmask)

  bitsHost=qntHost(qntBitsHost(maskconc, netmask))
  print("Quantidade de hosts na rede:",bitsHost)

  faixavalida=faixa(ipRede,ipBroad)
  FaixaResposta=("Faixa de máquinas válidas: "+faixavalida)
  
  escreverNoArquivo(validezIP,validezMascara,ipStatus,redeIp,broadcastIp,classeIp,redebits,hostbits,bitsHost,faixavalida)
  return FaixaResposta

def escreverNoArquivo(validezIP,validezMascara,ipStatus,redeIp,broadcastIp,classeIp,redebits,hostbits,bitsHost,faixavalida):
  
  with open('saida.json', 'w') as outfile:
    outfile.write("{\n\tO IP é: "+str(validezIP)+",")
    outfile.write("\n\tA máscara é: "+str(validezMascara)+",")
    outfile.write("\n\tO IP é: "+str(ipStatus)+",")
    outfile.write("\n\tIP da Rede: "+str(redeIp)+",")
    outfile.write("\n\tIP de Broadcast: "+str(broadcastIp)+",")
    outfile.write("\n\tClasse do IP: "+str(classeIp)+",")
    outfile.write("\n\tBits de Rede da Máscara: "+str(redebits)+",")
    outfile.write("\n\tBits de Host da Máscara: "+str(hostbits)+",")
    outfile.write("\n\tQuantidade de hosts na rede: "+str(bitsHost)+",")
    outfile.write("\n\tFaixa de máquinas válidas: "+str(faixavalida+"\n}"))

def main():
  print(mostraAtributos())  

if __name__ == "__main__":
  main()