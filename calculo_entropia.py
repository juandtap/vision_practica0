import os, time, psutil
from skimage import io, color
import skimage.measure as ski
import matplotlib.pyplot as plt
import platform
from matplotlib.backends.backend_pdf import PdfPages

# ruta relativa de las imagenes 
# las imagenes deben ir en la careta images en el mismo directorio del script
carpeta_imagenes = './images'

# calculo del tiempo total
tiempo_inicio = time.time()

# listas para guardar los tiempos de cálculo de la entropía de cada imagen
tiempos_color = []
tiempos_gris = []

# lista para  uso de RAM, para calcular el uso medio
memoria_ram = []

# lista para uso de CPU
uso_cpu = []

# listas para guardar la entropia a color y escala de grises, para el histograma y el boxplot
lista_entropias_color = []
lista_entropias_gris = []

# se obtiene los nombres de las imagenes en la carpeta
lista_imagenes = os.listdir(carpeta_imagenes)

# calculo de entropia de cada imagen
for nombre_imagen in lista_imagenes:
    
    ruta_imagen = os.path.join(carpeta_imagenes, nombre_imagen)
    
    imagen = io.imread(ruta_imagen)

    # verifica si la imagen tiene 4 canales y la convierte a 3 canales si es necesario
    if len(imagen.shape) == 3 and imagen.shape[2] == 4:
        imagen = imagen[:, :, :3]
    
    # cálculo de la entropía en escala de grises

    inicio_entropia_gris = time.time()
    imagen_gris = color.rgb2gray(imagen)
    entropia_gris = ski.shannon_entropy(imagen_gris)
    fin_entropia_gris = time.time()
    tiempos_gris.append(fin_entropia_gris - inicio_entropia_gris)

    # se agrega la entropia gris a la lista
    lista_entropias_gris.append(entropia_gris)
    
    # cálculo de la entropía a color

    inicio_entropia_color = time.time()
    entropia_color = ski.shannon_entropy(imagen)
    fin_entropia_color = time.time()
    tiempos_color.append(fin_entropia_color - inicio_entropia_color)

    # se agrega la entropia color a la lista
    lista_entropias_color.append(entropia_color)

    # Imprimir la entropía de la imagen
    print(f"Entropía gris de {nombre_imagen}: {entropia_gris}")
    print(f"Entropía color de {nombre_imagen}: {entropia_color}")

    # guarda la memoria ram usada pare cada imagen
    memoria_ram.append(psutil.virtual_memory().used)
    # guarda el uso del cpu
    uso_cpu.append(psutil.cpu_percent())

# cálculo del tiempo de ejecución total
tiempo_final = time.time()
tiempo_total = tiempo_final - tiempo_inicio
tiempo_total =  round(tiempo_total, 4)
uso_cpu_promedio = round((sum(uso_cpu) / len(uso_cpu)), 4)
memoria_usada_promedio_mb = round((sum(memoria_ram) / len(memoria_ram)) / (1024**2), 4)
memoria_ram_mb = [ram / (1024**2) for ram in memoria_ram]
# Imprimir resultados
so_utilizado = platform.system()
tiempo_promedio_entropia_color =round( (sum(tiempos_color) / len(tiempos_color)), 4)
tiempo_promedio_entropia_grises = round((sum(tiempos_gris) / len(tiempos_gris)), 4)
print("\n")
print(f"Sistema operativo utilizado: {so_utilizado}")
print(f"Tiempo total de ejecución: {tiempo_total} segundos")
print(f"Tiempo promedio calculo entropia imagen a color {tiempo_promedio_entropia_color} segundos")
print(f"Tiempo promedio calculo entropia imagen a escala de grises {tiempo_promedio_entropia_grises} segundos")
print(f"Uso de CPU promedio: {uso_cpu_promedio} %")
print(f"Uso de RAM promedio: {memoria_usada_promedio_mb} Megabytes")


# Genreacion de Informe PDF

