from pathlib import Path
import pandas as pd
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'datos_fuente'
OUT = ROOT / 'datos_resultantes'
OUT.mkdir(exist_ok=True)

def normalizar(x):
    x = str(x).strip().upper()
    return ''.join(c for c in unicodedata.normalize('NFKD', x) if not unicodedata.combining(c))

def numero(s):
    return pd.to_numeric(s.astype('string').str.replace(',', '', regex=False).str.strip(), errors='coerce')

# INEC: encabezados estadísticos, totales de provincia y parroquias se excluyen.
inec = pd.read_csv(SRC/'2.1.csv', encoding='latin1', header=None, dtype=str)
inec = inec.iloc[:, 1:8].copy()
inec.columns = ['provincia','canton','parroquia','grupo_edad','poblacion','hombres','mujeres']
for c in ['provincia','canton','parroquia','grupo_edad']:
    inec[c] = inec[c].fillna('').str.strip()
inec = inec[(inec.provincia.map(normalizar)=='LOJA') & (inec.canton.str.len()>0)]
inec = inec[(inec.canton.map(normalizar)!='TOTAL LOJA') & (inec.parroquia.map(normalizar).str.startswith('TOTAL '))]
inec = inec[inec.grupo_edad.isin(['De 5-9','De 10-14','De 15-19'])].copy()
for c in ['poblacion','hombres','mujeres']:
    inec[c] = numero(inec[c])
assert inec[['poblacion','hombres','mujeres']].notna().all().all(), 'INEC: cifras inválidas'
assert (inec.poblacion == inec.hombres + inec.mujeres).all(), 'INEC: sexo no cuadra con total'
inec['clave_canton'] = inec.canton.map(normalizar)
assert not inec.duplicated(['clave_canton','grupo_edad']).any(), 'INEC: duplicación de totales cantonales'
pivot = inec.pivot(index='clave_canton', columns='grupo_edad', values='poblacion').rename(columns={'De 5-9':'poblacion_5_9','De 10-14':'poblacion_10_14','De 15-19':'poblacion_15_19'}).reset_index()
pivot['poblacion_5_19'] = pivot[['poblacion_5_9','poblacion_10_14','poblacion_15_19']].sum(axis=1)
pivot.to_csv(OUT/'inec_loja_limpio.csv', index=False, encoding='utf-8-sig')

# MINEDUC: conservar códigos como texto, para no perder ceros iniciales.
mineduc = pd.read_csv(SRC/'registro-administrativo-historico_2009-2024-inicio.csv', sep=';', dtype=str, encoding='utf-8-sig', low_memory=False)
mineduc = mineduc.dropna(how='all')
mineduc = mineduc[(mineduc.Provincia.fillna('').map(normalizar)=='LOJA') & (mineduc.Anio_lectivo.fillna('').str.strip()=='2022-2023 Inicio')].copy()
mineduc['clave_canton'] = mineduc.Canton.fillna('').map(normalizar)
for c in ['Total_Estudiantes','Total_Docentes']:
    mineduc[c] = pd.to_numeric(mineduc[c].str.strip().str.replace('.', '', regex=False).str.replace(',', '', regex=False), errors='coerce')
assert not mineduc.empty, 'MINEDUC: no se encontraron registros del período'
assert mineduc[['Total_Estudiantes','Total_Docentes']].notna().all().all(), 'MINEDUC: cifras faltantes/no numéricas'
assert (mineduc[['Total_Estudiantes','Total_Docentes']] >= 0).all().all(), 'MINEDUC: cifras negativas'
# Verificar la unicidad de AMIE antes de contar instituciones.
repetidas = mineduc.duplicated(['clave_canton','AMIE']).sum()
assert repetidas == 0, f'MINEDUC: {repetidas} AMIE repetidos por cantón; revisar granularidad'
edu = mineduc.groupby('clave_canton',as_index=False).agg(instituciones=('AMIE','nunique'),estudiantes_matriculados=('Total_Estudiantes','sum'),docentes=('Total_Docentes','sum'))
edu.to_csv(OUT/'mineduc_loja_limpio.csv',index=False,encoding='utf-8-sig')

faltan_inec = sorted(set(edu.clave_canton)-set(pivot.clave_canton))
faltan_mineduc = sorted(set(pivot.clave_canton)-set(edu.clave_canton))
assert not faltan_inec and not faltan_mineduc, f'Cantones sin correspondencia: INEC={faltan_inec}; MINEDUC={faltan_mineduc}'
resultado = pivot.merge(edu,on='clave_canton',how='inner',validate='one_to_one')
resultado.insert(0,'provincia','LOJA')
resultado = resultado.rename(columns={'clave_canton':'canton'}).sort_values('canton')
assert len(resultado)==16, f'Se esperaban 16 cantones; hay {len(resultado)}'
assert resultado.estudiantes_matriculados.sum()==mineduc.Total_Estudiantes.sum()
assert resultado.poblacion_5_19.sum()==pivot.poblacion_5_19.sum()
resultado.to_csv(OUT/'educacion_poblacion_loja.csv',index=False,encoding='utf-8-sig')
print('ETL completado. Cantones:',len(resultado))
print('Población 5-19:',int(resultado.poblacion_5_19.sum()))
print('Estudiantes:',int(resultado.estudiantes_matriculados.sum()))
print('Instituciones:',int(resultado.instituciones.sum()))
print(resultado.to_string(index=False))
