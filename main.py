#[Rastreador; Estación Espacial Internacional (ISS)].
import os
import sys
import json
import time
import urllib.request
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, TextArea

#[Corpus; Importación de archivos].
#(A):
mapa_mundi = os.path.join('imgs', 'mundi.jpg')
mundi_ = plt.imread(mapa_mundi)
#(B):
iss_log = os.path.join('imgs', 'iss_log.png')
log_ = plt.imread(iss_log)

#[Corpus; Ubicación anterior].
pHistory = []

#[Corpus; Configuración de latitudes y longitudes].
longMin = -180
longMax = 180
latMin = -90
latMax = 90

#[Corpus; BBOX].
bbox = (longMin, longMax, latMin, latMax)

#[Corpus; Factor de escala].
fS = 5

#[Corpus; Configuración de alto/ancho en mapa].
Alto = abs(latMax - latMin) / fS
Ancho = abs(longMax - longMin) / fS

zm = 0.1

#[Corpus; Creación de funciones].
def func_main():
    url = 'http://api.open-notify.org/iss-now.json'

    response = urllib.request.urlopen(url)
    result = json.loads(response.read())

    location = result['iss_position']
    latitude = location['latitude']
    longitude = location['longitude']
    timestamp = result['timestamp']

    return ((float(longitude), float(latitude)), timestamp)

#[Corpus; Vacío].
fig, ax = plt.subplots(figsize=(Ancho, Alto))

#[Corpus; Personalización].
ax.set_xlim(longMin, longMax)
ax.set_ylim(latMin, latMax)
ax.set_xlabel('Longitudes')
ax.set_ylabel('Latitudes')
ax.grid(True)

#[Corpus; Creación de marcas].
longi_li = list(range(longMin, longMax+1, 20))
lati_li = list(range(latMin, latMax+1, 30))

def append_deg(x, neg, pos):
    if x < 0:
        return str(abs(x)) + u"\u00b0" + neg
    elif x > 0:
        return str(x) + u"\u00b0" + pos
    else:
        return str(x) + u"\u00b0"
longi_li = list(map(lambda x: append_deg(x, 'W', 'E'), longi_li))
lati_li = list(map(lambda x: append_deg(x, 'S', 'N'), lati_li))

#[Corpus; Configuración de ejes].
plt.xticks(ticks=list(range(longMin, longMax+1, 20)), labels = longi_li)
plt.yticks(ticks=list(range(latMin, latMax+1, 30)), labels = lati_li)

ax.imshow(mundi_, alpha=0.65, extent = bbox)

#[Corpus; ISS Logo].
im = OffsetImage(log_, zoom=zm)
fig_num = fig.number

start_time = None
while True:
    try:
        pt, t = func_main()
    except Exception as e:
        print('[API Error; Detectado].')
        print(e)
        input('Presionar cualquier tecla para salir...')
        sys.exit()


    if start_time is None:
        start_time = t

    pHistory.append(pt)

    #[subCorpus; Escritura de tiempo en consola].
    print(f'Fecha: {time.ctime(t)}\tLatitud: {pt[1]}\tLongitud: {pt[0]}')

    #[subCorpus; Título].
    ax.set_title('Mapa mundial\n'+'(Fecha de inicio: '+time.ctime(start_time)+')\n\nFecha y hora de ubicación de Estación Espacial Internacional: '+time.ctime(t))

    #[subCorpus; ISS].
    ab = AnnotationBbox(im, pt, xycoords='data', frameon=False)
    ax.add_artist(ab)

    #[subCorpus; Latitud y longitud].
    tx = TextArea(f"({append_deg(pt[0], 'W', 'E')}, {append_deg(pt[1], 'S', 'N')})")
    ab2 = AnnotationBbox(tx, (pt[0], pt[1]-10), xycoords='data', frameon=False)
    ax.add_artist(ab2)

    #[subCorpus; Trazado de último punto].
    plt.scatter(pHistory[-1][0], pHistory[-1][1], c='r', s=3, alpha=0.9)

    plt.pause(5)

    if not plt.fignum_exists(fig_num):
        if not os.path.exists('Registro_de_recorridos'):
            os.mkdir('Registro_de_recorridos')
        loc = os.path.join('Registro_de_recorridos', f'recorrido_{start_time}')
        print(f'Guardando recorrido en: {loc}')
        fig.savefig(loc)
        sys.exit()
    
    ab.remove()
    ab2.remove()