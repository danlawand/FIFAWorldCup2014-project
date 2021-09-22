fhand = open("arti.txt","r")

i = 0
golos = 0
nomes = dict()
for line in fhand:
    texto = line.strip()
    if len(texto) > 0:
        nomes[texto] = nomes.get(texto, 0) + 1

soma = 0
for autor, q in nomes.items():
    n_spaces = 20 - len(autor)
    print(autor + ' '*n_spaces + str(q))
fhand.close()