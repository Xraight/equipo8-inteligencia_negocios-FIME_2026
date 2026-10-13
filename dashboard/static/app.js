// ==============================================================================
// CASA&ESTILO BI STUDIO - JAVASCRIPT LOGIC
// EQUIPO 8: Arely Carrillo, Rafael Collazo, Sergio Jaziel Butzmann
// ==============================================================================

const API_BASE = '/api';

let currentTable = 'fact_ventas';
let currentOffset = 0;
const PAGE_LIMIT = 50;
let totalTableRows = 0;
let currentSlide = 1;
const TOTAL_SLIDES = 5;
let allTop5Rows = [];

// Predefined SQL queries for the Playground
const SQL_PRESETS = {
  reto: `-- RETO UNIDAD 3: Top 5 Productos Más Rentables por Región (Q2 vs Q1 2026)
WITH rentabilidad_trimestral AS (
    SELECT
        s.zona AS region,
        p.producto_sk,
        p.nombre_producto,
        p.categoria,
        SUM(CASE WHEN t.trimestre = 1 THEN f.ganancia_bruta ELSE 0 END) AS rentabilidad_q1_2026,
        SUM(CASE WHEN t.trimestre = 2 THEN f.ganancia_bruta ELSE 0 END) AS rentabilidad_q2_2026
    FROM Fact_Ventas f
    JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
    JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
    JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
    WHERE t.anio = 2026 AND t.trimestre IN (1, 2)
    GROUP BY s.zona, p.producto_sk, p.nombre_producto, p.categoria
),
ranking_region AS (
    SELECT
        region,
        nombre_producto,
        categoria,
        rentabilidad_q1_2026,
        rentabilidad_q2_2026,
        (rentabilidad_q2_2026 - rentabilidad_q1_2026) AS variacion_absoluta,
        DENSE_RANK() OVER (
            PARTITION BY region 
            ORDER BY rentabilidad_q2_2026 DESC
        ) AS ranking_posicion
    FROM rentabilidad_trimestral
)
SELECT * FROM ranking_region WHERE ranking_posicion <= 5 ORDER BY region, ranking_posicion;`,

  error1055: `-- DEMOSTRACIÓN DE ERROR DE AGRUPACIÓN (SQL Estricto / Error 1055)
-- Esta consulta provoca un error porque selecciona nombre_producto sin agregarlo ni agruparlo
SELECT 
    s.zona AS region,
    p.nombre_producto, -- Columna no incluida en GROUP BY
    SUM(f.monto_venta_neta) AS total_venta_neta
FROM Fact_Ventas f
JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
GROUP BY s.zona;`,

  asesores: `-- COMISIONES Y RENDIMIENTO DE ASESORES
SELECT 
    a.nombre_asesor,
    a.porcentaje_comision,
    COUNT(DISTINCT f.orden_id) AS total_ordenes,
    SUM(f.cantidad) AS unidades_vendidas,
    ROUND(SUM(f.monto_venta_neta), 2) AS total_venta_neta,
    ROUND(SUM(f.monto_venta_neta * (a.porcentaje_comision / 100)), 2) AS comision_acumulada_mxn
FROM Fact_Ventas f
JOIN Dim_Asesor a ON f.asesor_sk = a.asesor_sk
GROUP BY a.nombre_asesor, a.porcentaje_comision
ORDER BY total_venta_neta DESC;`,

  logistica: `-- CUMPLIMIENTO LOGÍSTICO Y PROMEDIO DE RETRASO
SELECT 
    s.nombre_showroom,
    s.ciudad,
    f.tipo_surtido,
    COUNT(*) AS total_pedidos,
    ROUND(AVG(f.dias_para_entrega), 1) AS promedio_dias_entrega,
    ROUND(AVG(CASE WHEN f.retraso_dias > 0 THEN f.retraso_dias ELSE 0 END), 1) AS promedio_dias_retraso,
    ROUND((COUNT(CASE WHEN f.retraso_dias <= 0 THEN 1 END)::NUMERIC / COUNT(*)) * 100, 2) AS pct_cumplimiento_a_tiempo
FROM Fact_Ventas f
JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
WHERE f.fecha_real_entrega_sk IS NOT NULL
GROUP BY s.nombre_showroom, s.ciudad, f.tipo_surtido
ORDER BY s.nombre_showroom, f.tipo_surtido;`,

  categorias: `-- MARGEN Y GANANCIA BRUTA POR CATEGORÍA
SELECT 
    p.categoria,
    COUNT(*) AS renglones_vendidos,
    SUM(f.cantidad) AS volumen_unidades,
    ROUND(SUM(f.monto_venta_neta), 2) AS venta_neta_total,
    ROUND(SUM(f.ganancia_bruta), 2) AS ganancia_bruta_total,
    ROUND((SUM(f.ganancia_bruta) / SUM(f.monto_venta_neta)) * 100, 2) AS margen_bruto_pct
FROM Fact_Ventas f
JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
GROUP BY p.categoria
ORDER BY ganancia_bruta_total DESC;`
};

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initSlideControls();
  fetchDbStatus();
  fetchTablesList();
  fetchTop5Data();
  initSqlPlayground();
  
  document.getElementById('btn-refresh').addEventListener('click', () => {
    fetchDbStatus();
    fetchTablesList();
    fetchTableRows(currentTable, currentOffset);
    fetchTop5Data();
  });

  // Table pagination
  document.getElementById('btn-page-prev').addEventListener('click', () => {
    if (currentOffset >= PAGE_LIMIT) {
      currentOffset -= PAGE_LIMIT;
      fetchTableRows(currentTable, currentOffset);
    }
  });

  document.getElementById('btn-page-next').addEventListener('click', () => {
    if (currentOffset + PAGE_LIMIT < totalTableRows) {
      currentOffset += PAGE_LIMIT;
      fetchTableRows(currentTable, currentOffset);
    }
  });

  // Live filter in table
  document.getElementById('table-search-input').addEventListener('input', (e) => {
    const val = e.target.value.toLowerCase();
    const rows = document.querySelectorAll('#table-container tbody tr');
    rows.forEach(r => {
      r.style.display = r.innerText.toLowerCase().includes(val) ? '' : 'none';
    });
  });

  // Export CSV button
  document.getElementById('btn-export-csv').addEventListener('click', exportTableToCsv);

  // Region filter for Top 5
  document.getElementById('filter-region-select').addEventListener('change', (e) => {
    renderTop5Table(e.target.value);
  });
});

