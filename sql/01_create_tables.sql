-- ============================================================================
-- PROYECTO: Inteligencia de Negocios - Examen Unidad I
-- AUTOR: Abel Pacompia O.
-- INSTITUCIÓN: Universidad Privada de Tacna (UPT) - FAING - EPIS
-- DATASET: Registro de Atenciones de Cobertura Prestacional de Salud Privada (SUSALUD / TEDEF)
-- DESCRIPCIÓN: Script DDL de creación de tablas relacionales y dimensionales
-- ============================================================================

-- 1. TABLAS DIMENSIONALES (CATÁLOGOS OFICIALES SUSALUD)

DROP VIEW IF EXISTS vw_analisis_atenciones_salud;
DROP TABLE IF EXISTS atenciones_salud_privada;
DROP TABLE IF EXISTS dim_tipo_cobertura;
DROP TABLE IF EXISTS dim_tipo_afiliacion;
DROP TABLE IF EXISTS dim_tipo_profesional;
DROP TABLE IF EXISTS dim_sexo;
DROP TABLE IF EXISTS dim_filiacion;
DROP TABLE IF EXISTS dim_tipo_egreso;
DROP TABLE IF EXISTS dim_tipo_hospitalizacion;
DROP TABLE IF EXISTS dim_tipo_doc_pago;
DROP TABLE IF EXISTS dim_tipo_doc_identidad;

