import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="Casa&Estilo BI Studio", version="1.0.0")

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "casa_estilo_bi")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )

@app.get("/api/status")
def get_status():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()["version"]
                cur.execute("""
                    SELECT 
                        (SELECT COUNT(*) FROM fact_ventas) AS total_ventas,
                        (SELECT COUNT(DISTINCT orden_id) FROM fact_ventas) AS total_ordenes,
                        (SELECT COALESCE(SUM(monto_venta_neta), 0) FROM fact_ventas) AS venta_neta_total,
                        (SELECT COALESCE(SUM(ganancia_bruta), 0) FROM fact_ventas) AS ganancia_total,
                        (SELECT COUNT(*) FROM dim_cliente) AS total_clientes,
                        (SELECT COUNT(*) FROM dim_producto) AS total_productos,
                        (SELECT COUNT(*) FROM dim_showroom) AS total_showrooms
                """)
                summary = cur.fetchone()
                return {
                    "status": "connected",
                    "database": DB_NAME,
                    "engine": version,
                    "summary": summary
                }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/tables")
def get_tables():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                    ORDER BY 
                        CASE WHEN table_name = 'fact_ventas' THEN 0 ELSE 1 END,
                        table_name;
                """)
                tables = [r["table_name"] for r in cur.fetchall()]
                
                result = []
                for t in tables:
                    cur.execute(f"SELECT COUNT(*) AS count FROM {t};")
                    count = cur.fetchone()["count"]
                    cur.execute(f"""
                        SELECT column_name, data_type 
                        FROM information_schema.columns 
                        WHERE table_schema = 'public' AND table_name = '{t}';
                    """)
                    cols = cur.fetchall()
                    result.append({
                        "name": t,
                        "rows": count,
                        "columns_count": len(cols),
                        "columns": cols
                    })
                return {"tables": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/table/{table_name}")
def get_table_data(
    table_name: str,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    search: str = Query(None)
):
    valid_tables = [
        "dim_tiempo", "dim_cliente", "dim_producto", 
        "dim_showroom", "dim_asesor", "dim_canal", "fact_ventas"
    ]
    if table_name.lower() not in valid_tables:
        raise HTTPException(status_code=400, detail="Tabla no permitida.")
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Column names
                cur.execute(f"""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_schema = 'public' AND table_name = '{table_name.lower()}'
                    ORDER BY ordinal_position;
                """)
                columns = [c["column_name"] for c in cur.fetchall()]
                
                # Total count
                cur.execute(f"SELECT COUNT(*) AS total FROM {table_name.lower()};")
                total_rows = cur.fetchone()["total"]
                
                # Fetch rows
                query = f"SELECT * FROM {table_name.lower()} LIMIT %s OFFSET %s;"
                cur.execute(query, (limit, offset))
                rows = cur.fetchall()
                
                return {
                    "table": table_name,
                    "columns": columns,
                    "total_rows": total_rows,
                    "limit": limit,
                    "offset": offset,
                    "rows": rows
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/top5-rentabilidad")
def get_top5_rentabilidad():
    query = """
    WITH rentabilidad_trimestral AS (
        SELECT
            COALESCE(s.zona, 'Sin Zona') AS region,
            p.producto_sk,
            p.nombre_producto,
            p.categoria,
            -- Rentabilidad (Ganancia Bruta) por Trimestre de 2026
            SUM(CASE WHEN t.anio = 2026 AND t.trimestre = 1 THEN f.ganancia_bruta ELSE 0 END) AS rentabilidad_q1_2026,
            SUM(CASE WHEN t.anio = 2026 AND t.trimestre = 2 THEN f.ganancia_bruta ELSE 0 END) AS rentabilidad_q2_2026,
            -- Conteo de unidades en Q1 para saber si existieron datos previos
            COUNT(CASE WHEN t.anio = 2026 AND t.trimestre = 1 THEN 1 ELSE NULL END) AS transacciones_q1
        FROM Fact_Ventas f
        JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
        JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
        JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
        WHERE t.anio = 2026 AND t.trimestre IN (1, 2)
        GROUP BY s.zona, p.producto_sk, p.nombre_producto, p.categoria
    ),
    ranking_por_region AS (
        SELECT
            region,
            nombre_producto,
            categoria,
            rentabilidad_q1_2026,
            rentabilidad_q2_2026,
            (rentabilidad_q2_2026 - rentabilidad_q1_2026) AS variacion_absoluta,
            CASE
                WHEN rentabilidad_q1_2026 = 0 AND rentabilidad_q2_2026 > 0 THEN 100.00
                WHEN rentabilidad_q1_2026 = 0 AND rentabilidad_q2_2026 = 0 THEN 0.00
                ELSE ROUND(((rentabilidad_q2_2026 - rentabilidad_q1_2026) / ABS(rentabilidad_q1_2026)) * 100, 2)
            END AS variacion_porcentual,
            CASE
                WHEN transacciones_q1 = 0 THEN 'Sin datos en periodo anterior (Nuevo en Q2)'
                ELSE 'Con datos en periodo anterior'
            END AS indicador_periodo_anterior,
            DENSE_RANK() OVER (
                PARTITION BY region 
                ORDER BY rentabilidad_q2_2026 DESC
            ) AS ranking_region
        FROM rentabilidad_trimestral
    )
    SELECT
        region,
        ranking_region,
        nombre_producto,
        categoria,
        ROUND(rentabilidad_q2_2026, 2) AS rentabilidad_q2_2026,
        ROUND(rentabilidad_q1_2026, 2) AS rentabilidad_q1_2026,
        ROUND(variacion_absoluta, 2) AS variacion_absoluta,
        variacion_porcentual,
        indicador_periodo_anterior
    FROM ranking_por_region
    WHERE ranking_region <= 5
    ORDER BY region, ranking_region;
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                start_time = time.time()
                cur.execute(query)
                rows = cur.fetchall()
                elapsed_ms = round((time.time() - start_time) * 1000, 2)
                return {
                    "query_title": "Top 5 Productos con Mayor Rentabilidad por Región (Q2 vs Q1 2026)",
                    "execution_time_ms": elapsed_ms,
                    "rows": rows
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class QueryRequest(BaseModel):
    sql: str
    explain: bool = False

@app.post("/api/query")
def execute_query(req: QueryRequest):
    clean_sql = req.sql.strip().rstrip(";")
    if not clean_sql.upper().startswith("SELECT") and not clean_sql.upper().startswith("WITH") and not clean_sql.upper().startswith("EXPLAIN"):
        raise HTTPException(status_code=400, detail="Solo se permiten consultas de lectura (SELECT / WITH / EXPLAIN).")
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                target_sql = f"EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE, FORMAT TEXT) {clean_sql};" if req.explain else f"{clean_sql};"
                start = time.time()
                cur.execute(target_sql)
                elapsed_ms = round((time.time() - start) * 1000, 2)
                
                if req.explain:
                    lines = [r["QUERY PLAN"] for r in cur.fetchall()]
                    return {
                        "explain": True,
                        "execution_time_ms": elapsed_ms,
                        "plan": "\n".join(lines)
                    }
                else:
                    rows = cur.fetchall()
                    cols = list(rows[0].keys()) if rows else []
                    return {
                        "explain": False,
                        "execution_time_ms": elapsed_ms,
                        "columns": cols,
                        "total_rows": len(rows),
                        "rows": rows
                    }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Mount static directory for Frontend UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
