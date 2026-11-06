#!/usr/bin/env python3
# ==============================================================================
# PROYECTO: LABORATORIO UNIDAD 5 · DATA MART AL DASHBOARD EJECUTIVO
# SERVIDOR WEB EN TIEMPO REAL PARA VERIFICACIÓN EN EL SALÓN DE CLASES
# PUERTO POR DEFECTO: 8085
# EQUIPO: Equipo 8 (Inteligencia de Negocios · FIME UANL 2026)
# ==============================================================================

import os
import sys
import csv
import json
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import urllib.parse

PORT = int(os.environ.get("PORT", 8085))

# Rutas de datos
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "01_datos_crudos"
WEB_DIR = BASE_DIR / "dashboard_web"

# Cache de datos en memoria
DATOS_EN_MEMORIA = {}

def cargar_datos():
    print("📦 Cargando y relacionando Data Mart en memoria...")
    
    with open(RAW_DIR / "DIM_PRODUCTO.csv", encoding="utf-8-sig") as f:
        prods = {r["id_producto"]: r for r in csv.DictReader(f)}
    with open(RAW_DIR / "DIM_CLIENTE.csv", encoding="utf-8-sig") as f:
        clis = {r["id_cliente"]: r for r in csv.DictReader(f)}
    with open(RAW_DIR / "DIM_TIEMPO.csv", encoding="utf-8-sig") as f:
        times = {r["id_tiempo"]: r for r in csv.DictReader(f)}
    with open(RAW_DIR / "FACT_VENTAS.csv", encoding="utf-8-sig") as f:
        raw_facts = list(csv.DictReader(f))

    facts_denorm = []
    for r in raw_facts:
        p = prods[r["id_producto"]]
        c = clis[r["id_cliente"]]
        t = times[r["id_tiempo"]]
        monto = float(r["monto"])
        costo = float(r["costo"])
        cant = int(r["cantidad"])

        facts_denorm.append({
            "id_venta": int(r["id_venta"]),
            "id_producto": int(r["id_producto"]),
            "producto": p["producto"],
            "categoria": p["categoria"],
            "id_cliente": int(r["id_cliente"]),
            "cliente": c["cliente"],
            "region": c["region"],
            "id_tiempo": int(r["id_tiempo"]),
            "fecha": t["fecha"],
            "anio": int(t["anio"]),
            "mes": int(t["mes"]),
            "cantidad": cant,
            "monto": monto,
            "costo": costo
        })

    # Cifras de control globales
    total_ventas = sum(r["monto"] for r in facts_denorm)
    total_costo = sum(r["costo"] for r in facts_denorm)
    total_mb = total_ventas - total_costo
    total_tx = len(set(r["id_venta"] for r in facts_denorm))

    DATOS_EN_MEMORIA["summary"] = {
        "transacciones": total_tx,
        "ventas": total_ventas,
        "costo": total_costo,
        "margen_bruto": total_mb,
        "margen_pct": total_mb / total_ventas,
        "ticket_promedio": total_ventas / total_tx
    }
    DATOS_EN_MEMORIA["facts"] = facts_denorm
    print(f"✅ Data Mart cargado: {len(facts_denorm)} transacciones.")
    print(f"   Ventas: ${total_ventas:,.2f} | Margen: ${total_mb:,.2f} ({total_mb/total_ventas*100:.2f}%)")

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            html_file = WEB_DIR / "index.html"
            if html_file.exists():
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(html_file, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "index.html no encontrado")

        elif path == "/api/data":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(DATOS_EN_MEMORIA).encode("utf-8"))

        elif path == "/api/status":
            status_obj = {
                "status": "online",
                "equipo": "Equipo 8 (FIME 2026)",
                "unidad": 5,
                "modelo": "Esquema Estrella (Power Pivot / DAX)",
                "cifras_control": DATOS_EN_MEMORIA.get("summary", {})
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(status_obj).encode("utf-8"))

        else:
            self.send_error(404, "Ruta no encontrada")

    def log_message(self, format, *args):
        # Log silencioso o conciso para terminal
        sys.stderr.write(f"[{self.log_date_time_string()}] {args[0]} - {args[1]}\n")

def run_server():
    cargar_datos()
    server_address = ("0.0.0.0", PORT)
    httpd = ThreadingHTTPServer(server_address, DashboardHandler)
    print("==============================================================================")
    print(f"🚀 BI LIVE STUDIO EN VIVO EN PUERTO {PORT}")
    print("==============================================================================")
    print(f"🔗 Abre tu navegador en:  http://localhost:{PORT}")
    print("   (Presiona Ctrl+C para detener el servidor)")
    print("==============================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