-- Dimensión Tipo de Cobertura
CREATE TABLE dim_tipo_cobertura (
    cod_cobertura VARCHAR(5) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

-- Dimensión Tipo de Afiliación
CREATE TABLE dim_tipo_afiliacion (
    cod_afiliacion VARCHAR(5) PRIMARY KEY,
    regimen VARCHAR(50) NOT NULL,
    descripcion VARCHAR(100) NOT NULL
);

-- Dimensión Tipo de Profesional Responsable
CREATE TABLE dim_tipo_profesional (
    cod_profesional VARCHAR(5) PRIMARY KEY,
    colegio_profesional VARCHAR(150) NOT NULL
);

-- Dimensión Sexo
CREATE TABLE dim_sexo (
    cod_sexo VARCHAR(5) PRIMARY KEY,
    descripcion VARCHAR(20) NOT NULL
);

-- Dimensión Filiación del Paciente
CREATE TABLE dim_filiacion (
    cod_filiacion VARCHAR(5) PRIMARY KEY,
    parentesco VARCHAR(100) NOT NULL
);

-- Dimensión Tipo de Egreso Hospitalario
CREATE TABLE dim_tipo_egreso (
    cod_egreso VARCHAR(5) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

-- Dimensión Tipo de Hospitalización
CREATE TABLE dim_tipo_hospitalizacion (
    cod_hospitalizacion VARCHAR(5) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

-- Dimensión Tipo Documento de Pago
CREATE TABLE dim_tipo_doc_pago (
    cod_doc_pago VARCHAR(5) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

-- Dimensión Tipo Documento de Identidad
CREATE TABLE dim_tipo_doc_identidad (
    cod_doc_identidad VARCHAR(5) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

-- 2. TABLA PRINCIPAL / TABLA DE HECHOS: atenciones_salud_privada

CREATE TABLE atenciones_salud_privada (
    id_atencion BIGSERIAL PRIMARY KEY,
    vcodiafas_fac VARCHAR(64) NOT NULL,
    vcodipress_fac VARCHAR(64) NOT NULL,
    vtdocpago_fac VARCHAR(10),
    vndocpago_fac VARCHAR(64),
    vcorrpresta_ate VARCHAR(10),
    vtafilpac_ate VARCHAR(10),
    vtdociden_ate VARCHAR(10),
    vnumdociden_ate VARCHAR(64),
    vtipocobert_ate VARCHAR(10),
    vsubtipcobert_ate VARCHAR(10),
    vpridiagcie_ate VARCHAR(20),
    vfecpres_ate VARCHAR(10),
    vtitprorespres_ate VARCHAR(10),
    vtipohospi_ate VARCHAR(10),
    vfecingrhosp_ate VARCHAR(10),
    vfecegrhosp_ate VARCHAR(10),
    vtipegrehosp_ate VARCHAR(10),
    vdiasestfac_ate INTEGER DEFAULT 0,
    vfecnacpac_ate VARCHAR(10),
    vsexopac_ate VARCHAR(5),
    vfiliapac_ate VARCHAR(10),
    vubigeoipress_ate VARCHAR(10),
    vgasthonprosigv_ate NUMERIC(14,2) DEFAULT 0.00,
    vgastprodosigv_ate NUMERIC(14,2) DEFAULT 0.00,
    vgasthtsclitopsigv_ate NUMERIC(14,2) DEFAULT 0.00,
    vgastexauxlabsigv_ate NUMERIC(14,2) DEFAULT 0.00,
    vgastexauximgsigv_ate NUMERIC(14,2) DEFAULT 0.00,
    vgastfarinssigv_ate NUMERIC(14,2) DEFAULT 0.00,
    vgastprotsigv_ate NUMERIC(14,2) DEFAULT 0.00,
    vgastmedexoigv_ate NUMERIC(14,2) DEFAULT 0.00,
    vogpressldsigv_ate NUMERIC(14,2) DEFAULT 0.00,
    vcopagofijosigv_ate NUMERIC(14,2) DEFAULT 0.00,
    vcpagofijoexigv_ate NUMERIC(14,2) DEFAULT 0.00,
    vcopagovarsigv_ate NUMERIC(14,2) DEFAULT 0.00,
    vcpagovarexigv_ate NUMERIC(14,2) DEFAULT 0.00,
    vtotgastcubsigv_ate NUMERIC(14,2) DEFAULT 0.00,
    vtotliqiafas_ate NUMERIC(14,2) DEFAULT 0.00,
    dfecrecep_pq TIMESTAMP,
    ubigeo_afiliado VARCHAR(10),
    periodo_publicacion VARCHAR(10) DEFAULT '2026-08',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_atenciones_cobertura FOREIGN KEY (vtipocobert_ate) REFERENCES dim_tipo_cobertura(cod_cobertura),
    CONSTRAINT fk_atenciones_afiliacion FOREIGN KEY (vtafilpac_ate) REFERENCES dim_tipo_afiliacion(cod_afiliacion),
    CONSTRAINT fk_atenciones_sexo FOREIGN KEY (vsexopac_ate) REFERENCES dim_sexo(cod_sexo),
    CONSTRAINT fk_atenciones_docpago FOREIGN KEY (vtdocpago_fac) REFERENCES dim_tipo_doc_pago(cod_doc_pago)
);

-- 3. ÍNDICES ANALÍTICOS (OPTIMIZACIÓN PARA CONSULTAS DE INTELIGENCIA DE NEGOCIOS)

CREATE INDEX idx_atenciones_fecpres ON atenciones_salud_privada(vfecpres_ate);
CREATE INDEX idx_atenciones_cobertura ON atenciones_salud_privada(vtipocobert_ate);
CREATE INDEX idx_atenciones_cie10 ON atenciones_salud_privada(vpridiagcie_ate);
CREATE INDEX idx_atenciones_ubigeo_ipress ON atenciones_salud_privada(vubigeoipress_ate);
CREATE INDEX idx_atenciones_ubigeo_afiliado ON atenciones_salud_privada(ubigeo_afiliado);
CREATE INDEX idx_atenciones_iafas ON atenciones_salud_privada(vcodiafas_fac);
CREATE INDEX idx_atenciones_ipress ON atenciones_salud_privada(vcodipress_fac);

-- 4. VISTA ANALÍTICA PARA CONSUMO DESDE POWER BI Y REPORTING

CREATE VIEW vw_analisis_atenciones_salud AS
SELECT
    a.id_atencion,
    a.vcodiafas_fac AS codigo_iafas,
    a.vcodipress_fac AS codigo_ipress,
    dp.descripcion AS tipo_documento_pago,
    a.vndocpago_fac AS nro_documento_pago,
    a.vcorrpresta_ate AS correlativo_prestacion,
    da.descripcion AS tipo_afiliacion,
    da.regimen AS regimen_afiliacion,
    di.descripcion AS tipo_doc_identidad,
    a.vnumdociden_ate AS nro_doc_identidad,
    dc.descripcion AS tipo_cobertura,
    a.vsubtipcobert_ate AS subtipo_cobertura,
    a.vpridiagcie_ate AS diagnostico_cie10,
    TO_DATE(a.vfecpres_ate, 'YYYYMMDD') AS fecha_prestacion,
    dpr.colegio_profesional AS profesional_responsable,
    dh.descripcion AS tipo_hospitalizacion,
    CASE WHEN a.vfecingrhosp_ate IS NOT NULL AND a.vfecingrhosp_ate <> '' 
         THEN TO_DATE(a.vfecingrhosp_ate, 'YYYYMMDD') ELSE NULL END AS fecha_ingreso_hosp,
    CASE WHEN a.vfecegrhosp_ate IS NOT NULL AND a.vfecegrhosp_ate <> '' 
         THEN TO_DATE(a.vfecegrhosp_ate, 'YYYYMMDD') ELSE NULL END AS fecha_egreso_hosp,
    de.descripcion AS tipo_egreso_hosp,
    COALESCE(a.vdiasestfac_ate, 0) AS dias_estancia_facturable,
    CASE WHEN a.vfecnacpac_ate IS NOT NULL AND a.vfecnacpac_ate <> '' 
         THEN TO_DATE(a.vfecnacpac_ate, 'YYYYMMDD') ELSE NULL END AS fecha_nacimiento,
    s.descripcion AS sexo_paciente,
    df.parentesco AS filiacion_paciente,
    a.vubigeoipress_ate AS ubigeo_ipress,
    a.ubigeo_afiliado AS ubigeo_afiliado,
    a.vgasthonprosigv_ate AS gasto_honorarios,
    a.vgastprodosigv_ate AS gasto_odontologico,
    a.vgasthtsclitopsigv_ate AS gasto_hoteleria_clinica,
    a.vgastexauxlabsigv_ate AS gasto_laboratorio,
    a.vgastexauximgsigv_ate AS gasto_imagenes,
    a.vgastfarinssigv_ate AS gasto_farmacia,
    a.vgastprotsigv_ate AS gasto_protesis,
    a.vgastmedexoigv_ate AS gasto_medicamentos_exonerados,
    a.vogpressldsigv_ate AS otros_gastos_salud,
    a.vcopagofijosigv_ate AS copago_fijo_afecto,
    a.vcpagofijoexigv_ate AS copago_fijo_exonerado,
    a.vcopagovarsigv_ate AS copago_variable_afecto,
    a.vcpagovarexigv_ate AS copago_variable_exonerado,
    (a.vcopagofijosigv_ate + a.vcpagofijoexigv_ate + a.vcopagovarsigv_ate + a.vcpagovarexigv_ate) AS total_copago,
    a.vtotgastcubsigv_ate AS total_gastos_cubiertos,
    a.vtotliqiafas_ate AS total_liquidado_iafas,
    a.dfecrecep_pq AS fecha_recepcion_tedef,
    a.periodo_publicacion
FROM atenciones_salud_privada a
LEFT JOIN dim_tipo_cobertura dc ON a.vtipocobert_ate = dc.cod_cobertura
LEFT JOIN dim_tipo_afiliacion da ON a.vtafilpac_ate = da.cod_afiliacion
LEFT JOIN dim_tipo_profesional dpr ON a.vtitprorespres_ate = dpr.cod_profesional
LEFT JOIN dim_sexo s ON a.vsexopac_ate = s.cod_sexo
LEFT JOIN dim_filiacion df ON a.vfiliapac_ate = df.cod_filiacion
LEFT JOIN dim_tipo_egreso de ON a.vtipegrehosp_ate = de.cod_egreso
LEFT JOIN dim_tipo_hospitalizacion dh ON a.vtipohospi_ate = dh.cod_hospitalizacion
LEFT JOIN dim_tipo_doc_pago dp ON a.vtdocpago_fac = dp.cod_doc_pago
LEFT JOIN dim_tipo_doc_identidad di ON a.vtdociden_ate = di.cod_doc_identidad;