// ==================== TABS SWITCHER ====================
function initTabs() {
  const tabs = document.querySelectorAll('.nav-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      goToTab(tab.getAttribute('data-tab'));
    });
  });
}

function goToTab(tabId) {
  document.querySelectorAll('.nav-tab').forEach(t => {
    t.classList.toggle('active', t.getAttribute('data-tab') === tabId);
  });
  document.querySelectorAll('.tab-panel').forEach(p => {
    p.classList.toggle('active', p.id === tabId);
  });
}

// ==================== SLIDE CONTROLS (PITCH DECK) ====================
function initSlideControls() {
  document.getElementById('slide-prev').addEventListener('click', () => {
    if (currentSlide > 1) {
      currentSlide--;
      updateSlideView();
    }
  });
  document.getElementById('slide-next').addEventListener('click', () => {
    if (currentSlide < TOTAL_SLIDES) {
      currentSlide++;
      updateSlideView();
    }
  });
}

function updateSlideView() {
  document.querySelectorAll('.pitch-slide').forEach(s => {
    s.classList.toggle('active', parseInt(s.getAttribute('data-slide')) === currentSlide);
  });
  document.getElementById('slide-num').innerText = `Paso ${currentSlide} de ${TOTAL_SLIDES}`;
}

// ==================== DB STATUS & STATS ====================
async function fetchDbStatus() {
  try {
    const res = await fetch(`${API_BASE}/status`);
    const data = await res.json();
    const pill = document.getElementById('db-status-pill');
    const text = document.getElementById('db-status-text');

    if (data.status === 'connected') {
      text.innerText = `PostgreSQL 16 Conectado (${data.summary.total_ventas} filas)`;
      pill.style.borderColor = 'rgba(16, 185, 129, 0.4)';
    } else {
      text.innerText = `Error: ${data.message}`;
      pill.style.borderColor = 'rgba(239, 68, 68, 0.4)';
    }
  } catch (err) {
    document.getElementById('db-status-text').innerText = 'Servidor local no disponible';
  }
}

// ==================== TABLES EXPLORER ====================
async function fetchTablesList() {
  try {
    const res = await fetch(`${API_BASE}/tables`);
    const data = await res.json();
    const container = document.getElementById('table-chips-container');
    container.innerHTML = '';

    data.tables.forEach(t => {
      const chip = document.createElement('button');
      chip.className = `table-chip ${t.name === currentTable ? 'active' : ''}`;
      chip.innerHTML = `<span>${t.name}</span> <span class="chip-count">${t.rows}</span>`;
      chip.addEventListener('click', () => {
        currentTable = t.name;
        currentOffset = 0;
        document.querySelectorAll('.table-chip').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        fetchTableRows(t.name, 0);
      });
      container.appendChild(chip);
    });

    fetchTableRows(currentTable, currentOffset);
  } catch (err) {
    console.error('Error fetching tables:', err);
  }
}

