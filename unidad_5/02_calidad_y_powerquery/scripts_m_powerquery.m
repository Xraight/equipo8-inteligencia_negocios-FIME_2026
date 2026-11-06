// ==============================================================================
// CONSULTAS POWER QUERY (LENGUAJE M) · UNIDAD 5 (EQUIPO 8)
// Creado para Excel 365 / Power BI Data Model
// ==============================================================================

// ------------------------------------------------------------------------------
// 1. Consulta: FACT_VENTAS
// ------------------------------------------------------------------------------
let
    Origen = Csv.Document(File.Contents("FACT_VENTAS.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    EncabezadosPromovidos = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    TipoCambiado = Table.TransformColumnTypes(EncabezadosPromovidos, {
        {"id_venta", Int64.Type},
        {"id_producto", Int64.Type},
        {"id_cliente", Int64.Type},
        {"id_tiempo", Int64.Type},
        {"cantidad", Int64.Type},
        {"monto", type number},
        {"costo", type number}
    }),
    FiltroReglasNegocio = Table.SelectRows(TipoCambiado, each [cantidad] > 0 and [monto] >= 0 and [costo] >= 0)
in
    FiltroReglasNegocio

// ------------------------------------------------------------------------------
// 2. Consulta: DIM_PRODUCTO
// ------------------------------------------------------------------------------
let
    Origen = Csv.Document(File.Contents("DIM_PRODUCTO.csv"), [Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    EncabezadosPromovidos = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    TipoCambiado = Table.TransformColumnTypes(EncabezadosPromovidos, {
        {"id_producto", Int64.Type},
        {"producto", type text},
        {"categoria", type text}
    }),
    DuplicadosQuitados = Table.Distinct(TipoCambiado, {"id_producto"})
in
    DuplicadosQuitados

// ------------------------------------------------------------------------------
// 3. Consulta: DIM_CLIENTE
// ------------------------------------------------------------------------------
let
    Origen = Csv.Document(File.Contents("DIM_CLIENTE.csv"), [Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    EncabezadosPromovidos = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    TipoCambiado = Table.TransformColumnTypes(EncabezadosPromovidos, {
        {"id_cliente", Int64.Type},
        {"cliente", type text},
        {"region", type text}
    }),
    DuplicadosQuitados = Table.Distinct(TipoCambiado, {"id_cliente"})
in
    DuplicadosQuitados

// ------------------------------------------------------------------------------
// 4. Consulta: DIM_TIEMPO
// ------------------------------------------------------------------------------
let
    Origen = Csv.Document(File.Contents("DIM_TIEMPO.csv"), [Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    EncabezadosPromovidos = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    TipoCambiado = Table.TransformColumnTypes(EncabezadosPromovidos, {
        {"id_tiempo", Int64.Type},
        {"fecha", type date},
        {"anio", Int64.Type},
        {"mes", Int64.Type}
    }),
    DuplicadosQuitados = Table.Distinct(TipoCambiado, {"id_tiempo"})
in
    DuplicadosQuitados
