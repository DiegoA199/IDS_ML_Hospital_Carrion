# Evidencia de Quality Gate SonarCloud - IDS-ML Hospital Carrion

## 1. Identificacion

| Campo | Valor |
|---|---|
| Proyecto | IDS ML Hospital Carrion |
| Repositorio GitHub | `DiegoA199/IDS_ML_Hospital_Carrion` |
| Proyecto SonarCloud | `DiegoA199_IDS_ML_Hospital_Carrion` |
| Organizacion SonarCloud | `diegoa199` |
| Herramienta | SonarQube Cloud / SonarCloud |
| Fecha de verificacion | 2026-06-23 |
| Rama revisada | `main` |
| Revision | Consultar dashboard/API de SonarCloud; se actualiza con cada push |

## 2. Enlaces de consulta

| Recurso | Enlace |
|---|---|
| Dashboard SonarCloud | <https://sonarcloud.io/project/overview?id=DiegoA199_IDS_ML_Hospital_Carrion> |
| Quality Gate por API | <https://sonarcloud.io/api/qualitygates/project_status?projectKey=DiegoA199_IDS_ML_Hospital_Carrion> |
| Metricas por API | <https://sonarcloud.io/api/measures/component?component=DiegoA199_IDS_ML_Hospital_Carrion&metricKeys=bugs,vulnerabilities,code_smells,duplicated_lines_density,reliability_rating,security_rating,sqale_rating,security_hotspots,ncloc> |
| Corrida de GitHub Actions usada como evidencia | <https://github.com/DiegoA199/IDS_ML_Hospital_Carrion/actions/runs/28049612664> |

## 3. Resultado oficial de SonarCloud

La verificacion oficial fue realizada sobre el proyecto vinculado a GitHub y revisada nuevamente el 2026-06-23.
Las metricas siguientes corresponden al estado oficial visible en SonarCloud y a la corrida de GitHub Actions asociada al commit `f67055f`.

![Evidencia visual SonarCloud](../evidencias/sonarqube_quality_gate.png)

| Indicador | Resultado |
|---|---:|
| Quality Gate | OK |
| Bugs | 0 |
| Vulnerabilities | 0 |
| Security Hotspots | 0 |
| Code Smells | 0 |
| Duplicacion de lineas | 0.0% |
| Reliability Rating | A |
| Security Rating | A |
| Maintainability Rating | A |
| Lineas de codigo analizadas | 1615 |
| Issues abiertos | 0 |
| Fecha del snapshot documentado | 2026-06-02 |

Las calificaciones `1.0` reportadas por la API de SonarCloud equivalen a rating **A** en confiabilidad, seguridad y mantenibilidad.

## 4. Condiciones del Quality Gate

| Condicion | Umbral | Valor obtenido | Estado |
|---|---:|---:|---|
| Nueva confiabilidad | A | A | OK |
| Nueva seguridad | A | A | OK |
| Nueva mantenibilidad | A | A | OK |
| Duplicacion en nuevo codigo | <= 3% | 0.0% | OK |
| Security hotspots revisados | 100% | 100.0% | OK |

Resultado general: **Quality Gate aprobado**.

## 5. Validacion local complementaria

Antes del analisis oficial se valido localmente el comportamiento del proyecto con pruebas automatizadas:

```powershell
pytest --cov=src --cov-report=xml --cov-report=term
```

| Indicador local | Resultado |
|---|---:|
| Pruebas ejecutadas | 44 |
| Pruebas exitosas | 44 |
| Pruebas fallidas | 0 |
| Cobertura efectiva | 92% |
| Reporte generado | `coverage.xml` |

El archivo `coverage.xml` se genera para el analisis, pero no se versiona porque es un artefacto temporal.

## 6. Relacion con GitHub Actions

El workflow `.github/workflows/quality-sonar.yml` queda preparado para:

1. instalar dependencias;
2. ejecutar pruebas con `pytest`;
3. generar `coverage.xml`;
4. subir el reporte como artefacto;
5. ejecutar el scanner de SonarCloud cuando exista el secreto `SONAR_TOKEN`.

La corrida publica de GitHub Actions revisada finalizo en estado `success` para la rama `main`.

Nota tecnica: SonarCloud Automatic Analysis ya entrego un resultado oficial aprobado. El secreto `SONAR_TOKEN` se requiere solo si se desea que el scanner se ejecute desde GitHub Actions importando tambien `coverage.xml` en cada push.

## 7. Interpretacion para la tesis

El resultado obtenido evidencia que el prototipo IDS-ML cumple criterios basicos de calidad estatica para una sustentacion academica:

- no presenta bugs reportados por SonarCloud;
- no presenta vulnerabilidades reportadas;
- no presenta security hotspots pendientes;
- no presenta code smells abiertos;
- no presenta duplicacion detectable;
- mantiene ratings A en confiabilidad, seguridad y mantenibilidad;
- cuenta con pruebas automatizadas y cobertura local efectiva de 92%.

Esto no reemplaza las pruebas funcionales con usuarios TI ni la validacion con datasets reales, pero sirve como evidencia tecnica objetiva de mantenibilidad y control de calidad del software.

## 8. Evidencia recomendada para anexar

Para el informe final o la sustentacion se recomienda capturar:

- pantalla del dashboard SonarCloud con Quality Gate OK;
- pantalla de la seccion Issues con 0 issues abiertos;
- pantalla de GitHub Actions con estado `success`;
- salida local de `pytest --cov=src --cov-report=xml`;
- este documento como respaldo textual de la evidencia.

## 9. Comandos de reproduccion

```powershell
pytest --cov=src --cov-report=xml
```

Si se tiene instalado Sonar Scanner y configurado el token:

```powershell
sonar-scanner
```

En GitHub, despues de configurar `SONAR_TOKEN`, tambien puede ejecutarse manualmente:

```text
GitHub > Actions > Quality and Sonar > Run workflow
```

## 10. Conclusion

El proyecto IDS-ML Hospital Carrion cuenta con evidencia oficial de SonarCloud con **Quality Gate OK**. La revision muestra 0 bugs, 0 vulnerabilidades, 0 security hotspots, 0 code smells, 0.0% de duplicacion y ratings A, por lo que el proyecto queda apto para ser presentado como prototipo de tesis desde el punto de vista de calidad estatica del codigo.
