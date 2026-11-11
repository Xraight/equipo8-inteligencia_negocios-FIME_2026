// ==============================================================================
// PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) — CASA&ESTILO
// ARCHIVO: scripts_m_powerquery.m
// AUTOR: Equipo 8 — Analítica e Inteligencia de Negocios (FIME - UANL)
// ENTORNO: Power Query (Excel 365 / Power BI Desktop)
// ==============================================================================
// FUNCIÓN GENERAL:
// Código M formal de Power Query para la ingesta, tipado estricto y carga hacia
// el Modelo de Datos Tabular (VertiPaq / Power Pivot) soportando tres vías:
//   1. Tablas Oficiales internas del libro Excel (`Excel.CurrentWorkbook`).
//   2. Archivos CSV exportados en `datos_exportados/` (`Csv.Document`).
//   3. Conexión directa al Data Mart dimensional en MySQL 8.0 (`ce_bi`).
// ==============================================================================

// ------------------------------------------------------------------------------
// 1. INGESTA DESDE TABLAS OFICIALES DEL LIBRO EXCEL (ListObjects)
// ------------------------------------------------------------------------------

// Consulta: TablaFactVentas (331,758 filas atómicas — sin distorsión temporal)
let
    Origen = Excel.CurrentWorkbook(){[Name="TablaFactVentas"]}[Content],
    TipoCambiado = Table.TransformColumnTypes(Origen,{
        {"venta_id", type text},
        {"tiempo_id", Int64.Type},
        {"producto_key", Int64.Type},
        {"cliente_key", Int64.Type},
        {"sucursal_key", Int64.Type},
        {"canal_id", Int64.Type},
        {"metodo_pago_id", Int64.Type},
        {"cantidad", Int64.Type},
        {"monto_bruto", type number},
        {"monto_descuento", type number},
        {"monto_neto", type number},
        {"costo_total", type number},
        {"utilidad_bruta", type number}
    })
in
    TipoCambiado

// Consulta: TablaFactDevoluciones (9,952 filas completas)
let
    Origen = Excel.CurrentWorkbook(){[Name="TablaFactDevoluciones"]}[Content],
    TipoCambiado = Table.TransformColumnTypes(Origen,{
        {"devolucion_id", type text},
        {"venta_id", type text},
        {"tiempo_id", Int64.Type},
        {"producto_key", Int64.Type},
        {"sucursal_key", Int64.Type},
        {"cliente_key", Int64.Type},
        {"cantidad_devuelta", Int64.Type},
        {"importe_devuelto", type number},
        {"motivo", type text}
    })
in
    TipoCambiado

// Consulta: TablaFactInstalaciones (6,500 filas)
let
    Origen = Excel.CurrentWorkbook(){[Name="TablaFactInstalaciones"]}[Content],
    TipoCambiado = Table.TransformColumnTypes(Origen,{
        {"instalacion_id", type text},
        {"venta_id", type text},
        {"tiempo_id", Int64.Type},
        {"cliente_key", Int64.Type},
        {"sucursal_key", Int64.Type},
        {"dias_programados", Int64.Type},
        {"dias_reales", Int64.Type},
        {"dias_desviacion", Int64.Type},
        {"cumplio_sla", Int64.Type},
        {"satisfaccion", type number}
    })
in
    TipoCambiado

// Consulta: TablaFactInventario (21,440 combinaciones tienda-producto)
let
    Origen = Excel.CurrentWorkbook(){[Name="TablaFactInventario"]}[Content],
    TipoCambiado = Table.TransformColumnTypes(Origen,{
        {"sucursal_key", Int64.Type},
        {"producto_key", Int64.Type},
        {"stock_actual", Int64.Type},
        {"punto_reorden", Int64.Type},
        {"deficit_unidades", Int64.Type},
        {"valor_inventario_costo", type number},
        {"estatus_stock", type text}
    })
in
    TipoCambiado

// Consulta: TablaDimTiempo (1,096 días: 2024-01-01 a 2026-12-31)
let
    Origen = Excel.CurrentWorkbook(){[Name="TablaDimTiempo"]}[Content],
    TipoCambiado = Table.TransformColumnTypes(Origen,{
        {"tiempo_id", Int64.Type},
        {"fecha", type date},
        {"anio", Int64.Type},
        {"trimestre", Int64.Type},
        {"trimestre_nombre", type text},
        {"mes", Int64.Type},
        {"mes_nombre", type text},
        {"mes_anio", type text},
        {"semana_anio", Int64.Type},
        {"dia_mes", Int64.Type},
        {"dia_semana", Int64.Type},
        {"dia_semana_nombre", type text},
        {"es_fin_semana", Int64.Type}
    })
in
    TipoCambiado

