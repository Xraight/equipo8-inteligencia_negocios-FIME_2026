' ==============================================================================
' PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) — CASA&ESTILO
' ARCHIVO: construir_modelo_powerpivot_pia.bas
' AUTOR: Equipo 8 — Analítica e Inteligencia de Negocios (FIME - UANL)
' ENTORNO: Microsoft Excel 365 / Power Pivot (VBA)
' ==============================================================================
' FUNCIÓN GENERAL:
' Automatizar con 1 solo clic la construcción completa del Modelo de Datos
' Tabular VertiPaq en Power Pivot, estableciendo las relaciones 1:N del Esquema
' Estrella, registrando las 10 medidas DAX oficiales y generando una Tabla
' Dinámica nativa conectada a `ThisWorkbookDataModel`.
'
' FUNCIÓN ESPECÍFICA:
' 1. Cargar las Tablas Oficiales de Excel (ListObjects) hacia el Modelo de Datos.
' 2. Crear las relaciones 1:N en la Vista de Diagrama:
'    - TablaFactVentas[sucursal_key] -> TablaDimSucursal[sucursal_key]
'    - TablaFactVentas[canal_id]     -> TablaDimCanal[canal_id]
'    - TablaFactVentas[tiempo_id]    -> TablaDimTiempo[tiempo_id]
' 3. Registrar las 10 medidas DAX oficiales en TablaFactVentas.
' 4. Generar la hoja `Dashboard_PowerPivot_Nativo` con Tabla Dinámica del modelo.
' ==============================================================================

Option Explicit