async function fetchTableRows(tableName, offset = 0) {
  const container = document.getElementById('table-container');
  container.innerHTML = '<div class="loading-state">Cargando registros...</div>';
  document.getElementById('current-table-title').innerText = tableName;

  try {
    const res = await fetch(`${API_BASE}/table/${tableName}?limit=${PAGE_LIMIT}&offset=${offset}`);
    const data = await res.json();

    totalTableRows = data.total_rows;
    document.getElementById('current-table-badge').innerText = `${data.total_rows} registros totales`;
    
    const pageNum = Math.floor(offset / PAGE_LIMIT) + 1;
    const maxPage = Math.ceil(data.total_rows / PAGE_LIMIT) || 1;
    document.getElementById('page-indicator').innerText = `Página ${pageNum} de ${maxPage}`;

    if (!data.rows || data.rows.length === 0) {
      container.innerHTML = '<div class="empty-state">No se encontraron registros en esta tabla.</div>';
      return;
    }

    let html = '<table class="data-table"><thead><tr>';
    data.columns.forEach(col => {
      html += `<th>${col}</th>`;
    });
    html += '</tr></thead><tbody>';

    data.rows.forEach(row => {
      html += '<tr>';
      data.columns.forEach(col => {
        let val = row[col];
        if (val === null || val === undefined) {
          html += '<td class="text-dim"><em>NULL</em></td>';
        } else if (typeof val === 'number' && (col.includes('monto') || col.includes('ganancia') || col.includes('precio') || col.includes('costo'))) {
          html += `<td class="font-bold">$${parseFloat(val).toLocaleString('es-MX', { minimumFractionDigits: 2 })}</td>`;
        } else if (val === 'Stock') {
          html += `<td><span class="badge badge-stock">Stock</span></td>`;
        } else if (val === 'Sobre pedido') {
          html += `<td><span class="badge badge-pedido">Sobre pedido</span></td>`;
        } else {
          html += `<td>${val}</td>`;
        }
      });
      html += '</tr>';
    });

    html += '</tbody></table>';
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<div class="empty-state text-danger">Error al cargar registros: ${err.message}</div>`;
  }
}

// ==================== RETO UNIDAD 3 (TOP 5) ====================
async function fetchTop5Data() {
  const container = document.getElementById('reto-table-container');
  try {
    const res = await fetch(`${API_BASE}/top5-rentabilidad`);
    const data = await res.json();
    allTop5Rows = data.rows || [];

    // Populate Region filter dropdown
    const select = document.getElementById('filter-region-select');
    const regions = [...new Set(allTop5Rows.map(r => r.region))];
    select.innerHTML = '<option value="ALL">Todas las Regiones</option>';
    regions.forEach(reg => {
      select.innerHTML += `<option value="${reg}">${reg}</option>`;
    });

    // Calculate totals
    const sumQ1 = allTop5Rows.reduce((acc, r) => acc + parseFloat(r.rentabilidad_q1_2026 || 0), 0);
    const sumQ2 = allTop5Rows.reduce((acc, r) => acc + parseFloat(r.rentabilidad_q2_2026 || 0), 0);
    const varPct = sumQ1 > 0 ? (((sumQ2 - sumQ1) / sumQ1) * 100).toFixed(2) : '100.00';

    document.getElementById('kpi-total-regiones').innerText = regions.length;
    document.getElementById('kpi-total-q1').innerText = `$${sumQ1.toLocaleString('es-MX', { minimumFractionDigits: 2 })}`;
    document.getElementById('kpi-total-q2').innerText = `$${sumQ2.toLocaleString('es-MX', { minimumFractionDigits: 2 })}`;
    document.getElementById('kpi-var-global').innerText = `${varPct > 0 ? '+' : ''}${varPct}%`;
    document.getElementById('kpi-var-global').className = `kpi-value ${varPct >= 0 ? 'text-success' : 'text-danger'}`;

    renderTop5Table('ALL');
  } catch (err) {
    container.innerHTML = `<div class="empty-state text-danger">Error al calcular el reto: ${err.message}</div>`;
  }
}

function renderTop5Table(filterRegion = 'ALL') {
  const container = document.getElementById('reto-table-container');
  const filtered = filterRegion === 'ALL' 
    ? allTop5Rows 
    : allTop5Rows.filter(r => r.region === filterRegion);

  if (filtered.length === 0) {
    container.innerHTML = '<div class="empty-state">No hay registros para la región seleccionada.</div>';
    return;
  }

  let html = `
    <table class="data-table">
      <thead>
        <tr>
          <th>Región</th>
          <th>Top</th>
          <th>Nombre del Producto</th>
          <th>Categoría</th>
          <th>Rentabilidad Q2 2026</th>
          <th>Rentabilidad Q1 2026</th>
          <th>Variación Absoluta ($)</th>
          <th>Variación (%)</th>
          <th>Estatus Periodo Anterior</th>
        </tr>
      </thead>
      <tbody>
  `;

  filtered.forEach(r => {
    const varAbs = parseFloat(r.variacion_absoluta);
    const varPct = parseFloat(r.variacion_porcentual);
    const badgeClass = varPct >= 0 ? 'text-success' : 'text-danger';
    const isNew = r.indicador_periodo_anterior.includes('Nuevo');

    html += `
      <tr>
        <td><strong>${r.region}</strong></td>
        <td><span class="badge badge-rank">#${r.ranking_region}</span></td>
        <td class="font-bold">${r.nombre_producto}</td>
        <td>${r.categoria}</td>
        <td class="text-success font-bold">$${parseFloat(r.rentabilidad_q2_2026).toLocaleString('es-MX', { minimumFractionDigits: 2 })}</td>
        <td class="text-muted">$${parseFloat(r.rentabilidad_q1_2026).toLocaleString('es-MX', { minimumFractionDigits: 2 })}</td>
        <td class="${badgeClass}">$${varAbs.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</td>
        <td class="${badgeClass} font-bold">${varPct > 0 ? '+' : ''}${varPct}%</td>
        <td><span class="badge ${isNew ? 'badge-pedido' : 'badge-stock'}">${r.indicador_periodo_anterior}</span></td>
      </tr>
    `;
  });

  html += '</tbody></table>';
  container.innerHTML = html;
}

// ==================== SQL PLAYGROUND ====================
function initSqlPlayground() {
  const select = document.getElementById('sql-preset-select');
  const editor = document.getElementById('sql-editor-input');
  const btnRun = document.getElementById('btn-run-sql');
  const btnExplain = document.getElementById('btn-run-explain');

  // Load initial preset
  editor.value = SQL_PRESETS.reto;

  select.addEventListener('change', (e) => {
    if (SQL_PRESETS[e.target.value]) {
      editor.value = SQL_PRESETS[e.target.value];
    }
  });

  btnRun.addEventListener('click', () => executeQuery(false));
  btnExplain.addEventListener('click', () => executeQuery(true));
}

async function executeQuery(isExplain = false) {
  const sql = document.getElementById('sql-editor-input').value;
  const container = document.getElementById('query-results-container');
  const timeInd = document.getElementById('sql-time-indicator');

  if (!sql.trim()) return;

  container.innerHTML = '<div class="loading-state">Ejecutando en PostgreSQL 16...</div>';
  timeInd.innerText = 'Tiempo: calculando...';

  try {
    const res = await fetch(`${API_BASE}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sql, explain: isExplain })
    });
    const data = await res.json();

    if (!res.ok) {
      container.innerHTML = `<div class="empty-state text-danger">⚠️ Error en la consulta: ${data.detail || data.message}</div>`;
      timeInd.innerText = 'Error';
      return;
    }

    timeInd.innerText = `Tiempo: ${data.execution_time_ms} ms`;

    if (data.explain) {
      container.innerHTML = `<div class="explain-output">${data.plan}</div>`;
    } else {
      if (!data.rows || data.rows.length === 0) {
        container.innerHTML = `<div class="empty-state">Consulta exitosa. Se devolvieron 0 registros (${data.execution_time_ms} ms).</div>`;
        return;
      }

      let html = `<div class="mb-3 text-muted" style="font-size:0.8rem;">Filas devueltas: <strong>${data.total_rows}</strong></div>`;
      html += '<table class="data-table"><thead><tr>';
      data.columns.forEach(c => {
        html += `<th>${c}</th>`;
      });
      html += '</tr></thead><tbody>';

      data.rows.forEach(r => {
        html += '<tr>';
        data.columns.forEach(c => {
          let val = r[c];
          if (val === null || val === undefined) {
            html += '<td class="text-dim"><em>NULL</em></td>';
          } else if (typeof val === 'number') {
            html += `<td>${val.toLocaleString('es-MX')}</td>`;
          } else {
            html += `<td>${val}</td>`;
          }
        });
        html += '</tr>';
      });

      html += '</tbody></table>';
      container.innerHTML = html;
    }
  } catch (err) {
    container.innerHTML = `<div class="empty-state text-danger">Error de conexión: ${err.message}</div>`;
  }
}

// ==================== CSV EXPORT ====================
function exportTableToCsv() {
  const table = document.querySelector('#table-container table');
  if (!table) return;

  let csv = [];
  const rows = table.querySelectorAll('tr');
  rows.forEach(row => {
    let cols = row.querySelectorAll('th, td');
    let rowData = [];
    cols.forEach(c => {
      let text = c.innerText.replace(/"/g, '""').trim();
      rowData.push(`"${text}"`);
    });
    csv.push(rowData.join(','));
  });

  const blob = new Blob([csv.join('\n')], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${currentTable}_export_${new Date().toISOString().slice(0, 10)}.csv`;
  a.click();
}