// Consulta: TablaDimProducto (1,341 registros)
let
    Origen = Excel.CurrentWorkbook(){[Name="TablaDimProducto"]}[Content],
    TipoCambiado = Table.TransformColumnTypes(Origen,{
        {"producto_key", Int64.Type},
        {"producto_id", type text},
        {"sku", type text},
        {"producto", type text},
        {"categoria", type text},
        {"marca", type text},
        {"costo", type number},
        {"precio_lista", type number},
        {"margen_teorico_pct", type number},
        {"activo", type text},
        {"requiere_instalacion", type text}
    })
in
    TipoCambiado

// Consulta: TablaDimSucursal (17 registros)
let
    Origen = Excel.CurrentWorkbook(){[Name="TablaDimSucursal"]}[Content],
    TipoCambiado = Table.TransformColumnTypes(Origen,{
        {"sucursal_key", Int64.Type},
        {"sucursal_id", type text},
        {"sucursal", type text},
        {"ciudad", type text},
        {"estado", type text},
        {"m2", Int64.Type},
        {"categoria_tamano", type text},
        {"fecha_apertura", type date}
    })
in
    TipoCambiado

// Consulta: TablaDimCanal (3 registros)
let
    Origen = Excel.CurrentWorkbook(){[Name="TablaDimCanal"]}[Content],
    TipoCambiado = Table.TransformColumnTypes(Origen,{
        {"canal_id", Int64.Type},
        {"canal_nombre", type text}
    })
in
    TipoCambiado

// Consulta: TablaDimCliente (10,801 registros)
let
    Origen = Excel.CurrentWorkbook(){[Name="TablaDimCliente"]}[Content],
    TipoCambiado = Table.TransformColumnTypes(Origen,{
        {"cliente_key", Int64.Type},
        {"cliente_id", type text},
        {"nombre", type text},
        {"sexo", type text},
        {"fecha_alta", type date},
        {"ciudad", type text},
        {"segmento", type text},
        {"email", type text}
    })
in
    TipoCambiado

// Consulta: TablaDimMetodoPago (4 registros)
let
    Origen = Excel.CurrentWorkbook(){[Name="TablaDimMetodoPago"]}[Content],
    TipoCambiado = Table.TransformColumnTypes(Origen,{
        {"metodo_pago_id", Int64.Type},
        {"metodo_nombre", type text}
    })
in
    TipoCambiado


// ------------------------------------------------------------------------------
// 2. PLANTILLA PARA CARGA DESDE CSV EXPORTADO ("Solo crear conexión + Data Model")
// ------------------------------------------------------------------------------
/*
// Cambia `RutaCarpeta` por la ruta real en Windows donde clonaste el proyecto.
// Ejemplo parametrizado reutilizable para fact_ventas_detalle.csv:
let
    RutaCarpeta = "C:\CasaEstilo\PIA\03_dashboard_excel\datos_exportados\",
    Origen = Csv.Document(File.Contents(RutaCarpeta & "fact_ventas_detalle.csv"), [Delimiter=",", Columns=13, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    TipoCambiado = Table.TransformColumnTypes(Encabezados,{
        {"venta_id", type text}, {"tiempo_id", Int64.Type}, {"producto_key", Int64.Type},
        {"cliente_key", Int64.Type}, {"sucursal_key", Int64.Type}, {"canal_id", Int64.Type},
        {"metodo_pago_id", Int64.Type}, {"cantidad", Int64.Type}, {"monto_bruto", type number},
        {"monto_descuento", type number}, {"monto_neto", type number}, {"costo_total", type number},
        {"utilidad_bruta", type number}
    }, "en-US")
in
    TipoCambiado
*/


// ------------------------------------------------------------------------------
// 3. INGESTA DIRECTA DESDE MYSQL 8.0 (DATA MART ce_bi)
// ------------------------------------------------------------------------------
/*
let
    Origen = MySQL.Database("127.0.0.1:3306", "ce_bi", [ReturnSingleDatabase=true]),
    ce_bi_fact_ventas_detalle = Origen{[Schema="ce_bi",Item="fact_ventas_detalle"]}[Data],
    ce_bi_fact_devoluciones = Origen{[Schema="ce_bi",Item="fact_devoluciones"]}[Data],
    ce_bi_fact_instalaciones = Origen{[Schema="ce_bi",Item="fact_instalaciones"]}[Data],
    ce_bi_fact_inventario_snapshot = Origen{[Schema="ce_bi",Item="fact_inventario_snapshot"]}[Data],
    ce_bi_dim_tiempo = Origen{[Schema="ce_bi",Item="dim_tiempo"]}[Data],
    ce_bi_dim_producto = Origen{[Schema="ce_bi",Item="dim_producto"]}[Data],
    ce_bi_dim_sucursal = Origen{[Schema="ce_bi",Item="dim_sucursal"]}[Data],
    ce_bi_dim_canal = Origen{[Schema="ce_bi",Item="dim_canal"]}[Data],
    ce_bi_dim_cliente = Origen{[Schema="ce_bi",Item="dim_cliente"]}[Data],
    ce_bi_dim_metodo_pago = Origen{[Schema="ce_bi",Item="dim_metodo_pago"]}[Data]
in
    ce_bi_fact_ventas_detalle
*/