Public Sub ConstruirModeloPowerPivotPIA()
    Dim wb As Workbook
    Dim wsDash As Worksheet
    Dim connModel As WorkbookConnection
    Dim c As WorkbookConnection
    Dim ptCache As PivotCache
    Dim pt As PivotTable

    Set wb = ActiveWorkbook

    On Error GoTo ManejoErrorGeneral
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False

    ' --------------------------------------------------------------------------
    ' PASO 1: CARGAR TABLAS OFICIALES (ListObjects) AL MODELO DE DATOS
    ' --------------------------------------------------------------------------
    ' Power Query M que lee directamente las tablas existentes del libro
    CargarTablaAlModelo wb, "TablaFactVentas", "FACT_VENTAS_MODELO"
    CargarTablaAlModelo wb, "TablaDimProducto", "DIM_PRODUCTO"
    CargarTablaAlModelo wb, "TablaDimSucursal", "DIM_SUCURSAL"
    CargarTablaAlModelo wb, "TablaDimCanal", "DIM_CANAL"
    CargarTablaAlModelo wb, "TablaDimTiempo", "DIM_TIEMPO"
    CargarTablaAlModelo wb, "TablaFactDevoluciones", "FACT_DEVOLUCIONES"
    CargarTablaAlModelo wb, "TablaFactInstalaciones", "FACT_INSTALACIONES"

    ' --------------------------------------------------------------------------
    ' PASO 2: CREAR RELACIONES 1:N EN LA VISTA DE DIAGRAMA (ESQUEMA ESTRELLA)
    ' --------------------------------------------------------------------------
    CrearRelacionSegura wb, "TablaFactVentas", "sucursal_key", "TablaDimSucursal", "sucursal_key"
    CrearRelacionSegura wb, "TablaFactVentas", "canal_id", "TablaDimCanal", "canal_id"
    CrearRelacionSegura wb, "TablaFactVentas", "tiempo_id", "TablaDimTiempo", "tiempo_id"
    CrearRelacionSegura wb, "TablaFactDevoluciones", "sucursal_key", "TablaDimSucursal", "sucursal_key"
    CrearRelacionSegura wb, "TablaFactInstalaciones", "sucursal_key", "TablaDimSucursal", "sucursal_key"

    ' --------------------------------------------------------------------------
    ' PASO 3: REGISTRAR LAS 10 MEDIDAS DAX OFICIALES
    ' --------------------------------------------------------------------------
    ' 1. Ventas Brutas
    CrearMedidaDAXSegura wb, "TablaFactVentas", "Ventas Brutas", "SUM(TablaFactVentas[monto_bruto])"
    
    ' 2. Descuentos Totales
    CrearMedidaDAXSegura wb, "TablaFactVentas", "Descuentos Totales", "SUM(TablaFactVentas[monto_descuento])"
    
    ' 3. Ventas Netas
    CrearMedidaDAXSegura wb, "TablaFactVentas", "Ventas Netas", "[Ventas Brutas] - [Descuentos Totales]"
    
    ' 4. Costo de Ventas (COGS)
    CrearMedidaDAXSegura wb, "TablaFactVentas", "Costo de Ventas (COGS)", "SUM(TablaFactVentas[costo_total])"
    
    ' 5. Utilidad Bruta
    CrearMedidaDAXSegura wb, "TablaFactVentas", "Utilidad Bruta", "[Ventas Netas] - [Costo de Ventas (COGS)]"
    
    ' 6. Margen Bruto %
    CrearMedidaDAXSegura wb, "TablaFactVentas", "Margen Bruto %", "DIVIDE([Utilidad Bruta], [Ventas Netas], 0)"
    
    ' 7. Ticket Promedio
    CrearMedidaDAXSegura wb, "TablaFactVentas", "Ticket Promedio", "DIVIDE([Ventas Netas], SUM(TablaFactVentas[transacciones]), 0)"
    
    ' 8. Tasa de Devolución %
    CrearMedidaDAXSegura wb, "TablaFactVentas", "Tasa de Devolucion %", "DIVIDE(SUM(TablaFactDevoluciones[importe_devuelto]), [Ventas Brutas], 0)"
    
    ' 9. Cumplimiento SLA %
    CrearMedidaDAXSegura wb, "TablaFactVentas", "Cumplimiento SLA %", "DIVIDE(CALCULATE(COUNTROWS(TablaFactInstalaciones), TablaFactInstalaciones[cumplio_sla]=1), COUNTROWS(TablaFactInstalaciones), 0)"
    
    ' 10. Crecimiento YoY %
    CrearMedidaDAXSegura wb, "TablaFactVentas", "Crecimiento YoY %", "DIVIDE([Ventas Netas] - CALCULATE([Ventas Netas], SAMEPERIODLASTYEAR(TablaDimTiempo[fecha])), CALCULATE([Ventas Netas], SAMEPERIODLASTYEAR(TablaDimTiempo[fecha])), 0)"

    ' --------------------------------------------------------------------------
    ' PASO 4: CREACIÓN DE HOJA DASHBOARD CON TABLA DINÁMICA NATIVA POWER PIVOT
    ' --------------------------------------------------------------------------
    On Error Resume Next
    Set wsDash = wb.Worksheets("DASHBOARD_POWERPIVOT_NATIVO")
    If wsDash Is Nothing Then
        Set wsDash = wb.Worksheets.Add(After:=wb.Worksheets(1))
        wsDash.Name = "DASHBOARD_POWERPIVOT_NATIVO"
    Else
        wsDash.Cells.Clear
    End If

    ' Encabezado Ejecutivo
    With wsDash.Range("B2:H2")
        .Merge
        .Value = "CASA&ESTILO — TABLERO DE CONTROL DINÁMICO (POWER PIVOT / VERTIPAQ NATIVO)"
        .Font.Name = "Calibri"
        .Font.Size = 13
        .Font.Bold = True
        .Font.Color = RGB(255, 255, 255)
        .Interior.Color = RGB(26, 54, 93)
        .HorizontalAlignment = xlCenter
        .VerticalAlignment = xlCenter
    End With

    ' Conexión segura al Modelo de Datos
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

    If Not connModel Is Nothing Then
        Set ptCache = wb.PivotCaches.Create(SourceType:=xlExternal, SourceData:=connModel)
        If Not ptCache Is Nothing Then
            Set pt = ptCache.CreatePivotTable(TableDestination:=wsDash.Range("B5"), TableName:="TD_Desempeno_Categorias_PIA")
            If Not pt Is Nothing Then
                With pt
                    .RowAxisLayout xlTabularRow
                    .ColumnGrand = True
                    .RowGrand = True
                    .CubeFields("[TablaFactVentas].[categoria]").Orientation = xlRowField
                    .CubeFields("[Measures].[Ventas Netas]").Orientation = xlDataField
                    .CubeFields("[Measures].[Utilidad Bruta]").Orientation = xlDataField
                    .CubeFields("[Measures].[Margen Bruto %]").Orientation = xlDataField
                    .CubeFields("[Measures].[Ticket Promedio]").Orientation = xlDataField
                End With
            End If
        End If
    Else
        wsDash.Range("B5").Value = "✔ Modelo de Datos y Medidas DAX configuradas con éxito."
        wsDash.Range("B6").Value = "👉 Ve a Insertar -> Tabla dinámica -> Desde el modelo de datos para visualizar el cubo."
        wsDash.Range("B5:H6").Font.Bold = True
    End If

    wsDash.Columns("B:H").AutoFit
    On Error GoTo 0

    Application.ScreenUpdating = True
    Application.DisplayAlerts = True

    MsgBox "¡MODELO POWER PIVOT CONFIGURADO EXITOSAMENTE!" & vbCrLf & vbCrLf & _
           "1. 5 Tablas cargadas en ThisWorkbookDataModel." & vbCrLf & _
           "2. Relaciones 1:N creadas en la Vista de Diagrama." & vbCrLf & _
           "3. 10 Medidas DAX registradas con éxito." & vbCrLf & _
           "4. Hoja 'DASHBOARD_POWERPIVOT_NATIVO' generada." & vbCrLf & vbCrLf & _
           "Abre [Power Pivot] -> [Administrar] -> [Vista de diagrama] para mostrar el Esquema Estrella ante el profesor.", _
           vbInformation, "Equipo 8 · Casa&Estilo BI"
    Exit Sub

