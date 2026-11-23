
# Integración de Datos Educativos y Poblacionales de Loja

## 1. Descripción del proyecto

Este proyecto consiste en implementar un proceso ETL (Extracción, Transformación y Carga) para integrar información educativa y poblacional de la provincia de Loja, Ecuador.

Se utilizaron dos conjuntos de datos públicos provenientes del Instituto Nacional de Estadística y Censos (INEC) y del Ministerio de Educación (MINEDUC).

El objetivo es obtener un conjunto de datos organizado que permita relacionar la población de 5 a 19 años con la cantidad de estudiantes matriculados, instituciones educativas y docentes de los 16 cantones de Loja.

## 2. Fuentes de datos

### Dataset 1: INEC - Censo de Población 2022

**Archivo:** `2.1.csv`

**Fuente:** Instituto Nacional de Estadística y Censos (INEC).

**Formato:** CSV (valores separados por comas).

**Enlace:** https://www.censoecuador.gob.ec/resultados-censo/

Este archivo contiene información sobre la población ecuatoriana, organizada por provincia, cantón, parroquia, sexo y grupos quinquenales de edad.

Para el proyecto se utilizaron principalmente los siguientes datos:

- Provincia y cantón.
- Grupos de edad.
- Población total.
- Población masculina y femenina.

**Problemas identificados:**

- Encabezados y filas informativas mezclados con los datos.
- Columnas sin nombres descriptivos.
- Diferentes niveles geográficos dentro de una misma tabla.
- Información de provincias y grupos de edad no necesarios para el proyecto.
- Valores numéricos que requerían conversión.

### Dataset 2: MINEDUC - Registro Administrativo Histórico

**Archivo:** `registro-administrativo-historico_2009-2024-inicio.csv`

**Fuente:** Ministerio de Educación del Ecuador.

**Formato:** CSV (valores separados por punto y coma).

**Enlace:** https://www.datosabiertos.gob.ec/dataset/registro-de-matricula-mineduc

Este archivo contiene información histórica de las instituciones educativas del Ecuador, incluyendo su ubicación, cantidad de estudiantes matriculados y docentes.

Para el proyecto se utilizaron principalmente:

- Año lectivo.
- Provincia y cantón.
- Código geográfico.
- Código AMIE de las instituciones.
- Total de estudiantes.
- Total de docentes.

**Problemas identificados:**

- Existencia de filas vacías.
- Registros correspondientes a diferentes períodos académicos.
- Información de todas las provincias del Ecuador.
- Diferencias en la escritura de los nombres geográficos.
- Valores numéricos con separadores de miles.

## 3. Herramientas utilizadas

- **Python:** desarrollo del proceso ETL.
- **pandas:** manipulación, limpieza e integración de datos.
- **Visual Studio Code:** ejecución del programa.
- **Microsoft Excel:** exploración y revisión de los archivos CSV.
- **GitHub:** almacenamiento del proyecto y sus evidencias.

## 4. Proceso ETL

El proceso se desarrolló mediante un script de Python llamado `etl.py` y se dividió en las siguientes etapas:

### Extracción

Se importaron los dos archivos CSV originales utilizando la librería pandas.

Se consideraron las diferencias de formato, codificación y delimitadores de cada archivo para realizar una lectura correcta de los datos.

### Transformación

Se realizaron operaciones de limpieza y preparación en ambos conjuntos de datos.

**INEC:**

- Eliminación de filas y columnas innecesarias.
- Organización y renombramiento de columnas.
- Filtrado de los registros correspondientes a Loja.
- Selección de los grupos de edad de 5 a 19 años.
- Conversión de datos numéricos.
- Agrupación de la población por cantón.

**MINEDUC:**

- Eliminación de registros vacíos.
- Filtrado de la provincia de Loja.
- Selección del período académico 2022-2023 Inicio.
- Normalización de nombres de cantones.
- Conversión de valores numéricos.
- Agrupación de instituciones, estudiantes y docentes por cantón.

### Integración

Se relacionaron ambos conjuntos de datos utilizando los nombres normalizados de los cantones como campo de correspondencia.

La integración se realizó mediante un `INNER JOIN`, obteniendo una tabla que combina información poblacional y educativa de los 16 cantones de Loja.

### Carga

Los datos procesados se almacenaron en nuevos archivos CSV dentro de la carpeta `datos_resultantes/`.

Se generaron archivos con los datos limpios de cada institución y un archivo final con la información integrada.

### Validación

Se realizaron comprobaciones para verificar:

- La correspondencia de los cantones entre ambas fuentes.
- La ausencia de duplicados en las tablas agrupadas.
- La consistencia de los valores numéricos.
- La integración de los 16 cantones de Loja.
- La coherencia de los resultados obtenidos.

## 5. Resultados obtenidos

El proceso ETL se ejecutó correctamente en Python, obteniendo los siguientes resultados:

| Indicador | Resultado |
|---|---:|
| Cantones integrados | 16 |
| Población de 5 a 19 años | 128.024 |
| Estudiantes matriculados | 117.041 |
| Instituciones educativas | 1.102 |

El conjunto de datos resultante permite consultar información de población, matrícula, instituciones educativas y docentes por cantón.

Es importante considerar que los datos poblacionales corresponden al Censo 2022 y los educativos al período 2022-2023, por lo que su integración permite una comparación descriptiva y no representa directamente una tasa de cobertura escolar.


## 6. Conclusión

El proyecto permitió integrar información de dos fuentes públicas que originalmente presentaban estructuras y formatos diferentes.

Mediante el proceso ETL se realizaron operaciones de limpieza, normalización, filtrado y agrupación, obteniendo un conjunto de datos consolidado de los 16 cantones de Loja.

Los resultados constituyen una base organizada para futuros análisis relacionados con la población y el sistema educativo de la provincia, además de demostrar la importancia de preparar y validar los datos antes de utilizarlos en soluciones de Inteligencia de Negocios.
