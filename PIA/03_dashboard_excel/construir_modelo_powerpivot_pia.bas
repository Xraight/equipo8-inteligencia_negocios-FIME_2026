Attribute VB_Name = "ModuloPowerPivotPIA"
' ==============================================================================
' PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
' ARCHIVO: construir_modelo_powerpivot_pia.bas
' AUTOR: Equipo 8 - Analitica e Inteligencia de Negocios (FIME - UANL)
' ENTORNO: Microsoft Excel 365 / Power Pivot (VBA)
' CODIFICACION: ANSI / Windows-1252 (Compatible nativo con Editor VBA)
' ==============================================================================
' FUNCION GENERAL:
' Automatiza la construccion del Modelo de Datos Tabular VertiPaq en Power Pivot:
' 1. Habilita el complemento COM Power Pivot si no estuviera conectado.
' 2. Carga las 7 Tablas Oficiales (ListObjects) al Modelo VertiPaq con sintaxis
'    nativa WORKSHEET (CommandText = [Libro]![Tabla]).
' 3. Crea las relaciones 1:N en la Vista de Diagrama (Esquema Estrella).
' 4. Registra las 10 medidas DAX oficiales de Casa&Estilo.
' 5. Genera la Tabla Dinamica OLAP nativa en B5 con medidas en valores.
' 6. Imprime la bitacora de ejecucion paso a paso en la celda B12 de la hoja.
' ==============================================================================

Option Explicit