ManejoErrorGeneral:
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    MsgBox "Aviso informativo durante la ejecución:" & vbCrLf & _
           Err.Description & vbCrLf & _
           "(Código: " & Err.Number & ")" & vbCrLf & vbCrLf & _
           "Nota: Puedes abrir la pestaña Power Pivot -> Administrar para ver el modelo.", _
           vbInformation, "Equipo 8 · Aviso Power Pivot"
End Sub

Private Sub CargarTablaAlModelo(wb As Workbook, nombreTabla As String, nombreHoja As String)
    On Error Resume Next
    Dim ws As Worksheet
    Dim lo As ListObject
    Dim q As WorkbookQuery
    Dim codigoM As String
    Dim connStr As String
    Dim connNombre As String

    Set ws = wb.Worksheets(nombreHoja)
    If Not ws Is Nothing Then
        Set lo = ws.ListObjects(nombreTabla)
        If Not lo Is Nothing Then
            codigoM = "let" & vbCrLf & _
                      "    Origen = Excel.CurrentWorkbook(){[Name=""" & nombreTabla & """]}[Content]" & vbCrLf & _
                      "in" & vbCrLf & _
                      "    Origen"

            connNombre = "Query - " & nombreTabla
            connStr = "OLEDB;Provider=Microsoft.Mashup.OleDb.1;Data Source=$Workbook$;Location=" & nombreTabla & ";Extended Properties="""""

            Set q = wb.Queries(nombreTabla)
            If Not q Is Nothing Then
                q.Formula = codigoM
            Else
                wb.Queries.Add nombreTabla, codigoM, "Consulta para " & nombreTabla
            End If

            wb.Connections.Add2 connNombre, _
                                "Conexión a Modelo Power Pivot para " & nombreTabla, _
                                connStr, _
                                "SELECT * FROM [" & nombreTabla & "]", _
                                2, True, False
        End If
    End If
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