informe_pdf = f"informe_entropia_{platform.system()}.pdf"

dimesion_pdf = (8.27, 11.69) # Tamaño A4 en pulgadas (210mm x 297mm)

with PdfPages(informe_pdf) as pdf:
    
    texto = (
        f"Informe cálculo entropía de imágenes a color y a escala de grises\n"
        f"Autor: Diego Tapia\n"
        f"Sistema operativo utilizado: {so_utilizado}\n"
        f"Tiempo total de ejecución: {tiempo_total} segundos\n"
        f"Tiempo promedio cálculo entropía imagen a color: {tiempo_promedio_entropia_color} segundos\n"
        f"Tiempo promedio cálculo entropía imagen a escala de grises: {tiempo_promedio_entropia_grises} segundos\n"
        f"Uso de CPU promedio: {uso_cpu_promedio} %\n"
        f"Uso de RAM promedio: {memoria_usada_promedio_mb} Megabytes\n"
    )
    plt.figure(figsize=dimesion_pdf)  
    plt.text(0.05, 0.95, texto, ha='left', va='top', wrap=True)
    plt.axis('off')
    pdf.savefig()
    plt.close()

# Graficos



    # boxplots entropias
    plt.figure(figsize=dimesion_pdf)  
    plt.boxplot([lista_entropias_gris, lista_entropias_color], labels=['Escala de grises', 'Color'])
    plt.xlabel('Tipo imagen')
    plt.ylabel('Entropía')
    plt.title('Diagrama de cajas de Entropías')

    pdf.savefig()
    plt.close()

    # histograma de cálculo de entropía a color
    plt.figure(figsize=dimesion_pdf)
    plt.hist(tiempos_color, bins=10, color='blue', alpha=0.7)
    plt.xlabel('Entropía')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de Cálculo de Entropía a Color')
    pdf.savefig()
    plt.close()

    # histograma  de cálculo de entropía en escala de grises
    plt.figure(figsize=dimesion_pdf)
    plt.hist(tiempos_gris, bins=10, color='green', alpha=0.7)
    plt.xlabel('Entropía')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de Cálculo de Entropía en Escala de Grises')
    pdf.savefig()
    plt.close()

    # graficos metricas, tiempo, %CPU, RAM(MB)

    plt.figure(figsize=(11.69, 8.27))

    # Gráfico 1: Tiempos de cálculo de entropía imagen a color
    plt.subplot(2, 2, 1)
    plt.plot(range(len(tiempos_color)), tiempos_color, label='Tiempos entropía color', color='green')
    plt.xlabel('imagen')
    plt.ylabel('tiempo (segundos)')
    plt.title('Tiempos Cálculo de Entropía imagen a Color')
    plt.legend()
    

    # Gráfico 2: Tiempos de cálculo de entropía imagen a escala de grises
    plt.subplot(2, 2, 2)
    plt.plot(range(len(tiempos_gris)), tiempos_gris, label='Tiempos entropía escala grises', color='gray')
    plt.xlabel('imagen')
    plt.ylabel('tiempo (segundos)')
    plt.title('Tiempos Cálculo de Entropía imagen a Escala de Grises')
    plt.legend()
    

    # Gráfico 3: Uso de CPU
    plt.subplot(2, 2, 3)
    plt.plot(range(len(uso_cpu)), uso_cpu, label='Uso de CPU', color='red')
    plt.xlabel('imagen')
    plt.ylabel('% CPU')
    plt.title('Uso de CPU')
    plt.legend()
    

    # Gráfico 4: Uso de RAM
    plt.subplot(2, 2, 4)
    plt.plot(range(len(memoria_ram_mb)), memoria_ram_mb, label='Uso de RAM (MB)', color='blue')
    plt.xlabel('imagen')
    plt.ylabel('RAM (MB)')
    plt.title('Uso de RAM')
    plt.legend()
    

    # Ajustar el espacio entre los gráficos
    plt.tight_layout()

    pdf.savefig()
    plt.close()
