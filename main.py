import rsa
import aes
import sign
print("1 - Cifra em aes")
print("2 - Cifra em rsa")
print("3 - Assinatura")
op = input("Digite uma opção: ")
if(op == "1"):
    aes.run()
elif(op == "2"):
    rsa.run()
else:
    sign.run()