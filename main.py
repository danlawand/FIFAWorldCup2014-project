import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
import time

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter URL: ')
if (len(url) < 1): url = 'https://openfootball.github.io/'

f = open("cupdb.txt", "w")

html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')
print('Retrieving:', url)

tags = soup('a')
for tag in tags:
    try:
        url = tag.get('href', None)
    except:
        continue
    if url == 'https://github.com/openfootball/world-cup/blob/master/2014--brazil/cup.txt':
        break;

fhand = urllib.request.urlopen(url)
codigo = list()
matchDay = dict()
info = list()
partida = dict()
autoresGols = dict()
golsContra = dict()
golsPenaltis = dict()
i = 0
golos = 0
for line in fhand:
    linha = line.decode().strip()
    texto = re.findall('<td id="LC.+">(.*)</td>', linha)

    if len(texto) > 0:
        codigo.append(texto[0])
        l = codigo[i]
        l = l.lstrip()
        l = l.replace('&#39;', "'")
        l = re.sub('[(]UTC-.[)]','', l)
        l = re.sub('[(].-.[)] ','', l)
        l = re.sub('[á-å]', 'a', l)
        l = re.sub('[çć]', 'c', l)
        l = re.sub('[é-ë]', 'e', l)
        l = re.sub('[í-ï]', 'i', l)
        l = re.sub('[ó-õö]', 'o', l)
        l = re.sub('[ú-ü]', 'u', l)
        l = re.sub('ñ', 'n', l)
        l = re.sub('[ÄÅ]', 'A', l)
        l = re.sub('Ç', 'C', l)
        l = re.sub('É', 'E', l)
        l = re.sub('Ñ', 'N', l)
        l = re.sub('Ö', 'O', l)
        l = re.sub('Ü', 'U', l)
        l = re.sub('ž', 'z', l)
        l = re.sub('Ž', 'Z', l)
        l = re.sub('š', 's', l)
        l = re.sub('Š', 'S', l)

        mDay = re.findall('[M][atchday]+\s[0-9]+\s+\|\s+[A-z0-9\/\s]+\r', l)
        if len(mDay) > 0:
            vamo = mDay[0].split('|')
            vamo[1] = vamo[1].replace('\r', '')
            matchDay[vamo[1].lstrip()] = vamo[0].rstrip()

        nPartida = re.findall('\(([0-9]+)\).+', l)
        if len(nPartida) > 0:
            info.append(nPartida[0])
            l = re.sub('\(([0-9]+)\) ', nPartida[0]+'\n', l)

        dataPartida = re.findall('([A-Z][a-z][a-z]\s[A-Z][a-z][a-z]/[0-9][0-9]\s[0-9][0-9]:[0-9][0-9])', l)
        if len(dataPartida) > 0:
            dSemana = re.findall('\s+([A-Z][a-z][a-z] [A-Z][a-z][a-z]/[0-9][0-9])\s', l)
            if dSemana[0] in matchDay:
                info.append(matchDay[dSemana[0]])
            info.append(dataPartida[0])
            l = re.sub('\s+[A-Z][a-z][a-z] [A-Z][a-z][a-z]/[0-9][0-9] [0-9][0-9]:[0-9][0-9]', '\n'+dataPartida[0]+'\n&', l)
            l = re.sub('&\s+', '', l)

        jogo = re.findall('(.+)@', l)
        if len(jogo) > 0:
            jogo[0] = jogo[0].strip()
            placar = re.findall('([0-9]+-[0-9]+)', jogo[0])
            adversario1 = re.findall('(.+)\s[0-9]+', jogo[0])
            adversario2 = re.findall('[0-9]\s(.+)', jogo[0])
            info.append(placar[0])
            info.append(adversario1[0])
            info.append(adversario2 [0])

        estadio = re.findall('@ (.+)\s\r', l)
        if len(estadio) > 0:
            estadio[0].rstrip()
            info.append(estadio[0])
        l = re.sub('[@] ', '\n', l)



        autorGol = re.findall("[;[\s']+([A-z\s]+)\s*[0-9\+\s]+'", l)
        if len(autorGol) > 0:
            for autor in autorGol:
                autor = autor.strip()
                gols = re.findall(autor+"([^A-Z\];]+)", l)
                if len(gols) > 0:
                    for gol in gols:
                        gol = gol.strip()
                        score = gol.split(',')
                        for sc in score:
                            sc = sc.strip()
                            if sc == '':
                                continue
                            contra = re.findall("(\(o\.g\.\))+", sc)
                            if len(contra) > 0:
                                golsContra[autor] = golsContra.get(autor, 0) + 1
                                continue
                            penalidade = re.findall("(\(pen\.\))+", sc)
                            if len(penalidade) > 0:
                                golsPenaltis[autor] = golsPenaltis.get(autor, 0) + 1
                                autoresGols[autor] = autoresGols.get(autor, 0) + 1
                                continue
                            autoresGols[autor] = autoresGols.get(autor, 0) + 1

        l = l+'\n'
        f.write(l)
        i = i + 1
soma = 0
for autor, gol in autoresGols.items():
    soma = soma + int(gol)
for autor, gol in golsContra.items():
    soma = soma + int(gol)

j = 0
for item in info:
    if j%7 == 0:
        partida[item] = info[j:j+7]
    j = j + 1
for key, item in partida.items():
    print(key, item)
    print()
f.write('\n\n')

f.write('---- ARTILHEIROS ----\n')
sort_autores = sorted(autoresGols.items(), key=lambda x: x[1], reverse=True)
for items in sort_autores:
    n_spaces = 20 - len(items[0])
    f.write(items[0] + ' '*n_spaces + str(items[1]))
    f.write('\n')
f.write('\n\n')

f.write('---- GOLS CONTRA ----\n')
sort_golsContra = sorted(golsContra.items(), key=lambda x: x[1], reverse=True)
for items in sort_golsContra:
    n_spaces = 20 - len(items[0])
    f.write(items[0] + ' '*n_spaces + str(items[1]))
    f.write('\n')
f.close()
