import rsa
import aes
print("1 - Cifra em aes")
print("2 - Cifra em rsa")
op = input("Digite uma opção: ")
if(op == "1"):
    aes.run()
else:
    rsa.run()