#!/usr/bin/env fontforge
import fontforge
import psMat
import os
import glob

# -------------------------
# 1. Parámetros de la fuente
# -------------------------
NOMBRE_FUENTE   = "CatFont_"
desired_height  = 700   # Altura deseada de cada glifo (en unidades de FontForge)
side_bearing    = 50    # Espacio lateral a cada lado de la letra
ascent_value    = 800   # Altura por encima de la línea base
descent_value   = 200   # Altura por debajo de la línea base

# -------------------------
# 2. Crear la fuente
# -------------------------
fuente = fontforge.font()
fuente.encoding   = "UnicodeFull"
fuente.fontname   = NOMBRE_FUENTE
fuente.familyname = NOMBRE_FUENTE
fuente.fullname   = NOMBRE_FUENTE

# Ajustar ascent y descent para que las letras quepan
fuente.ascent  = ascent_value
fuente.descent = descent_value

# -------------------------
# 3. Procesar cada archivo SVG
# -------------------------
ruta_svg = "cat_svg"  # carpeta con los SVG

for archivo in glob.glob(os.path.join(ruta_svg, "*.svg")):
    nombre = os.path.basename(archivo)
    caracter, ext = os.path.splitext(nombre)

    # Evitar archivos que no sean un solo carácter (p.e. "A.svg", "B.svg", etc.)
    if len(caracter) != 1:
        print(f"Saltando {nombre}: no es un solo carácter.")
        continue

    # Crear el glifo
    codigo = ord(caracter)
    glifo = fuente.createChar(codigo)

    # Importar el contorno desde el SVG
    glifo.importOutlines(archivo)

    # -------------------------
    # 3.1. Escalado automático
    # -------------------------
    # 1) Tomar bounding box actual
    xmin, ymin, xmax, ymax = glifo.boundingBox()
    altura_actual = ymax - ymin

    # 2) Calcular factor de escala para que el glifo tenga "desired_height"
    #    Evitamos dividir entre 0 por si el SVG estuviera vacío
    if altura_actual > 0:
        scale_factor = desired_height / altura_actual
    else:
        scale_factor = 1.0  # si no hay contorno, no escalamos

    # 3) Aplicar la transformación de escala
    glifo.transform(psMat.scale(scale_factor))

    # 4) Volver a medir bounding box tras la escala
    xmin, ymin, xmax, ymax = glifo.boundingBox()

    # -------------------------
    # 3.2. Alinear la base en y=0
    # -------------------------
    # Tras escalar, movemos el glifo para que ymin sea 0 (si lo deseas)
    dy = -ymin
    glifo.transform(psMat.translate(0, dy))

    # Recalcular bounding box tras la traducción
    xmin, ymin, xmax, ymax = glifo.boundingBox()

    # -------------------------
    # 3.3. Ajustar ancho (width)
    # -------------------------
    new_width = (xmax - xmin) + 2 * side_bearing
    glifo.width = int(new_width)

# -------------------------
# 4. Generar la fuente OTF
# -------------------------
nombre_otf = f"{NOMBRE_FUENTE}.otf"
fuente.generate(nombre_otf)
print(f"Fuente generada: {nombre_otf}")
