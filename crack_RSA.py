 #!/usr/bin/python

 #Author:Giuseppe Festa

#try to get all kays with shared primes 

from Crypto.PublicKey import RSA
import os
from collections import OrderedDict




def GCD(x, y): 
  
   while(y): 
       x, y = y, x % y 
  
   return x 

def egcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0


def save(key, fname):
    with open(fname, 'wb') as f:
        f.write(key.exportKey())


def create_corr_file():
	a=0
	for nm in ast.keys():
		filelist.append("")
		for cn in  ast.keys():
			if GCD(ast[nm],ast[cn]) != 1:
				filelist[a]=filelist[a]+" "+cn.replace("\n","")
		filelist[a]=filelist[a]+'\n'
		a=a+1

	cop.writelines(filelist)
	cop.close()

def create_corr():
	corr=[]
	for i in range(len(names)):
		corr.append([])
	a=0
	print len(n)
	for k in n:
		corr[a].append(k)
		for cor in n:
			if k != cor:
				if GCD(k,cor)!=1:
					corr[a].append(cor)
		print len(corr[a])			
		a=a+1		

	print len(corr)
	return corr

def load(what, dir):
	with open(dir,'w') as lol:
		lol.write(what)

def mkdir(name):
	try:	
		os.mkdir(name, 0o755)
	except:
		pass

def extract(cor):
	firstprime=GCD(cor[0],cor[1])
	secondprime=cor[0]/firstprime
	return firstprime,secondprime

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


mkdir('new')
mkdir('privkeys')
pubdir="pubkeys/{}.pem"
names=open("users.txt",'r').readlines()
cop=open('cop.txt','w+')

n=[]
ast=OrderedDict()
a=0
for name in names:
	work=pubdir.format(name.replace('\n',""))
	filekey=open(work,'r')
	key=RSA.importKey(filekey)
	ast[name]=key.n
	n.append(key.n)
	a=a+1

print ast
filelist=[]
create_corr_file()

co=create_corr()
for i in range (len(names)):
	try:
		p,q=extract(co[i])
		e = 0x10001
		d = modinv(e, (p-1)*(q-1))
		key = RSA.construct((n[i], long(e), d))
		
	except:
		print "jumped"

	save(key, 'privkeys/{}.pem'.format(names[i].replace('\n',"")))
	with open('messages/{}.enc'.format(names[i].replace('\n',"")),'r') as f:
			dec=key.decrypt(f.read())
			load(dec,'new/{}.txt'.format(names[i].replace('\n',"")))
		