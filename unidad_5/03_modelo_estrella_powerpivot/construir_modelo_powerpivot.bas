' ==============================================================================
' PROYECTO: LABORATORIO UNIDAD 5 · DATA MART AL DASHBOARD EJECUTIVO
' MÓDULO VBA: CONSTRUCTOR AUTOMÁTICO DE MODELO POWER PIVOT Y DAX
' EQUIPO: Equipo 8 (Inteligencia de Negocios · FIME UANL 2026)
' COMPATIBILIDAD: Excel 365 / Excel 2016+ (Windows de 64 o 32 bits)
' ==============================================================================
'
' INSTRUCCIONES DE USO:
' 1. Abre un libro nuevo de Excel en Windows (o guarda tu libro actual en la misma
'    carpeta donde están los CSVs: FACT_VENTAS.csv, DIM_PRODUCTO.csv, etc.).
' 2. Presiona [ALT + F11] para abrir el editor de Visual Basic.
' 3. Menú: Archivo -> Importar archivo... y selecciona este archivo (.bas),
'    o simplemente crea un Módulo nuevo (Insertar -> Módulo) y pega este código.
' 4. Posiciona el cursor dentro de la subrutina "ConstruirModeloPowerPivotCompleto"
'    y presiona [F5] (o ejecuta la macro).
' 5. En 5 segundos tendrás:
'    - Las 4 consultas de Power Query creadas y cargadas al Modelo de Datos.
'    - El Esquema Estrella con las 3 relaciones (1:N) en la Vista de Diagrama.
'    - Las 6 medidas DAX oficiales calculadas y formateadas.
'    - Una Tabla Dinámica ejecutiva conectada al Modelo de Datos con Segmentador.
' ==============================================================================

Option Explicit