Public Sub ConstruirModeloPowerPivotPIA()
    Dim wb As Workbook
    Dim wsDash As Worksheet
    Dim logMensaje As String
    Dim numTablas As Integer
    Dim numRel As Integer
    Dim numDAX As Integer
    Dim ai As COMAddIn

    Set wb = ActiveWorkbook
    logMensaje = ""

    ' --------------------------------------------------------------------------
    ' PASO 0: VERIFICACIONES PREVIAS Y ACTIVACION DE POWER PIVOT COM
    ' --------------------------------------------------------------------------
    If wb.Path = "" Then
        MsgBox "Por favor guarda primero el archivo de Excel (.xlsx o .xlsm) en tu disco local antes de ejecutar la macro.", _
               vbExclamation, "Equipo 8 - Guardar Requerido"
        Exit Sub
    End If

    On Error Resume Next
    For Each ai In Application.COMAddIns
        If ai.Description Like "*Power Pivot*" Or InStr(1, ai.progID, "AnalysisServices", vbTextCompare) > 0 Then
            ai.Connect = True
            Exit For
        End If
    Next ai
    On Error GoTo 0

    Application.ScreenUpdating = False
    Application.DisplayAlerts = False

    ' --------------------------------------------------------------------------
    ' PASO 1: CARGAR TABLAS OFICIALES (ListObjects) AL MODELO VERTIPAQ NATIVO
    ' --------------------------------------------------------------------------
    numTablas = 0
    CargarTablaAlModelo wb, "TablaFactVentas", "FACT_VENTAS_MODELO", numTablas, logMensaje
    CargarTablaAlModelo wb, "TablaDimProducto", "DIM_PRODUCTO", numTablas, logMensaje
    CargarTablaAlModelo wb, "TablaDimSucursal", "DIM_SUCURSAL", numTablas, logMensaje
    CargarTablaAlModelo wb, "TablaDimCanal", "DIM_CANAL", numTablas, logMensaje
    CargarTablaAlModelo wb, "TablaDimTiempo", "DIM_TIEMPO", numTablas, logMensaje
    CargarTablaAlModelo wb, "TablaFactDevoluciones", "FACT_DEVOLUCIONES", numTablas, logMensaje
    CargarTablaAlModelo wb, "TablaFactInstalaciones", "FACT_INSTALACIONES", numTablas, logMensaje

    ' --------------------------------------------------------------------------
    ' PASO 2: CREAR RELACIONES 1:N EN LA VISTA DE DIAGRAMA
    ' --------------------------------------------------------------------------
    numRel = 0
    CrearRelacion wb, "TablaFactVentas", "sucursal_key", "TablaDimSucursal", "sucursal_key", numRel, logMensaje
    CrearRelacion wb, "TablaFactVentas", "canal_id", "TablaDimCanal", "canal_id", numRel, logMensaje
    CrearRelacion wb, "TablaFactVentas", "tiempo_id", "TablaDimTiempo", "tiempo_id", numRel, logMensaje
    CrearRelacion wb, "TablaFactDevoluciones", "sucursal_key", "TablaDimSucursal", "sucursal_key", numRel, logMensaje
    CrearRelacion wb, "TablaFactDevoluciones", "producto_key", "TablaDimProducto", "producto_key", numRel, logMensaje
    CrearRelacion wb, "TablaFactInstalaciones", "sucursal_key", "TablaDimSucursal", "sucursal_key", numRel, logMensaje

    ' --------------------------------------------------------------------------
    ' PASO 3: REGISTRAR LAS 10 MEDIDAS DAX OFICIALES
    ' --------------------------------------------------------------------------
    numDAX = 0
    RegistrarDAX wb, "TablaFactVentas", "Ventas Brutas", "SUM(TablaFactVentas[monto_bruto])", False, True, numDAX, logMensaje
    RegistrarDAX wb, "TablaFactVentas", "Descuentos Totales", "SUM(TablaFactVentas[monto_descuento])", False, True, numDAX, logMensaje
    RegistrarDAX wb, "TablaFactVentas", "Ventas Netas", "[Ventas Brutas] - [Descuentos Totales]", False, True, numDAX, logMensaje
    RegistrarDAX wb, "TablaFactVentas", "Costo de Ventas (COGS)", "SUM(TablaFactVentas[costo_total])", False, True, numDAX, logMensaje
    RegistrarDAX wb, "TablaFactVentas", "Utilidad Bruta", "[Ventas Netas] - [Costo de Ventas (COGS)]", False, True, numDAX, logMensaje
    RegistrarDAX wb, "TablaFactVentas", "Margen Bruto %", "DIVIDE([Utilidad Bruta], [Ventas Netas], 0)", True, False, numDAX, logMensaje
    RegistrarDAX wb, "TablaFactVentas", "Ticket Promedio", "DIVIDE([Ventas Netas], SUM(TablaFactVentas[transacciones]), 0)", False, True, numDAX, logMensaje
    RegistrarDAX wb, "TablaFactVentas", "Tasa de Devolucion %", "DIVIDE(SUM(TablaFactDevoluciones[importe_devuelto]), [Ventas Brutas], 0)", True, False, numDAX, logMensaje
    RegistrarDAX wb, "TablaFactVentas", "Cumplimiento SLA %", "DIVIDE(CALCULATE(COUNTROWS(TablaFactInstalaciones), TablaFactInstalaciones[cumplio_sla]=1), COUNTROWS(TablaFactInstalaciones), 0)", True, False, numDAX, logMensaje
    RegistrarDAX wb, "TablaFactVentas", "Crecimiento YoY %", "DIVIDE([Ventas Netas] - CALCULATE([Ventas Netas], SAMEPERIODLASTYEAR(TablaDimTiempo[fecha])), CALCULATE([Ventas Netas], SAMEPERIODLASTYEAR(TablaDimTiempo[fecha])), 0)", True, False, numDAX, logMensaje

    ' --------------------------------------------------------------------------
    ' PASO 4: CREACION Y FORMATEO DE LA HOJA DASHBOARD NATIVO
    ' --------------------------------------------------------------------------
    On Error Resume Next
    Set wsDash = wb.Worksheets("DASHBOARD_POWERPIVOT_NATIVO")
    If wsDash Is Nothing Then
        Set wsDash = wb.Worksheets.Add(After:=wb.Worksheets(1))
        wsDash.Name = "DASHBOARD_POWERPIVOT_NATIVO"
    Else
        wsDash.Cells.Clear
    End If
    On Error GoTo 0

    ' Banner Superior Ejecutivo
    With wsDash.Range("B2:N2")
        .Merge
        .Value = "CASA&ESTILO - TABLERO DE CONTROL DINAMICO (POWER PIVOT / VERTIPAQ NATIVO)"
        .Font.Name = "Calibri"
        .Font.Size = 13
        .Font.Bold = True
        .Font.Color = RGB(255, 255, 255)
        .Interior.Color = RGB(26, 54, 93)
        .HorizontalAlignment = xlCenter
        .VerticalAlignment = xlCenter
        .RowHeight = 28
    End With

    ' Subtitulo con instruccion clara de defensa
    With wsDash.Range("B3:N3")
        .Merge
        .Value = "Defensa PIA: Abre [Power Pivot] -> [Administrar] -> [Vista de diagrama] para mostrar el Esquema Estrella conectado ante el profesor."
        .Font.Name = "Calibri"
        .Font.Size = 10
        .Font.Italic = True
        .Font.Color = RGB(45, 55, 72)
        .Interior.Color = RGB(237, 242, 247)
        .HorizontalAlignment = xlCenter
        .VerticalAlignment = xlCenter
        .RowHeight = 20
    End With

    ' Construir Tabla Dinamica OLAP desde el Data Model
    If numTablas > 0 Then
        ConstruirTablaDinamicaModelo wb, wsDash, logMensaje
    End If

    ' Reporte de Auditoria y Estado del Modelo en la Hoja
    With wsDash.Range("J5:N5")
        .Merge
        .Value = "ESTADO DEL MODELO DE DATOS (AUDITORIA)"
        .Font.Bold = True
        .Font.Color = RGB(255, 255, 255)
        .Interior.Color = RGB(43, 108, 176)
        .HorizontalAlignment = xlCenter
    End With

    wsDash.Range("J6").Value = "Tablas en Data Model:"
    wsDash.Range("M6").Value = numTablas & " de 7 cargadas"
    wsDash.Range("J7").Value = "Relaciones 1:N creadas:"
    wsDash.Range("M7").Value = numRel & " relaciones activas"
    wsDash.Range("J8").Value = "Medidas DAX oficiales:"
    wsDash.Range("M8").Value = numDAX & " de 10 registradas"
    wsDash.Range("J9").Value = "Motor Tabular:"
    wsDash.Range("M9").Value = "Microsoft VertiPaq (Local)"
    wsDash.Range("J10").Value = "Vista de Diagrama:"
    wsDash.Range("M10").Value = "Power Pivot -> Administrar"
    wsDash.Range("J6:J10").Font.Bold = True
    wsDash.Range("J5:N10").Borders.LineStyle = xlContinuous

    ' Imprimir Bitacora de Auditoria en la Hoja para Transparencia Total
    wsDash.Range("B12:H12").Merge
    wsDash.Range("B12").Value = "BITACORA TECNICA DE EJECUCION (AUDITORIA PASO A PASO):"
    wsDash.Range("B12").Font.Bold = True
    wsDash.Range("B12").Font.Color = RGB(26, 54, 93)

    Dim lineasLog() As String
    lineasLog = Split(logMensaje, vbCrLf)
    Dim k As Long
    For k = 0 To UBound(lineasLog)
        If Trim(lineasLog(k)) <> "" Then
            wsDash.Range("B" & (13 + k) & ":H" & (13 + k)).Merge
            wsDash.Range("B" & (13 + k)).Value = lineasLog(k)
            wsDash.Range("B" & (13 + k)).Font.Size = 9
            If InStr(1, lineasLog(k), "OK", vbTextCompare) > 0 Then
                wsDash.Range("B" & (13 + k)).Font.Color = RGB(47, 133, 90)
            ElseIf InStr(1, lineasLog(k), "ERROR", vbTextCompare) > 0 Or InStr(1, lineasLog(k), "FALLO", vbTextCompare) > 0 Then
                wsDash.Range("B" & (13 + k)).Font.Color = RGB(197, 48, 48)
                wsDash.Range("B" & (13 + k)).Font.Bold = True
            End If
        End If
    Next k

    wsDash.Columns("B:N").AutoFit

    Application.ScreenUpdating = True
    Application.DisplayAlerts = True

    ' --------------------------------------------------------------------------
    ' PASO 5: MENSAJE FINAL AL USUARIO CON DIAGNOSTICO COMPLETO
    ' --------------------------------------------------------------------------
    If numTablas > 0 Then
        MsgBox "CONFIGURACION DE POWER PIVOT FINALIZADA" & vbCrLf & vbCrLf & _
               "- Tablas en Data Model: " & numTablas & " / 7" & vbCrLf & _
               "- Relaciones 1:N: " & numRel & " / 6" & vbCrLf & _
               "- Medidas DAX: " & numDAX & " / 10" & vbCrLf & vbCrLf & _
               "COMO VER EL DIAGRAMA:" & vbCrLf & _
               "1. Haz clic en la pestana 'Power Pivot' de Excel." & vbCrLf & _
               "2. Clic en 'Administrar'." & vbCrLf & _
               "3. Clic en el boton 'Vista de diagrama' (Diagram View)." & vbCrLf & _
               "Ahi veras las tablas como tarjetas unidas con lineas de relacion.", _
               vbInformation, "Equipo 8 - Casa&Estilo Power Pivot"
    Else
        MsgBox "AVISO: Las tablas no pudieron agregarse automaticamente mediante macro." & vbCrLf & _
               "Revisa la bitacora en la fila 12 de esta hoja para ver el detalle." & vbCrLf & vbCrLf & _
               "METODO MANUAL INMEDIATO (2 MINUTOS):" & vbCrLf & _
               "1. Ve a la hoja FACT_VENTAS_MODELO y haz clic dentro de la tabla." & vbCrLf & _
               "2. En la pestana Power Pivot, haz clic en 'Agregar a modelo de datos'." & vbCrLf & _
               "3. Repite en DIM_PRODUCTO, DIM_SUCURSAL, DIM_CANAL y DIM_TIEMPO." & vbCrLf & _
               "4. En Power Pivot pulsa 'Vista de diagrama' para arrastrar las relaciones.", _
               vbExclamation, "Equipo 8 - Modo Manual Recomendado"
    End If
