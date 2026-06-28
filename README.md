# Analytics Service - Modulo 6 Finanzas

Servicio independiente para la pantalla "Ventas de la Semana / Reporte" del sistema distribuido Sakila.

## Responsabilidad

- Exponer el reporte semanal de ventas del modulo de finanzas.
- Ejecutar consultas analiticas separadas del POS para no afectar alquileres y devoluciones.
- Entregar KPIs: ventas totales, operaciones, ticket promedio y ventas agrupadas por dia.
- Publicar endpoints de salud para monitoreo y alta disponibilidad.
- Escribir logs trazables con `request_id`, ruta, estado y duracion.

## Endpoints

- `GET /`: informacion del servicio.
- `GET /health/live`: verifica que el proceso esta vivo.
- `GET /health/ready`: verifica conexion con Supabase.
- `GET /reports/sales-report?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`: reporte semanal.

El reporte acepta un rango maximo de 7 dias.

## Variables de entorno

Copia `.env.example` como `.env` y completa:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `CORS_ORIGINS`
- `CORS_ALLOW_CREDENTIALS`
- `LOG_LEVEL`

No subas `.env` al repositorio.

## Ejecucion local

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8006
```

## Produccion en VPS

```bash
gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  -w 2 \
  -b 0.0.0.0:8006 \
  --access-logfile - \
  --error-logfile -
```

## Docker

```bash
docker compose up -d --build
docker compose logs -f analytics-service
```

## Alta disponibilidad

Para produccion, se recomienda:

- Ejecutar al menos 2 workers con Gunicorn.
- Usar `restart: unless-stopped` o un servicio `systemd` con reinicio automatico.
- Exponer `/health/live` y `/health/ready` en el balanceador o monitor.
- Mantener Supabase con pooling de conexiones.
- Enviar logs de stdout a Cloud Logging, journald o al sistema de monitoreo del VPS.
