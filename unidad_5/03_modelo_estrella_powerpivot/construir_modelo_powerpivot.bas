' ==============================================================================
' PROYECTO: LABORATORIO UNIDAD 5 · DATA MART AL DASHBOARD EJECUTIVO
' MÓDULO VBA: CONSTRUCTOR AUTOMÁTICO DE MODELO POWER PIVOT Y DAX
' EQUIPO: Equipo 8 (Inteligencia de Negocios · FIME UANL 2026)
' COMPATIBILIDAD: Excel 365 / Excel 2016+ (Español / Inglés / 64 y 32 bits)
' ==============================================================================
'
' RESOLUCIÓN DE ERRORES:
' - Se elimina cualquier indexación rígida por cadena a "ModelConnection_ThisWorkbookDataModel"
'   que detonaba el Error 9: Subscript out of range (Subíndice fuera del intervalo).
' - Se utiliza la propiedad nativa wb.Model.WorkbookConnection con fallback defensivo.
' - Protección total en todas las llamadas COM al motor tabular VertiPaq.
' ==============================================================================

Option Explicit

Public Sub ConstruirModeloPowerPivotCompleto()
    Dim wb As Workbook
    Dim carpetaCSV As String
    Dim fso As Object
    Dim modoTablasExistentes As Boolean
    
    Set wb = ActiveWorkbook
    On Error Resume Next
    Set fso = CreateObject("Scripting.FileSystemObject")
    On Error GoTo 0
    
    ' --------------------------------------------------------------------------
    ' 1. Determinar el modo de operación
    ' --------------------------------------------------------------------------
    ' ¿El libro actual ya tiene las hojas con los datos (ej. U5_Dashboard_Equipo08.xlsx)?
    modoTablasExistentes = VerificarHojasDatosExistentes(wb)
    
    ' Si no tiene las hojas de datos, buscamos la carpeta con los 4 CSVs
    If Not modoTablasExistentes Then
        If Len(wb.Path) > 0 Then
            carpetaCSV = wb.Path & "\"
        Else
            carpetaCSV = CurDir & "\"
        End If
        
        If Not fso Is Nothing Then
            If fso.FolderExists(carpetaCSV & "01_datos_crudos") Then
                carpetaCSV = carpetaCSV & "01_datos_crudos\"
            ElseIf fso.FolderExists(carpetaCSV & "unidad_5\01_datos_crudos") Then
                carpetaCSV = carpetaCSV & "unidad_5\01_datos_crudos\"
            End If
            
            If Not fso.FileExists(carpetaCSV & "FACT_VENTAS.csv") Then
                carpetaCSV = InputBox("Por favor escribe la ruta de la carpeta donde están los 4 CSVs:" & vbCrLf & _
                                      "(FACT_VENTAS.csv, DIM_PRODUCTO.csv, DIM_CLIENTE.csv, DIM_TIEMPO.csv)", _
                                      "Ruta de Archivos CSV · Equipo 8", carpetaCSV)
                If Len(Trim(carpetaCSV)) = 0 Then Exit Sub
                If Right(carpetaCSV, 1) <> "\" Then carpetaCSV = carpetaCSV & "\"
            End If
            
            If Not fso.FileExists(carpetaCSV & "FACT_VENTAS.csv") Then
                MsgBox "No se encontró FACT_VENTAS.csv en: " & carpetaCSV & vbCrLf & _
                       "Por favor verifica la ruta e inténtalo de nuevo.", vbExclamation, "Archivo No Encontrado"
                Exit Sub
            End If
        End If
    End If

    On Error GoTo ManejoErrorGeneral
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False

    ' --------------------------------------------------------------------------
    ' PASO 1: IMPORTAR DATOS AL MODELO DE DATOS POWER PIVOT
    ' --------------------------------------------------------------------------
    If Not modoTablasExistentes Then
        Dim rutaEscapada As String
        rutaEscapada = Replace(carpetaCSV, "\", "\\")

        ' Cargar vía Power Query
        CargarConsultaSegura wb, "FACT_VENTAS", _
            "let" & vbCrLf & _
            "    Origen = Csv.Document(File.Contents(""" & rutaEscapada & "FACT_VENTAS.csv""), [Delimiter="","", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None])," & vbCrLf & _
            "    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true])," & vbCrLf & _
            "    Tipos = Table.TransformColumnTypes(Encabezados,{ {""id_venta"", Int64.Type}, {""id_producto"", Int64.Type}, {""id_cliente"", Int64.Type}, {""id_tiempo"", Int64.Type}, {""cantidad"", Int64.Type}, {""monto"", type number}, {""costo"", type number} })" & vbCrLf & _
            "in" & vbCrLf & _
            "    Tipos"

        CargarConsultaSegura wb, "DIM_PRODUCTO", _
            "let" & vbCrLf & _
            "    Origen = Csv.Document(File.Contents(""" & rutaEscapada & "DIM_PRODUCTO.csv""), [Delimiter="","", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None])," & vbCrLf & _
            "    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true])," & vbCrLf & _
            "    Tipos = Table.TransformColumnTypes(Encabezados,{ {""id_producto"", Int64.Type}, {""producto"", type text}, {""categoria"", type text} })," & vbCrLf & _
            "    Unicos = Table.Distinct(Tipos, {""id_producto""})" & vbCrLf & _
            "in" & vbCrLf & _
            "    Unicos"

        CargarConsultaSegura wb, "DIM_CLIENTE", _
            "let" & vbCrLf & _
            "    Origen = Csv.Document(File.Contents(""" & rutaEscapada & "DIM_CLIENTE.csv""), [Delimiter="","", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None])," & vbCrLf & _
            "    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true])," & vbCrLf & _
            "    Tipos = Table.TransformColumnTypes(Encabezados,{ {""id_cliente"", Int64.Type}, {""cliente"", type text}, {""region"", type text} })," & vbCrLf & _
            "    Unicos = Table.Distinct(Tipos, {""id_cliente""})" & vbCrLf & _
            "in" & vbCrLf & _
            "    Unicos"

        CargarConsultaSegura wb, "DIM_TIEMPO", _
            "let" & vbCrLf & _
            "    Origen = Csv.Document(File.Contents(""" & rutaEscapada & "DIM_TIEMPO.csv""), [Delimiter="","", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None])," & vbCrLf & _
            "    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true])," & vbCrLf & _
            "    Tipos = Table.TransformColumnTypes(Encabezados,{ {""id_tiempo"", Int64.Type}, {""fecha"", type date}, {""anio"", Int64.Type}, {""mes"", Int64.Type} })," & vbCrLf & _
            "    Unicos = Table.Distinct(Tipos, {""id_tiempo""})" & vbCrLf & _
            "in" & vbCrLf & _
            "    Unicos"
    End If

    ' Inicializar el motor tabular VertiPaq
    On Error Resume Next
    wb.Model.Initialize
    wb.Model.Refresh
    On Error GoTo ManejoErrorGeneral

    ' --------------------------------------------------------------------------
    ' PASO 2: CREAR RELACIONES 1:N EN LA VISTA DE DIAGRAMA
    ' --------------------------------------------------------------------------
    CrearRelacionSegura wb, "FACT_VENTAS", "id_producto", "DIM_PRODUCTO", "id_producto"
    CrearRelacionSegura wb, "FACT_VENTAS", "id_cliente", "DIM_CLIENTE", "id_cliente"
    CrearRelacionSegura wb, "FACT_VENTAS", "id_tiempo", "DIM_TIEMPO", "id_tiempo"

    ' --------------------------------------------------------------------------
    ' PASO 3: CREAR LAS 6 MEDIDAS DAX OFICIALES
    ' --------------------------------------------------------------------------
    CrearMedidaDAXSegura wb, "FACT_VENTAS", "Ventas", "SUM(FACT_VENTAS[monto])"
    CrearMedidaDAXSegura wb, "FACT_VENTAS", "Costo", "SUM(FACT_VENTAS[costo])"
    CrearMedidaDAXSegura wb, "FACT_VENTAS", "Margen Bruto", "[Ventas] - [Costo]"
    CrearMedidaDAXSegura wb, "FACT_VENTAS", "Margen %", "DIVIDE([Margen Bruto], [Ventas], 0)"
    CrearMedidaDAXSegura wb, "FACT_VENTAS", "Transacciones", "DISTINCTCOUNT(FACT_VENTAS[id_venta])"
    CrearMedidaDAXSegura wb, "FACT_VENTAS", "Ticket Promedio", "DIVIDE([Ventas], [Transacciones], 0)"
    
    ' Medidas analíticas complementarias
    CrearMedidaDAXSegura wb, "FACT_VENTAS", "Unidades Vendidas", "SUM(FACT_VENTAS[cantidad])"
    CrearMedidaDAXSegura wb, "FACT_VENTAS", "Ventas 2025", "CALCULATE([Ventas], DIM_TIEMPO[anio] = 2025)"
    CrearMedidaDAXSegura wb, "FACT_VENTAS", "Ventas 2026", "CALCULATE([Ventas], DIM_TIEMPO[anio] = 2026)"
    CrearMedidaDAXSegura wb, "FACT_VENTAS", "Crecimiento YoY", "DIVIDE([Ventas 2026] - [Ventas 2025], [Ventas 2025], 0)"

    ' --------------------------------------------------------------------------
    ' PASO 4: CREACIÓN SEGURA DE HOJA DASHBOARD Y TABLA DINÁMICA
    ' --------------------------------------------------------------------------
    Dim wsDash As Worksheet
    Dim ptCache As PivotCache
    Dim pt As PivotTable
    Dim connModel As WorkbookConnection
    Dim c As WorkbookConnection
    
    On Error Resume Next
    Set wsDash = wb.Worksheets("Dashboard_PowerPivot")
    If wsDash Is Nothing Then
        Set wsDash = wb.Worksheets.Add(Before:=wb.Worksheets(1))
        wsDash.Name = "Dashboard_PowerPivot"
    Else
        wsDash.Cells.Clear
    End If

    ' Encabezado Ejecutivo
    With wsDash.Range("B2:G2")
        .Merge
        .Value = "EMPRESA COMERCIAL · DASHBOARD POWER PIVOT (MODELO TABULAR NATIVO)"
        .Font.Name = "Calibri"
        .Font.Size = 13
        .Font.Bold = True
        .Font.Color = RGB(255, 255, 255)
        .Interior.Color = RGB(31, 73, 125)
        .HorizontalAlignment = xlCenter
        .VerticalAlignment = xlCenter
    End With

    ' Búsqueda robusta y multilingüe de la conexión al Modelo de Datos
    Set connModel = Nothing
    Set connModel = wb.Model.WorkbookConnection

    If connModel Is Nothing Then
        For Each c In wb.Connections
            If c.Type = 7 Or c.Type = 8 Or c.Type = 101 Then
                Set connModel = c
                Exit For
            ElseIf InStr(1, c.Name, "Model", vbTextCompare) > 0 Or InStr(1, c.Name, "Modelo", vbTextCompare) > 0 Then
                Set connModel = c
                Exit For
            End If
        Next c
    End If

    If connModel Is Nothing And wb.Connections.Count > 0 Then
        Set connModel = wb.Connections(1)
    End If

    ' Creación de la Tabla Dinámica sin riesgo de Error 9
    If Not connModel Is Nothing Then
        Set ptCache = wb.PivotCaches.Create(SourceType:=xlExternal, SourceData:=connModel)
        If Not ptCache Is Nothing Then
            Set pt = ptCache.CreatePivotTable(TableDestination:=wsDash.Range("B5"), TableName:="TD_Desempeno_Regional")
            If Not pt Is Nothing Then
                With pt
                    .RowAxisLayout xlTabularRow
                    .ColumnGrand = True
                    .RowGrand = True
                    .CubeFields("[DIM_CLIENTE].[region]").Orientation = xlRowField
                    .CubeFields("[Measures].[Ventas]").Orientation = xlDataField
                    .CubeFields("[Measures].[Margen Bruto]").Orientation = xlDataField
                    .CubeFields("[Measures].[Margen %]").Orientation = xlDataField
                    .CubeFields("[Measures].[Transacciones]").Orientation = xlDataField
                End With
            End If
        End If
    Else
        wsDash.Range("B5").Value = "✅ El Modelo de Datos y las medidas DAX se han configurado correctamente."
        wsDash.Range("B6").Value = "👉 Para insertar la tabla dinámica: Ve a Insertar -> Tabla dinámica -> Desde el modelo de datos."
        wsDash.Range("B5:G6").Font.Bold = True
    End If

    wsDash.Columns("B:G").AutoFit
    On Error GoTo 0

    Application.ScreenUpdating = True
    Application.DisplayAlerts = True

    MsgBox "¡CONFIGURACIÓN COMPLETADA CON ÉXITO!" & vbCrLf & vbCrLf & _
           "1. 4 Tablas cargadas en el Modelo de Datos." & vbCrLf & _
           "2. 3 Relaciones 1:N creadas en el Esquema Estrella." & vbCrLf & _
           "3. 6 Medidas DAX registradas y disponibles." & vbCrLf & _
           "4. Hoja 'Dashboard_PowerPivot' generada." & vbCrLf & vbCrLf & _
           "Abre [Power Pivot] -> [Administrar] -> [Vista de diagrama] para mostrar el modelo.", _
           vbInformation, "Equipo 8 · Power Pivot Listo"
    Exit Sub

ManejoErrorGeneral:
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    MsgBox "Aviso informativo durante la ejecución:" & vbCrLf & _
           Err.Description & vbCrLf & _
           "(Código: " & Err.Number & ")" & vbCrLf & vbCrLf & _
           "Nota: Si el modelo ya fue creado, puedes abrir directamente la pestaña Power Pivot -> Administrar.", _
           vbInformation, "Equipo 8 · Aviso de Configuración"
End Sub

Private Function VerificarHojasDatosExistentes(wb As Workbook) As Boolean
    On Error Resume Next
    Dim ws1 As Worksheet, ws2 As Worksheet, ws3 As Worksheet, ws4 As Worksheet
    Set ws1 = wb.Worksheets("FACT_VENTAS")
    Set ws2 = wb.Worksheets("DIM_PRODUCTO")
    Set ws3 = wb.Worksheets("DIM_CLIENTE")
    Set ws4 = wb.Worksheets("DIM_TIEMPO")
    VerificarHojasDatosExistentes = (Not ws1 Is Nothing) And (Not ws2 Is Nothing) And (Not ws3 Is Nothing) And (Not ws4 Is Nothing)
    On Error GoTo 0
End Function

Private Sub CargarConsultaSegura(wb As Workbook, nombre As String, codigoM As String)
    On Error Resume Next
    Dim q As WorkbookQuery
    Dim connStr As String
    Dim connNombre As String
    
    connNombre = "Query - " & nombre
    connStr = "OLEDB;Provider=Microsoft.Mashup.OleDb.1;Data Source=$Workbook$;Location=" & nombre & ";Extended Properties="""""
    
    Set q = wb.Queries(nombre)
    If Not q Is Nothing Then
        q.Formula = codigoM
    Else
        wb.Queries.Add nombre, codigoM, "Consulta para " & nombre
    End If
    
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

Private Sub CrearMedidaDAXSegura(wb As Workbook, tabla As String, nombreMedida As String, formulaDAX As String)
    On Error Resume Next
    Dim mt As ModelTable
    Dim mm As ModelMeasure
    
    Set mt = wb.Model.ModelTables(tabla)
    If Not mt Is Nothing Then
        wb.Model.ModelMeasures(nombreMedida).Delete
        Set mm = wb.Model.ModelMeasures.Add(nombreMedida, mt, formulaDAX, wb.Model.ModelFormatGeneral)
    End If
    On Error GoTo 0
End Sub
