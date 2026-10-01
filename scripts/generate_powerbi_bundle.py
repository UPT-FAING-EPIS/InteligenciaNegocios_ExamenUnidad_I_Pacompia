import os
import json
import zipfile

def build_pbi_bundle():
    base_dir = r"C:\Users\HP\Documents\InteligenciaNegocios_ExamenUnidad_I_Pacompia"
    pbi_dir = os.path.join(base_dir, "powerbi")
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(pbi_dir, exist_ok=True)

    csv_abs_path = os.path.join(data_dir, "atenciones_salud_privada_sample.csv").replace("\\", "/")

    # 1. CONTENT TYPES XML
    content_types_xml = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="xml" ContentType="application/xml" />
  <Override PartName="/Version" ContentType="application/json" />
  <Override PartName="/Settings" ContentType="application/json" />
  <Override PartName="/Metadata" ContentType="application/json" />
  <Override PartName="/DiagramLayout" ContentType="application/json" />
  <Override PartName="/DataModelSchema" ContentType="application/json" />
  <Override PartName="/Report/Layout" ContentType="application/json" />
</Types>"""

    # 2. VERSION
    version_str = "1.28"

    # 3. SETTINGS
    settings_json = json.dumps({"Locale": "es-PE"}, indent=2)

    # 4. METADATA
    metadata_json = json.dumps({"Version": 1, "Type": 1}, indent=2)

    # 5. DIAGRAM LAYOUT
    diagram_json = json.dumps({"version": "1.1.0", "diagrams": []}, indent=2)

    # 6. DATA MODEL SCHEMA
    m_code = f"""let
    Origen = Csv.Document(File.Contents("{csv_abs_path}"),[Delimiter=";", Columns=39, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Encabezados promovidos" = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Encabezados promovidos",{{
        {{"VCODIAFAS_FAC", type text}},
        {{"VCODIPRESS_FAC", type text}},
        {{"VTDOCPAGO_FAC", type text}},
        {{"VNDOCPAGO_FAC", type text}},
        {{"VCORRPRESTA_ATE", type text}},
        {{"VTAFILPAC_ATE", type text}},
        {{"VTDOCIDEN_ATE", type text}},
        {{"VNUMDOCIDEN_ATE", type text}},
        {{"VTIPOCOBERT_ATE", type text}},
        {{"VSUBTIPCOBERT_ATE", type text}},
        {{"VPRIDIAGCIE_ATE", type text}},
        {{"VFECPRES_ATE", type text}},
        {{"VTITPRORESPRES_ATE", type text}},
        {{"VTIPOHOSPI_ATE", type text}},
        {{"VFECINGRHOSP_ATE", type text}},
        {{"VFECEGRHOSP_ATE", type text}},
        {{"VTIPEGREHOSP_ATE", type text}},
        {{"VDIASESTFAC_ATE", Int64.Type}},
        {{"VFECNACPAC_ATE", type text}},
        {{"VSEXOPAC_ATE", type text}},
        {{"VFILIAPAC_ATE", type text}},
        {{"VUBIGEOIPRESS_ATE", type text}},
        {{"VGASTHONPROSIGV_ATE", type number}},
        {{"VGASTPRODOSIGV_ATE", type number}},
        {{"VGASTHTSCLITOPSIGV_ATE", type number}},
        {{"VGASTEXAUXLABSIGV_ATE", type number}},
        {{"VGASTEXAUXIMGSIGV_ATE", type number}},
        {{"VGASTFARINSSIGV_ATE", type number}},
        {{"VGASTPROTSIGV_ATE", type number}},
        {{"VGASTMEDEXOIGV_ATE", type number}},
        {{"VOGPRESSLDSIGV_ATE", type number}},
        {{"VCOPAGOFIJOSIGV_ATE", type number}},
        {{"VCPAGOFIJOEXIGV_ATE", type number}},
        {{"VCOPAGOVARSIGV_ATE", type number}},
        {{"VCPAGOVAREXIGV_ATE", type number}},
        {{"VTOTGASTCUBSIGV_ATE", type number}},
        {{"VTOTLIQIAFAS_ATE", type number}},
        {{"DFECRECEP_PQ", type datetime}},
        {{"UBIGEO_AFILIADO", type text}}
    }}),
    #"Columna Cobertura" = Table.AddColumn(#"Tipo cambiado", "Tipo_Cobertura_Desc", each if [VTIPOCOBERT_ATE] = "1" then "Extra hospitalario" else if [VTIPOCOBERT_ATE] = "2" then "Médico en planta" else if [VTIPOCOBERT_ATE] = "3" then "Medicinas alternativas" else if [VTIPOCOBERT_ATE] = "4" then "Ambulatorio" else if [VTIPOCOBERT_ATE] = "5" then "Hospitalaria" else if [VTIPOCOBERT_ATE] = "6" then "Emergencia" else if [VTIPOCOBERT_ATE] = "8" then "Integral (SIS)" else "Otros", type text),
    #"Columna Sexo" = Table.AddColumn(#"Columna Cobertura", "Sexo_Desc", each if [VSEXOPAC_ATE] = "1" then "Masculino" else if [VSEXOPAC_ATE] = "2" then "Femenino" else "No especificado", type text),
    #"Columna Afiliacion" = Table.AddColumn(#"Columna Sexo", "Tipo_Afiliacion_Desc", each if [VTAFILPAC_ATE] = "1" then "Regular" else if [VTAFILPAC_ATE] = "2" then "SCTR" else if [VTAFILPAC_ATE] = "3" then "Potestativo" else if [VTAFILPAC_ATE] = "4" then "SCTR Indep." else if [VTAFILPAC_ATE] = "6" then "SOAT" else if [VTAFILPAC_ATE] = "8" then "SIS Subsidiado" else "Otros", type text),
    #"Columna Copago Total" = Table.AddColumn(#"Columna Afiliacion", "Total_Copago", each [VCOPAGOFIJOSIGV_ATE] + [VCPAGOFIJOEXIGV_ATE] + [VCOPAGOVARSIGV_ATE] + [VCPAGOVAREXIGV_ATE], type number)
in
    #"Columna Copago Total" """

    data_model_schema = {
        "name": "Model",
        "compatibilityLevel": 1550,
        "model": {
            "culture": "es-PE",
            "dataAccessOptions": {
                "legacyRedirects": True,
                "returnErrorValuesAsNull": True
            },
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "tables": [
                {
                    "name": "AtencionesSaludPrivada",
                    "columns": [
                        {"name": "VCODIAFAS_FAC", "dataType": "string", "sourceColumn": "VCODIAFAS_FAC"},
                        {"name": "VCODIPRESS_FAC", "dataType": "string", "sourceColumn": "VCODIPRESS_FAC"},
                        {"name": "VTDOCPAGO_FAC", "dataType": "string", "sourceColumn": "VTDOCPAGO_FAC"},
                        {"name": "VNDOCPAGO_FAC", "dataType": "string", "sourceColumn": "VNDOCPAGO_FAC"},
                        {"name": "VCORRPRESTA_ATE", "dataType": "string", "sourceColumn": "VCORRPRESTA_ATE"},
                        {"name": "VTAFILPAC_ATE", "dataType": "string", "sourceColumn": "VTAFILPAC_ATE"},
                        {"name": "VTDOCIDEN_ATE", "dataType": "string", "sourceColumn": "VTDOCIDEN_ATE"},
                        {"name": "VNUMDOCIDEN_ATE", "dataType": "string", "sourceColumn": "VNUMDOCIDEN_ATE"},
                        {"name": "VTIPOCOBERT_ATE", "dataType": "string", "sourceColumn": "VTIPOCOBERT_ATE"},
                        {"name": "VSUBTIPCOBERT_ATE", "dataType": "string", "sourceColumn": "VSUBTIPCOBERT_ATE"},
                        {"name": "VPRIDIAGCIE_ATE", "dataType": "string", "sourceColumn": "VPRIDIAGCIE_ATE"},
                        {"name": "VFECPRES_ATE", "dataType": "string", "sourceColumn": "VFECPRES_ATE"},
                        {"name": "VTITPRORESPRES_ATE", "dataType": "string", "sourceColumn": "VTITPRORESPRES_ATE"},
                        {"name": "VTIPOHOSPI_ATE", "dataType": "string", "sourceColumn": "VTIPOHOSPI_ATE"},
                        {"name": "VFECINGRHOSP_ATE", "dataType": "string", "sourceColumn": "VFECINGRHOSP_ATE"},
                        {"name": "VFECEGRHOSP_ATE", "dataType": "string", "sourceColumn": "VFECEGRHOSP_ATE"},
                        {"name": "VTIPEGREHOSP_ATE", "dataType": "string", "sourceColumn": "VTIPEGREHOSP_ATE"},
                        {"name": "VDIASESTFAC_ATE", "dataType": "int64", "sourceColumn": "VDIASESTFAC_ATE"},
                        {"name": "VFECNACPAC_ATE", "dataType": "string", "sourceColumn": "VFECNACPAC_ATE"},
                        {"name": "VSEXOPAC_ATE", "dataType": "string", "sourceColumn": "VSEXOPAC_ATE"},
                        {"name": "VFILIAPAC_ATE", "dataType": "string", "sourceColumn": "VFILIAPAC_ATE"},
                        {"name": "VUBIGEOIPRESS_ATE", "dataType": "string", "sourceColumn": "VUBIGEOIPRESS_ATE"},
                        {"name": "VGASTHONPROSIGV_ATE", "dataType": "double", "sourceColumn": "VGASTHONPROSIGV_ATE"},
                        {"name": "VGASTPRODOSIGV_ATE", "dataType": "double", "sourceColumn": "VGASTPRODOSIGV_ATE"},
                        {"name": "VGASTHTSCLITOPSIGV_ATE", "dataType": "double", "sourceColumn": "VGASTHTSCLITOPSIGV_ATE"},
                        {"name": "VGASTEXAUXLABSIGV_ATE", "dataType": "double", "sourceColumn": "VGASTEXAUXLABSIGV_ATE"},
                        {"name": "VGASTEXAUXIMGSIGV_ATE", "dataType": "double", "sourceColumn": "VGASTEXAUXIMGSIGV_ATE"},
                        {"name": "VGASTFARINSSIGV_ATE", "dataType": "double", "sourceColumn": "VGASTFARINSSIGV_ATE"},
                        {"name": "VGASTPROTSIGV_ATE", "dataType": "double", "sourceColumn": "VGASTPROTSIGV_ATE"},
                        {"name": "VGASTMEDEXOIGV_ATE", "dataType": "double", "sourceColumn": "VGASTMEDEXOIGV_ATE"},
                        {"name": "VOGPRESSLDSIGV_ATE", "dataType": "double", "sourceColumn": "VOGPRESSLDSIGV_ATE"},
                        {"name": "VCOPAGOFIJOSIGV_ATE", "dataType": "double", "sourceColumn": "VCOPAGOFIJOSIGV_ATE"},
                        {"name": "VCPAGOFIJOEXIGV_ATE", "dataType": "double", "sourceColumn": "VCPAGOFIJOEXIGV_ATE"},
                        {"name": "VCOPAGOVARSIGV_ATE", "dataType": "double", "sourceColumn": "VCOPAGOVARSIGV_ATE"},
                        {"name": "VCPAGOVAREXIGV_ATE", "dataType": "double", "sourceColumn": "VCPAGOVAREXIGV_ATE"},
                        {"name": "VTOTGASTCUBSIGV_ATE", "dataType": "double", "sourceColumn": "VTOTGASTCUBSIGV_ATE"},
                        {"name": "VTOTLIQIAFAS_ATE", "dataType": "double", "sourceColumn": "VTOTLIQIAFAS_ATE"},
                        {"name": "DFECRECEP_PQ", "dataType": "dateTime", "sourceColumn": "DFECRECEP_PQ"},
                        {"name": "UBIGEO_AFILIADO", "dataType": "string", "sourceColumn": "UBIGEO_AFILIADO"},
                        {"name": "Tipo_Cobertura_Desc", "dataType": "string", "sourceColumn": "Tipo_Cobertura_Desc"},
                        {"name": "Sexo_Desc", "dataType": "string", "sourceColumn": "Sexo_Desc"},
                        {"name": "Tipo_Afiliacion_Desc", "dataType": "string", "sourceColumn": "Tipo_Afiliacion_Desc"},
                        {"name": "Total_Copago", "dataType": "double", "sourceColumn": "Total_Copago"}
                    ],
                    "partitions": [
                        {
                            "name": "AtencionesSaludPrivada",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [line + "\n" for line in m_code.split("\n")]
                            }
                        }
                    ],
                    "measures": [
                        {
                            "name": "Total Atenciones",
                            "expression": "COUNTROWS('AtencionesSaludPrivada')",
                            "formatString": "#,0"
                        },
                        {
                            "name": "Total Facturado IAFAS",
                            "expression": "SUM('AtencionesSaludPrivada'[VTOTLIQIAFAS_ATE])",
                            "formatString": "\"S/.\" #,0.00"
                        },
                        {
                            "name": "Total Copagos Pacientes",
                            "expression": "SUM('AtencionesSaludPrivada'[Total_Copago])",
                            "formatString": "\"S/.\" #,0.00"
                        },
                        {
                            "name": "Total Gasto Farmacia",
                            "expression": "SUM('AtencionesSaludPrivada'[VGASTFARINSSIGV_ATE])",
                            "formatString": "\"S/.\" #,0.00"
                        },
                        {
                            "name": "Total Gasto Honorarios",
                            "expression": "SUM('AtencionesSaludPrivada'[VGASTHONPROSIGV_ATE])",
                            "formatString": "\"S/.\" #,0.00"
                        }
                    ]
                }
            ]
        }
    }

    # 7. REPORT LAYOUT JSON (Sections & Visuals)
    layout_obj = {
        "id": 0,
        "resourcePackages": [],
        "sections": [
            {
                "id": 0,
                "name": "Section1",
                "displayName": "Dashboard 1 - Indicadores Financieros",
                "ordinal": 0,
                "visualContainers": [
                    {
                        "x": 20, "y": 20, "z": 1000, "width": 1240, "height": 60,
                        "config": json.dumps({
                            "name": "Title1",
                            "layouts": [{"id": 0, "position": {"x": 20, "y": 20, "z": 1000, "width": 1240, "height": 60}}],
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [{"value": "DASHBOARD FINANCIERO: PRESTACIONES DE SALUD PRIVADA (SUSALUD / TEDEF)", "textStyle": {"fontSize": "20pt", "fontFamily": "Segoe UI Semibold", "color": "#003366"}}]}]}}]}
                            }
                        })
                    },
                    {
                        "x": 20, "y": 100, "z": 1001, "width": 380, "height": 130,
                        "config": json.dumps({
                            "name": "CardTotalFacturado",
                            "layouts": [{"id": 0, "position": {"x": 20, "y": 100, "z": 1001, "width": 380, "height": 130}}],
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "AtencionesSaludPrivada.Total Facturado IAFAS"}]}
                            }
                        })
                    },
                    {
                        "x": 450, "y": 100, "z": 1002, "width": 380, "height": 130,
                        "config": json.dumps({
                            "name": "CardTotalCopagos",
                            "layouts": [{"id": 0, "position": {"x": 450, "y": 100, "z": 1002, "width": 380, "height": 130}}],
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "AtencionesSaludPrivada.Total Copagos Pacientes"}]}
                            }
                        })
                    },
                    {
                        "x": 880, "y": 100, "z": 1003, "width": 380, "height": 130,
                        "config": json.dumps({
                            "name": "CardTotalAtenciones",
                            "layouts": [{"id": 0, "position": {"x": 880, "y": 100, "z": 1003, "width": 380, "height": 130}}],
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "AtencionesSaludPrivada.Total Atenciones"}]}
                            }
                        })
                    },
                    {
                        "x": 20, "y": 250, "z": 1004, "width": 700, "height": 430,
                        "config": json.dumps({
                            "name": "BarFacturadoPorCobertura",
                            "layouts": [{"id": 0, "position": {"x": 20, "y": 250, "z": 1004, "width": 700, "height": 430}}],
                            "singleVisual": {
                                "visualType": "columnChart",
                                "projections": {
                                    "Category": [{"queryRef": "AtencionesSaludPrivada.Tipo_Cobertura_Desc"}],
                                    "Y": [{"queryRef": "AtencionesSaludPrivada.Total Facturado IAFAS"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 750, "y": 250, "z": 1005, "width": 510, "height": 430,
                        "config": json.dumps({
                            "name": "DonutGastoPorRubro",
                            "layouts": [{"id": 0, "position": {"x": 750, "y": 250, "z": 1005, "width": 510, "height": 430}}],
                            "singleVisual": {
                                "visualType": "pieChart",
                                "projections": {
                                    "Category": [{"queryRef": "AtencionesSaludPrivada.Tipo_Afiliacion_Desc"}],
                                    "Y": [{"queryRef": "AtencionesSaludPrivada.Total Facturado IAFAS"}]
                                }
                            }
                        })
                    }
                ]
            },
            {
                "id": 1,
                "name": "Section2",
                "displayName": "Dashboard 2 - Análisis Clínico y Demográfico",
                "ordinal": 1,
                "visualContainers": [
                    {
                        "x": 20, "y": 20, "z": 2000, "width": 1240, "height": 60,
                        "config": json.dumps({
                            "name": "Title2",
                            "layouts": [{"id": 0, "position": {"x": 20, "y": 20, "z": 2000, "width": 1240, "height": 60}}],
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [{"value": "ANÁLISIS DEMOGRÁFICO Y MORBILIDAD (CIE-10 / PACIENTES)", "textStyle": {"fontSize": "20pt", "fontFamily": "Segoe UI Semibold", "color": "#003366"}}]}]}}]}
                            }
                        })
                    },
                    {
                        "x": 20, "y": 100, "z": 2001, "width": 450, "height": 580,
                        "config": json.dumps({
                            "name": "DonutSexo",
                            "layouts": [{"id": 0, "position": {"x": 20, "y": 100, "z": 2001, "width": 450, "height": 580}}],
                            "singleVisual": {
                                "visualType": "donutChart",
                                "projections": {
                                    "Category": [{"queryRef": "AtencionesSaludPrivada.Sexo_Desc"}],
                                    "Y": [{"queryRef": "AtencionesSaludPrivada.Total Atenciones"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 500, "y": 100, "z": 2002, "width": 760, "height": 580,
                        "config": json.dumps({
                            "name": "BarTopDiagnosticos",
                            "layouts": [{"id": 0, "position": {"x": 500, "y": 100, "z": 2002, "width": 760, "height": 580}}],
                            "singleVisual": {
                                "visualType": "barChart",
                                "projections": {
                                    "Category": [{"queryRef": "AtencionesSaludPrivada.VPRIDIAGCIE_ATE"}],
                                    "Y": [{"queryRef": "AtencionesSaludPrivada.Total Atenciones"}]
                                }
                            }
                        })
                    }
                ]
            },
            {
                "id": 2,
                "name": "Section3",
                "displayName": "Reporte Tabla - Detalle de Atenciones",
                "ordinal": 2,
                "visualContainers": [
                    {
                        "x": 20, "y": 20, "z": 3000, "width": 1240, "height": 60,
                        "config": json.dumps({
                            "name": "Title3",
                            "layouts": [{"id": 0, "position": {"x": 20, "y": 20, "z": 3000, "width": 1240, "height": 60}}],
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [{"value": "REPORTE DETALLADO CON SEGMENTACIÓN (FILTROS)", "textStyle": {"fontSize": "20pt", "fontFamily": "Segoe UI Semibold", "color": "#003366"}}]}]}}]}
                            }
                        })
                    },
                    {
                        "x": 20, "y": 90, "z": 3001, "width": 380, "height": 130,
                        "config": json.dumps({
                            "name": "SlicerCobertura",
                            "layouts": [{"id": 0, "position": {"x": 20, "y": 90, "z": 3001, "width": 380, "height": 130}}],
                            "singleVisual": {
                                "visualType": "slicer",
                                "projections": {
                                    "Values": [{"queryRef": "AtencionesSaludPrivada.Tipo_Cobertura_Desc"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 420, "y": 90, "z": 3002, "width": 380, "height": 130,
                        "config": json.dumps({
                            "name": "SlicerSexo",
                            "layouts": [{"id": 0, "position": {"x": 420, "y": 90, "z": 3002, "width": 380, "height": 130}}],
                            "singleVisual": {
                                "visualType": "slicer",
                                "projections": {
                                    "Values": [{"queryRef": "AtencionesSaludPrivada.Sexo_Desc"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 820, "y": 90, "z": 3003, "width": 440, "height": 130,
                        "config": json.dumps({
                            "name": "SlicerAfiliacion",
                            "layouts": [{"id": 0, "position": {"x": 820, "y": 90, "z": 3003, "width": 440, "height": 130}}],
                            "singleVisual": {
                                "visualType": "slicer",
                                "projections": {
                                    "Values": [{"queryRef": "AtencionesSaludPrivada.Tipo_Afiliacion_Desc"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 20, "y": 240, "z": 3004, "width": 1240, "height": 450,
                        "config": json.dumps({
                            "name": "TableDetalleAtenciones",
                            "layouts": [{"id": 0, "position": {"x": 20, "y": 240, "z": 3004, "width": 1240, "height": 450}}],
                            "singleVisual": {
                                "visualType": "tableEx",
                                "projections": {
                                    "Values": [
                                        {"queryRef": "AtencionesSaludPrivada.VCORRPRESTA_ATE"},
                                        {"queryRef": "AtencionesSaludPrivada.VFECPRES_ATE"},
                                        {"queryRef": "AtencionesSaludPrivada.VPRIDIAGCIE_ATE"},
                                        {"queryRef": "AtencionesSaludPrivada.Tipo_Cobertura_Desc"},
                                        {"queryRef": "AtencionesSaludPrivada.Tipo_Afiliacion_Desc"},
                                        {"queryRef": "AtencionesSaludPrivada.Sexo_Desc"},
                                        {"queryRef": "AtencionesSaludPrivada.VGASTHONPROSIGV_ATE"},
                                        {"queryRef": "AtencionesSaludPrivada.VGASTFARINSSIGV_ATE"},
                                        {"queryRef": "AtencionesSaludPrivada.Total_Copago"},
                                        {"queryRef": "AtencionesSaludPrivada.VTOTLIQIAFAS_ATE"}
                                    ]
                                }
                            }
                        })
                    }
                ]
            }
        ]
    }

    layout_json_str = json.dumps(layout_obj, indent=2)
    schema_json_str = json.dumps(data_model_schema, indent=2)

    # -------------------------------------------------------------
    # BUILD .PBIT (Power BI Template)
    # -------------------------------------------------------------
    pbit_path = os.path.join(pbi_dir, "Reporte_Atenciones_Salud_Privada.pbit")
    with zipfile.ZipFile(pbit_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types_xml.encode("utf-8"))
        z.writestr("Version", version_str.encode("utf-16le"))
        z.writestr("Settings", settings_json.encode("utf-16le"))
        z.writestr("Metadata", metadata_json.encode("utf-16le"))
        z.writestr("DiagramLayout", diagram_json.encode("utf-16le"))
        z.writestr("DataModelSchema", schema_json_str.encode("utf-16le"))
        z.writestr("Report/Layout", layout_json_str.encode("utf-16le"))

    print(f"Created Power BI Template: {pbit_path}")

    # -------------------------------------------------------------
    # BUILD .PBIX (Power BI Report file)
    # -------------------------------------------------------------
    pbix_path = os.path.join(pbi_dir, "Reporte_Atenciones_Salud_Privada.pbix")
    with zipfile.ZipFile(pbix_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types_xml.encode("utf-8"))
        z.writestr("Version", version_str.encode("utf-16le"))
        z.writestr("Settings", settings_json.encode("utf-16le"))
        z.writestr("Metadata", metadata_json.encode("utf-16le"))
        z.writestr("DiagramLayout", diagram_json.encode("utf-16le"))
        z.writestr("DataModelSchema", schema_json_str.encode("utf-16le"))
        z.writestr("Report/Layout", layout_json_str.encode("utf-16le"))

    print(f"Created Power BI Report (.pbix): {pbix_path}")

    # -------------------------------------------------------------
    # BUILD .PBIP (Modern Power BI Project structure)
    # -------------------------------------------------------------
    pbip_proj_file = os.path.join(pbi_dir, "Reporte_Atenciones_Salud_Privada.pbip")
    with open(pbip_proj_file, "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0",
            "artifacts": [
                {
                    "report": {
                        "path": "Reporte_Atenciones_Salud_Privada.Report"
                    }
                }
            ],
            "settings": {
                "enableAutoAuth": True
            }
        }, f, indent=2)

    # Report folder
    report_folder = os.path.join(pbi_dir, "Reporte_Atenciones_Salud_Privada.Report")
    os.makedirs(report_folder, exist_ok=True)
    with open(os.path.join(report_folder, "definition.pbir"), "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0",
            "datasetReference": {
                "byPath": {
                    "path": "../Reporte_Atenciones_Salud_Privada.Dataset"
                },
                "byConnection": None
            }
        }, f, indent=2)

    with open(os.path.join(report_folder, "report.json"), "w", encoding="utf-8") as f:
        f.write(layout_json_str)

    # Dataset folder
    dataset_folder = os.path.join(pbi_dir, "Reporte_Atenciones_Salud_Privada.Dataset")
    os.makedirs(dataset_folder, exist_ok=True)
    with open(os.path.join(dataset_folder, "definition.pbism"), "w", encoding="utf-8") as f:
        json.dump({"version": "1.0"}, f, indent=2)

    with open(os.path.join(dataset_folder, "model.bim"), "w", encoding="utf-8") as f:
        f.write(schema_json_str)

    print("Created PBIP project files successfully.")

if __name__ == "__main__":
    build_pbi_bundle()