End Sub

' ==============================================================================
' SUBRUTINA: Cargar ListObject al Data Model de forma Segura
' ==============================================================================
Private Sub CargarTablaAlModelo(wb As Workbook, tblName As String, sheetName As String, ByRef contador As Integer, ByRef logMensaje As String)
    Dim ws As Worksheet
    Dim tbl As ListObject
    Dim connName As String
    Dim connStr As String
    Dim cmdText As String
    Dim mt As ModelTable
    Dim yaEnModelo As Boolean
    Dim c As WorkbookConnection
    
    ' 1. Verificar si ya existe en wb.Model
    yaEnModelo = False
    On Error Resume Next
    Set mt = wb.Model.ModelTables(tblName)
    If Not mt Is Nothing Then yaEnModelo = True
    On Error GoTo 0
    
    If yaEnModelo Then
        contador = contador + 1
        logMensaje = logMensaje & "OK: '" & tblName & "' ya se encuentra en el Modelo de Datos." & vbCrLf
        Exit Sub
    End If
    
    ' 2. Verificar existencia de la hoja y la tabla
    On Error Resume Next
    Set ws = wb.Worksheets(sheetName)
    If ws Is Nothing Then
        logMensaje = logMensaje & "ERROR: No existe la hoja '" & sheetName & "'." & vbCrLf
        Exit Sub
    End If
    Set tbl = ws.ListObjects(tblName)
    If tbl Is Nothing Then
        logMensaje = logMensaje & "ERROR: No existe la tabla '" & tblName & "' en hoja '" & sheetName & "'." & vbCrLf
        Exit Sub
    End If
    On Error GoTo 0
    
    ' 3. Limpiar conexion previa con nombre duplicado si existiera
    connName = "WorksheetConnection_" & wb.Name & "!" & tblName
    connStr = "WORKSHEET;" & wb.FullName
    
    On Error Resume Next
    For Each c In wb.Connections
        If c.Name = connName Or c.Name = ("Query - " & tblName) Then
            c.Delete
            Exit For
        End If
    Next c
    Err.Clear
    On Error GoTo 0
    
    ' Metodo 1A: Sintaxis oficial Excel [Libro]![Tabla] con xlCmdTable (7)
    cmdText = wb.Name & "!" & tblName
    On Error Resume Next
    wb.Connections.Add2 _
        Name:=connName, _
        Description:="Data Model para " & tblName, _
        ConnectionString:=connStr, _
        CommandText:=cmdText, _
        lCmdtype:=7, _
        CreateModelConnection:=True, _
        ImportRelationships:=False
        
    If Err.Number = 0 Then
        contador = contador + 1
        logMensaje = logMensaje & "OK: '" & tblName & "' cargada exitosamente via WORKSHEET [Libro]![Tabla]." & vbCrLf
        Exit Sub
    End If
    
    ' Metodo 1B: Sintaxis solo [Tabla]
    Err.Clear
    cmdText = tblName
    wb.Connections.Add2 _
        Name:=connName, _
        Description:="Data Model para " & tblName, _
        ConnectionString:=connStr, _
        CommandText:=cmdText, _
        lCmdtype:=7, _
        CreateModelConnection:=True, _
        ImportRelationships:=False
        
    If Err.Number = 0 Then
        contador = contador + 1
        logMensaje = logMensaje & "OK: '" & tblName & "' cargada exitosamente via WORKSHEET [Tabla]." & vbCrLf
        Exit Sub
    End If

    ' Metodo 1C: Sintaxis [Hoja]![Tabla]
    Err.Clear
    cmdText = sheetName & "!" & tblName
    wb.Connections.Add2 _
        Name:=connName, _
        Description:="Data Model para " & tblName, _
        ConnectionString:=connStr, _
        CommandText:=cmdText, _
        lCmdtype:=7, _
        CreateModelConnection:=True, _
        ImportRelationships:=False
        
    If Err.Number = 0 Then
        contador = contador + 1
        logMensaje = logMensaje & "OK: '" & tblName & "' cargada via WORKSHEET [Hoja]![Tabla]." & vbCrLf
        Exit Sub
    End If

    ' Metodo 2: Fallback via Power Query M
    Dim errDesc As String
    errDesc = Err.Description
    Err.Clear
    Dim mCode As String
    mCode = "let Source = Excel.CurrentWorkbook(){[Name=""" & tblName & """]}[Content] in Source"
    On Error Resume Next
    wb.Queries(tblName).Delete
    Err.Clear
    wb.Queries.Add tblName, mCode
    wb.Connections.Add2 _
        Name:="Query - " & tblName, _
        Description:="PQ Data Model " & tblName, _
        ConnectionString:="OLEDB;Provider=Microsoft.Mashup.OleDb.1;Data Source=$;Location=" & tblName, _
        CommandText:=tblName, _
        lCmdtype:=6, _
        CreateModelConnection:=True, _
        ImportRelationships:=False
        
    If Err.Number = 0 Then
        contador = contador + 1
        logMensaje = logMensaje & "OK: '" & tblName & "' cargada via Power Query M." & vbCrLf
    Else
        logMensaje = logMensaje & "FALLO '" & tblName & "': " & errDesc & " (PQ: " & Err.Description & ")" & vbCrLf
    End If
    On Error GoTo 0
End Sub

' ==============================================================================
' SUBRUTINA: Crear Relaciones 1:N en el Modelo
' ==============================================================================
Private Sub CrearRelacion(wb As Workbook, tablaMuchos As String, colMuchos As String, tablaUno As String, colUno As String, ByRef contador As Integer, ByRef logMensaje As String)
    Dim mtMuchos As ModelTable
    Dim mtUno As ModelTable
    Dim mcMuchos As ModelTableColumn
    Dim mcUno As ModelTableColumn
    Dim rel As ModelRelationship
    
    On Error Resume Next
    For Each rel In wb.Model.ModelRelationships
        If rel.ForeignKeyTable.Name = tablaMuchos And rel.ForeignKeyColumn.Name = colMuchos And _
           rel.PrimaryKeyTable.Name = tablaUno And rel.PrimaryKeyColumn.Name = colUno Then
            contador = contador + 1
            Exit Sub
        End If
    Next rel
    Err.Clear
    
    Set mtMuchos = wb.Model.ModelTables(tablaMuchos)
    Set mtUno = wb.Model.ModelTables(tablaUno)
    
    If mtMuchos Is Nothing Or mtUno Is Nothing Then
        logMensaje = logMensaje & "AVISO Relacion: Tablas " & tablaMuchos & "/" & tablaUno & " no listas." & vbCrLf
        Exit Sub
    End If
    
    Set mcMuchos = mtMuchos.ModelTableColumns(colMuchos)
    Set mcUno = mtUno.ModelTableColumns(colUno)
    
    If mcMuchos Is Nothing Or mcUno Is Nothing Then
        logMensaje = logMensaje & "AVISO Relacion: Columnas " & colMuchos & "/" & colUno & " no encontradas." & vbCrLf
        Exit Sub
    End If
    
    wb.Model.ModelRelationships.Add mcMuchos, mcUno
    If Err.Number = 0 Then
        contador = contador + 1
        logMensaje = logMensaje & "OK Relacion: " & tablaMuchos & "[" & colMuchos & "] -> " & tablaUno & "[" & colUno & "]" & vbCrLf
    Else
        logMensaje = logMensaje & "AVISO Relacion: " & Err.Description & vbCrLf
    End If
    On Error GoTo 0
End Sub

' ==============================================================================
' SUBRUTINA: Registrar Medida DAX con Formato
' ==============================================================================
Private Sub RegistrarDAX(wb As Workbook, tabla As String, nombreMedida As String, formulaDAX As String, esPct As Boolean, esMoneda As Boolean, ByRef contador As Integer, ByRef logMensaje As String)
    Dim mt As ModelTable
    Dim mm As ModelMeasure
    
    On Error Resume Next
    Set mt = wb.Model.ModelTables(tabla)
    If mt Is Nothing Then
        logMensaje = logMensaje & "AVISO DAX: Tabla " & tabla & " no lista para " & nombreMedida & vbCrLf
        Exit Sub
    End If
    
    wb.Model.ModelMeasures(nombreMedida).Delete
    Err.Clear
    
    If esPct Then
        Set mm = wb.Model.ModelMeasures.Add(nombreMedida, mt, formulaDAX, wb.Model.ModelFormatPercentageNumber)
    ElseIf esMoneda Then
        Set mm = wb.Model.ModelMeasures.Add(nombreMedida, mt, formulaDAX, wb.Model.ModelFormatCurrency)
    Else
        Set mm = wb.Model.ModelMeasures.Add(nombreMedida, mt, formulaDAX, wb.Model.ModelFormatGeneral)
    End If
    
    If Err.Number <> 0 Then
        Err.Clear
        Set mm = wb.Model.ModelMeasures.Add(nombreMedida, mt, formulaDAX, wb.Model.ModelFormatGeneral)
    End If
    
    If Err.Number = 0 Then
        contador = contador + 1
        logMensaje = logMensaje & "OK DAX: " & nombreMedida & vbCrLf
    Else
        logMensaje = logMensaje & "AVISO DAX " & nombreMedida & ": " & Err.Description & vbCrLf
    End If
    On Error GoTo 0
End Sub

' ==============================================================================
' SUBRUTINA: Construir Tabla Dinamica Conectada al Modelo
' ==============================================================================
Private Sub ConstruirTablaDinamicaModelo(wb As Workbook, wsDash As Worksheet, ByRef logMensaje As String)
    Dim connModel As WorkbookConnection
    Dim pcCache As PivotCache
    Dim pt As PivotTable
    Dim c As WorkbookConnection
    
    On Error Resume Next
    Set connModel = wb.Model.WorkbookConnection
    If connModel Is Nothing Then
        For Each c In wb.Connections
            If c.Name = "ThisWorkbookDataModel" Or InStr(1, c.Name, "DataModel", vbTextCompare) > 0 Then
                Set connModel = c
                Exit For
            End If
        Next c
    End If
    Err.Clear
    
    If connModel Is Nothing Then
        wsDash.Range("B5").Value = "Aviso: Modelo de Datos VertiPaq activo. Inserta tu Tabla Dinamica desde: Insertar -> Tabla Dinamica -> Desde el Modelo de Datos."
        wsDash.Range("B5:H5").Font.Bold = True
        Exit Sub
    End If
    
    Set pcCache = wb.PivotCaches.Create(SourceType:=xlExternal, SourceData:=connModel, Version:=6)
    If pcCache Is Nothing Then
        Set pcCache = wb.PivotCaches.Create(SourceType:=xlExternal, SourceData:=connModel)
    End If
    
    If Not pcCache Is Nothing Then
        Set pt = pcCache.CreatePivotTable(TableDestination:=wsDash.Range("B5"), TableName:="TD_Desempeno_Categorias_PIA")
        If Not pt Is Nothing Then
            With pt
                .RowAxisLayout xlTabularRow
                .ColumnGrand = True
                .RowGrand = True
                
                ' Fila por Categoria
                On Error Resume Next
                With .CubeFields("[TablaFactVentas].[categoria]")
                    .Orientation = xlRowField
                    .Position = 1
                End With
                
                ' Agregar Medidas usando AddDataField (Metodo OLAP correcto)
                .AddDataField pt.CubeFields("[Measures].[Ventas Netas]"), "Ventas Netas"
                .AddDataField pt.CubeFields("[Measures].[Utilidad Bruta]"), "Utilidad Bruta"
                .AddDataField pt.CubeFields("[Measures].[Margen Bruto %]"), "Margen %"
                .AddDataField pt.CubeFields("[Measures].[Ticket Promedio]"), "Ticket Promedio"
                On Error GoTo 0
            End With
        End If
    End If
    On Error GoTo 0
End Sub
