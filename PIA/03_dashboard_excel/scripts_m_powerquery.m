// ==============================================================================
// PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) — CASA&ESTILO
// ARCHIVO: scripts_m_powerquery.m
// AUTOR: Equipo 8 — Analítica e Inteligencia de Negocios (FIME - UANL)
// ENTORNO: Power Query (Excel 365 / Power BI Desktop)
// ==============================================================================
// FUNCIÓN GENERAL:
// Código M formal de Power Query para la ingesta, tipado estricto y carga hacia
// el Modelo de Datos (Data Model) en Power Pivot tanto desde las tablas locales
// de Excel (CurrentWorkbook) como desde el Data Mart en MySQL 8.0 (`ce_bi`).
// ==============================================================================

// ------------------------------------------------------------------------------
// 1. INGESTA DESDE TABLAS OFICIALES DE EXCEL (ListObjects)
// ------------------------------------------------------------------------------

// Consulta: FACT_VENTAS
let
    Origen = Excel.CurrentWorkbook(){[Name="TablaFactVentas"]}[Content],
    TipoCambiado = Table.TransformColumnTypes(Origen,{
        {"tiempo_id", Int64.Type},
        {"mes_anio", type text},
        {"sucursal_key", Int64.Type},
        {"canal_id", Int64.Type},
        {"categoria", type text},
        {"transacciones", Int64.Type},
        {"cantidad", Int64.Type},
        {"monto_bruto", type number},
        {"monto_descuento", type number},
        {"monto_neto", type number},
        {"costo_total", type number},
        {"utilidad_bruta", type number}
    })
in
    TipoCambiado

// Consulta: DIM_PRODUCTO
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

// Consulta: DIM_SUCURSAL
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

// Consulta: DIM_CANAL
let
    Origen = Excel.CurrentWorkbook(){[Name="TablaDimCanal"]}[Content],
    TipoCambiado = Table.TransformColumnTypes(Origen,{
        {"canal_id", Int64.Type},
        {"canal_nombre", type text}
    })
in
    TipoCambiado

// Consulta: DIM_TIEMPO
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


// ------------------------------------------------------------------------------
// 2. INGESTA DIRECTA DESDE MYSQL 8.0 (DATA MART ce_bi)
// ------------------------------------------------------------------------------

/*
// Conexión Directa a MySQL 8.0
let
    Origen = MySQL.Database("127.0.0.1:3306", "ce_bi", [ReturnSingleDatabase=true]),
    ce_bi_fact_ventas_detalle = Origen{[Schema="ce_bi",Item="fact_ventas_detalle"]}[Data],
    ce_bi_dim_producto = Origen{[Schema="ce_bi",Item="dim_producto"]}[Data],
    ce_bi_dim_sucursal = Origen{[Schema="ce_bi",Item="dim_sucursal"]}[Data],
    ce_bi_dim_canal = Origen{[Schema="ce_bi",Item="dim_canal"]}[Data],
    ce_bi_dim_tiempo = Origen{[Schema="ce_bi",Item="dim_tiempo"]}[Data]
in
    ce_bi_fact_ventas_detalle
*/
