# Documentación del Reporte Power BI

**Proyecto:** Inteligencia de Negocios - Examen Unidad I  
**Autor:** Abel Pacompia O.  
**Institución:** Universidad Privada de Tacna - FAING - EPIS  
**Archivo Principal:** `Reporte_Atenciones_Salud_Privada.pbix`  
**Plantilla:** `Reporte_Atenciones_Salud_Privada.pbit`  
**Proyecto Power BI (PBIP):** `Reporte_Atenciones_Salud_Privada.pbip`

---

## 1. Estructura de las Páginas del Reporte

El reporte cumple con el requerimiento de contar con **al menos 2 dashboards y 1 reporte tabla con filtros**:

### Dashboard 1: Indicadores Financieros y Prestacionales
* **Tarjeta KPI 1:** `Total Facturado IAFAS` (S/. Suma del monto liquidado por aseguradoras).
* **Tarjeta KPI 2:** `Total Copagos Pacientes` (S/. Suma de copagos fijos y variables asumidos por el afiliado).
* **Tarjeta KPI 3:** `Total Atenciones` (N° de prestaciones médicas facturadas).
* **Gráfico de Columnas:** `Total Facturado IAFAS por Tipo de Cobertura` (Ambulatorio, Hospitalario, Emergencia, etc.).
* **Gráfico Circular / Donut:** `Distribución del Gasto por Régimen de Afiliación` (Regular, SCTR, SOAT, Potestativo, SIS).

### Dashboard 2: Análisis Clínico y Demográfico
* **Gráfico de Anillo:** `Distribución de Atenciones por Sexo del Paciente` (Masculino vs. Femenino).
* **Gráfico de Barras Horizontales:** `Top Diagnósticos Médicos Principales (CIE-10)` (Frecuencia por código CIE-10 como dorsalgia, fracturas, etc.).
* **Distribución Territorial:** `Atenciones por Ubigeo de la IPRESS`.

### Reporte 3: Detalle de Atenciones Facturadas (Tabla con Filtros)
* **Segmentador (Slicer) 1:** Filtro por `Tipo de Cobertura`.
* **Segmentador (Slicer) 2:** Filtro por `Sexo del Paciente`.
* **Segmentador (Slicer) 3:** Filtro por `Tipo de Afiliación`.
* **Tabla Detallada:**
  * Correlativo de Atención (`VCORRPRESTA_ATE`)
  * Fecha de Prestación (`VFECPRES_ATE`)
  * Diagnóstico CIE-10 (`VPRIDIAGCIE_ATE`)
  * Tipo de Cobertura (`Tipo_Cobertura_Desc`)
  * Tipo de Afiliación (`Tipo_Afiliacion_Desc`)
  * Sexo (`Sexo_Desc`)
  * Gasto en Honorarios Médicos (`VGASTHONPROSIGV_ATE`)
  * Gasto en Farmacia e Insumos (`VGASTFARINSSIGV_ATE`)
  * Total Copago Asumido (`Total_Copago`)
  * Total Liquidado por IAFAS (`VTOTLIQIAFAS_ATE`)

---

## 2. Medidas DAX Implementadas

```dax
Total Atenciones = COUNTROWS('AtencionesSaludPrivada')

Total Facturado IAFAS = SUM('AtencionesSaludPrivada'[VTOTLIQIAFAS_ATE])

Total Copagos Pacientes = SUM('AtencionesSaludPrivada'[Total_Copago])

Total Gasto Farmacia = SUM('AtencionesSaludPrivada'[VGASTFARINSSIGV_ATE])

Total Gasto Honorarios = SUM('AtencionesSaludPrivada'[VGASTHONPROSIGV_ATE])
```

---

## 3. Instrucciones para Abrir y Actualizar en Power BI Desktop

1. Abrir Power BI Desktop en Windows.
2. Hacer doble clic en `powerbi/Reporte_Atenciones_Salud_Privada.pbix` o importar `powerbi/Reporte_Atenciones_Salud_Privada.pbit`.
3. Para refrescar los datos contra el archivo CSV local o base de datos, presionar el botón **Actualizar (Refresh)** en la pestaña Inicio.
4. Para publicar manualmente en Power BI Service:
   * Hacer clic en **Publicar (Publish)** en la cinta superior.
   * Seleccionar el Área de trabajo (Workspace).
   * Compartir el reporte con `patcuadrosq@upt.pe`.