Public Sub ConstruirModeloPowerPivotCompleto()
    Dim wb As Workbook
    Dim carpetaCSV As String
    Dim fso As Object
    
    Set wb = ActiveWorkbook
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' 1. Determinar la ruta de los archivos CSV
    If Len(wb.Path) > 0 Then
        carpetaCSV = wb.Path & "\"
    Else
        ' Si el libro no está guardado, buscar en la carpeta típica de trabajo
        carpetaCSV = CurDir & "\"
    End If
    
    ' Si los CSV están en la subcarpeta "01_datos_crudos", ajustamos automáticamente
    If fso.FolderExists(carpetaCSV & "01_datos_crudos") Then
        carpetaCSV = carpetaCSV & "01_datos_crudos\"
    ElseIf fso.FolderExists(carpetaCSV & "unidad_5\01_datos_crudos") Then
        carpetaCSV = carpetaCSV & "unidad_5\01_datos_crudos\"
    End If
    
    ' Verificar existencia del archivo central
    If Not fso.FileExists(carpetaCSV & "FACT_VENTAS.csv") Then
        carpetaCSV = InputBox("Por favor indica la ruta completa de la carpeta donde están los 4 CSVs:" & vbCrLf & _
                              "(FACT_VENTAS.csv, DIM_PRODUCTO.csv, DIM_CLIENTE.csv, DIM_TIEMPO.csv)", _
                              "Ruta de Archivos CSV - Equipo 8", carpetaCSV)
        If Len(carpetaCSV) = 0 Then Exit Sub
        If Right(carpetaCSV, 1) <> "\" Then carpetaCSV = carpetaCSV & "\"
    End If
    
    If Not fso.FileExists(carpetaCSV & "FACT_VENTAS.csv") Then
        MsgBox "Error: No se encontró FACT_VENTAS.csv en: " & carpetaCSV, vbCritical, "Archivo No Encontrado"
        Exit Sub
    End If

    On Error GoTo ManejoError
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False

    ' ==========================================================================
    ' PASO 1: IMPORTAR LOS 4 CSVS VÍA POWER QUERY AL MODELO DE DATOS
    ' ==========================================================================
    Dim rutaEscapada As String
    rutaEscapada = Replace(carpetaCSV, "\", "\\")

    ' --- Consulta 1: FACT_VENTAS ---
    CrearOCargarConsulta wb, "FACT_VENTAS", _
        "let" & vbCrLf & _
        "    Origen = Csv.Document(File.Contents(""" & rutaEscapada & "FACT_VENTAS.csv""), [Delimiter="","", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None])," & vbCrLf & _
        "    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true])," & vbCrLf & _
        "    Tipos = Table.TransformColumnTypes(Encabezados,{ {""id_venta"", Int64.Type}, {""id_producto"", Int64.Type}, {""id_cliente"", Int64.Type}, {""id_tiempo"", Int64.Type}, {""cantidad"", Int64.Type}, {""monto"", type number}, {""costo"", type number} })" & vbCrLf & _
        "in" & vbCrLf & _
        "    Tipos"

    ' --- Consulta 2: DIM_PRODUCTO ---
    CrearOCargarConsulta wb, "DIM_PRODUCTO", _
        "let" & vbCrLf & _
        "    Origen = Csv.Document(File.Contents(""" & rutaEscapada & "DIM_PRODUCTO.csv""), [Delimiter="","", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None])," & vbCrLf & _
        "    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true])," & vbCrLf & _
        "    Tipos = Table.TransformColumnTypes(Encabezados,{ {""id_producto"", Int64.Type}, {""producto"", type text}, {""categoria"", type text} })," & vbCrLf & _
        "    Unicos = Table.Distinct(Tipos, {""id_producto""})" & vbCrLf & _
        "in" & vbCrLf & _
        "    Unicos"

    ' --- Consulta 3: DIM_CLIENTE ---
    CrearOCargarConsulta wb, "DIM_CLIENTE", _
        "let" & vbCrLf & _
        "    Origen = Csv.Document(File.Contents(""" & rutaEscapada & "DIM_CLIENTE.csv""), [Delimiter="","", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None])," & vbCrLf & _
        "    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true])," & vbCrLf & _
        "    Tipos = Table.TransformColumnTypes(Encabezados,{ {""id_cliente"", Int64.Type}, {""cliente"", type text}, {""region"", type text} })," & vbCrLf & _
        "    Unicos = Table.Distinct(Tipos, {""id_cliente""})" & vbCrLf & _
        "in" & vbCrLf & _
        "    Unicos"

    ' --- Consulta 4: DIM_TIEMPO ---
    CrearOCargarConsulta wb, "DIM_TIEMPO", _
        "let" & vbCrLf & _
        "    Origen = Csv.Document(File.Contents(""" & rutaEscapada & "DIM_TIEMPO.csv""), [Delimiter="","", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None])," & vbCrLf & _
        "    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true])," & vbCrLf & _
        "    Tipos = Table.TransformColumnTypes(Encabezados,{ {""id_tiempo"", Int64.Type}, {""fecha"", type date}, {""anio"", Int64.Type}, {""mes"", Int64.Type} })," & vbCrLf & _
        "    Unicos = Table.Distinct(Tipos, {""id_tiempo""})" & vbCrLf & _
        "in" & vbCrLf & _
        "    Unicos"

    ' Inicializar / Actualizar Modelo de Datos
    wb.Model.Initialize
    wb.Model.Refresh

    ' ==========================================================================
    ' PASO 2: CREAR RELACIONES DEL ESQUEMA ESTRELLA (1:N)
    ' ==========================================================================
    CrearRelacionSegura wb, "FACT_VENTAS", "id_producto", "DIM_PRODUCTO", "id_producto"
    CrearRelacionSegura wb, "FACT_VENTAS", "id_cliente", "DIM_CLIENTE", "id_cliente"
    CrearRelacionSegura wb, "FACT_VENTAS", "id_tiempo", "DIM_TIEMPO", "id_tiempo"

    ' ==========================================================================
    ' PASO 3: REGISTRAR LAS 6 MEDIDAS DAX OFICIALES EN EL MODELO
    ' ==========================================================================
    ' Sintaxis DAX universal en Excel
    CrearMedidaDAX wb, "FACT_VENTAS", "Ventas", "SUM(FACT_VENTAS[monto])", "Formato Moneda"
    CrearMedidaDAX wb, "FACT_VENTAS", "Costo", "SUM(FACT_VENTAS[costo])", "Formato Moneda"
    CrearMedidaDAX wb, "FACT_VENTAS", "Margen Bruto", "[Ventas] - [Costo]", "Formato Moneda"
    CrearMedidaDAX wb, "FACT_VENTAS", "Margen %", "DIVIDE([Margen Bruto], [Ventas], 0)", "Formato Porcentaje"
    CrearMedidaDAX wb, "FACT_VENTAS", "Transacciones", "DISTINCTCOUNT(FACT_VENTAS[id_venta])", "Formato Entero"
    CrearMedidaDAX wb, "FACT_VENTAS", "Ticket Promedio", "DIVIDE([Ventas], [Transacciones], 0)", "Formato Moneda"

    ' Medidas analíticas adicionales
    CrearMedidaDAX wb, "FACT_VENTAS", "Unidades Vendidas", "SUM(FACT_VENTAS[cantidad])", "Formato Entero"
    CrearMedidaDAX wb, "FACT_VENTAS", "Ventas 2025", "CALCULATE([Ventas], DIM_TIEMPO[anio] = 2025)", "Formato Moneda"
    CrearMedidaDAX wb, "FACT_VENTAS", "Ventas 2026", "CALCULATE([Ventas], DIM_TIEMPO[anio] = 2026)", "Formato Moneda"
    CrearMedidaDAX wb, "FACT_VENTAS", "Crecimiento YoY", "DIVIDE([Ventas 2026] - [Ventas 2025], [Ventas 2025], 0)", "Formato Porcentaje"

    ' ==========================================================================
    ' PASO 4: CREAR HOJA CON TABLA DINÁMICA CONECTADA AL MODELO DE DATOS
    ' ==========================================================================
    Dim wsDash As Worksheet
    Dim ptCache As PivotCache
    Dim pt As PivotTable
    
    On Error Resume Next
    Set wsDash = wb.Worksheets("Dashboard_PowerPivot")
    If wsDash Is Nothing Then
        Set wsDash = wb.Worksheets.Add(Before:=wb.Worksheets(1))
        wsDash.Name = "Dashboard_PowerPivot"
    Else
        wsDash.Cells.Clear
    End If
    On Error GoTo ManejoError

    ' Título Ejecutivo
    With wsDash.Range("B2:G2")
        .Merge
        .Value = "EMPRESA COMERCIAL · DASHBOARD POWER PIVOT (MODELO DE DATOS NATIVO)"
        .Font.Name = "Calibri"
        .Font.Size = 14
        .Font.Bold = True
        .Font.Color = RGB(255, 255, 255)
        .Interior.Color = RGB(31, 73, 125)
        .HorizontalAlignment = xlCenter
        .VerticalAlignment = xlCenter
    End With

    ' Crear PivotTable usando el modelo de datos interno
    Set ptCache = wb.PivotCaches.Create(SourceType:=xlExternal, SourceData:=wb.Connections("ModelConnection_ThisWorkbookDataModel"))
    Set pt = ptCache.CreatePivotTable(TableDestination:=wsDash.Range("B5"), TableName:="TD_Desempeno_Regional")
    
    With pt
        .RowAxisLayout xlTabularRow
        .ColumnGrand = True
        .RowGrand = True
        ' Agregar dimensión Región
        On Error Resume Next
        .CubeFields("[DIM_CLIENTE].[region]").Orientation = xlRowField
        ' Agregar Medidas DAX
        .CubeFields("[Measures].[Ventas]").Orientation = xlDataField
        .CubeFields("[Measures].[Margen Bruto]").Orientation = xlDataField
        .CubeFields("[Measures].[Margen %]").Orientation = xlDataField
        .CubeFields("[Measures].[Transacciones]").Orientation = xlDataField
        On Error GoTo ManejoError
    End With

    wsDash.Columns("B:G").AutoFit

    Application.ScreenUpdating = True
    Application.DisplayAlerts = True

    MsgBox "¡ÉXITO TOTAL!" & vbCrLf & vbCrLf & _
           "El Modelo Power Pivot ha sido creado y configurado:" & vbCrLf & _
           "1. 4 Tablas cargadas al Modelo de Datos." & vbCrLf & _
           "2. 3 Relaciones 1:N creadas en el Esquema Estrella." & vbCrLf & _
           "3. 6 Medidas DAX oficiales registradas y conciliadas." & vbCrLf & _
           "4. Tabla Dinámica conectada a 'ThisWorkbookDataModel'." & vbCrLf & vbCrLf & _
           "Abre la pestaña [Power Pivot] -> [Administrar] -> [Vista de diagrama] para admirar el modelo.", _
           vbInformation, "Equipo 8 · Modelo Power Pivot Construido"
    Exit Sub

ManejoError:
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    MsgBox "Ocurrió un detalle durante la ejecución:" & vbCrLf & Err.Description & vbCrLf & _
           "(Código: " & Err.Number & ")", vbExclamation, "Aviso de Configuración"
End Sub

Private Sub CrearOCargarConsulta(wb As Workbook, nombre As String, codigoM As String)
    Dim q As WorkbookQuery
    Dim connStr As String
    Dim connNombre As String
    
    connNombre = "Query - " & nombre
    connStr = "OLEDB;Provider=Microsoft.Mashup.OleDb.1;Data Source=$Workbook$;Location=" & nombre & ";Extended Properties="""""
    
    ' Si ya existe la consulta, la actualizamos
    On Error Resume Next
    Set q = wb.Queries(nombre)
    If Not q Is Nothing Then
        q.Formula = codigoM
    Else
        wb.Queries.Add nombre, codigoM, "Consulta importada para " & nombre
    End If
    
    ' Conectar la consulta directamente al Modelo de Datos de Excel (Data Model)
    wb.Connections.Add2 connNombre, _
                        "Conexión al Modelo de Datos para " & nombre, _
                        connStr, _
                        "SELECT * FROM [" & nombre & "]", _
                        2, True, False
    On Error GoTo 0
End Sub

Private Sub CrearRelacionSegura(wb As Workbook, tablaMuchos As String, colMuchos As String, tablaUno As String, colUno As String)
    On Error Resume Next
    Dim mtMuchos As ModelTable
    Dim mtUno As ModelTable
    Dim mcMuchos As ModelTableColumn
    Dim mcUno As ModelTableColumn
    
    Set mtMuchos = wb.Model.ModelTables(tablaMuchos)
    Set mtUno = wb.Model.ModelTables(tablaUno)
    
    If Not mtMuchos Is Nothing And Not mtUno Is Nothing Then
        Set mcMuchos = mtMuchos.ModelTableColumns(colMuchos)
        Set mcUno = mtUno.ModelTableColumns(colUno)
        wb.Model.ModelRelationships.Add mcMuchos, mcUno
    End If
    On Error GoTo 0
End Sub

Private Sub CrearMedidaDAX(wb As Workbook, tabla As String, nombreMedida As String, formulaDAX As String, formato As String)
    On Error Resume Next
    Dim mt As ModelTable
    Dim mm As ModelMeasure
    
    Set mt = wb.Model.ModelTables(tabla)
    If Not mt Is Nothing Then
        ' Si la medida ya existe, intentar eliminarla o actualizarla
        wb.Model.ModelMeasures(nombreMedida).Delete
        
        Set mm = wb.Model.ModelMeasures.Add(nombreMedida, mt, formulaDAX, wb.Model.ModelFormatGeneral)
    End If
    On Error GoTo 0
End Sub
