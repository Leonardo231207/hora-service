# HoraService 🛠️

Calculadora de presupuestos para servicios técnicos freelance.  
Calcula el costo total según tipo de servicio, horas trabajadas y distancia al cliente (usando OpenStreetMap, sin costo).

## ¿Qué hace?

- **Servicios configurables**: creás tus servicios con categoría, descripción, valor/hora y horas mínimas
- **Cálculo de distancia real**: usa Nominatim (geocodificación) + OSRM (ruteo real por calles) — todo gratis, sin API key
- **Recargo por km**: configurás un valor fijo por kilómetro que se suma automáticamente
- **Advertencia por distancia**: si el destino está a más de 30 km, te avisa para que decidas si conviene
- **Planilla de presupuesto**: armá presupuestos con múltiples servicios, calculá distancias y costos en lote
- **Impresión/PDF**: generá un presupuesto limpio para enviar al cliente (con o sin precios)

## Estructura

```
hora-service/
├── application.py      # Flask app + lógica de negocio
├── requirements.txt
├── ejecutar.bat       # Script para iniciar todo automáticamente (Windows)
├── templates/
│   └── index.html     # UI completa (una sola página)
├── .gitignore         # Excluye DB, venv, archivos sensibles
└── instance/
    └── horaservice.db # SQLite (se crea automático)
```

## Setup

### Windows (con ejecutar.bat)

```cmd
cd hora-service
ejecutar.bat
```

El script automáticamente:
1. Crea el entorno virtual si no existe
2. Instala las dependencias
3. Crea la base de datos
4. Levanta el servidor en http://127.0.0.1:5000

### Manual

```bash
# Clonar / copiar el proyecto
cd hora-service

# Crear entorno virtual
python -m venv venv

# Activar
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Correr
python application.py
```

Abrir en `http://localhost:5000`

## Primeros pasos

1. Ir a **Configuración** → cargar tu domicilio (solo vos lo ves, no se expone) y el recargo por km
2. Ir a **Servicios** → agregar tus tipos de servicio con precio/hora y mínimo de horas
3. Ir a **Calculadora** → seleccionar servicio, ingresar la dirección del cliente → calcular
4. Ir a **Presupuesto** → armá una planilla con varios servicios, destinatarios distintos, y generá el PDF

## Seguridad

- La dirección de residencia se guarda localmente en la base de datos SQLite
- La API pública (`/api/config-publica`) no devuelve la dirección — solo se usa internamente
- El presupuesto enviado al cliente **no incluye la dirección de destino** (es solo para vos)
- El `.gitignore` excluye: `instance/`, `venv/`, `.env`, archivos de IDE

## Servicios de geolocalización usados

| Servicio | Función | Límite |
|---|---|---|
| [Nominatim](https://nominatim.openstreetmap.org) | Convierte dirección → coordenadas | 1 req/seg (uso personal) |
| [OSRM](https://router.project-osrm.org) | Calcula ruta real por calles | Sin límite estricto |

> ⚠️ Nominatim pide uso razonable. Para volumen alto se puede hostear localmente o usar Photon.

## Modelo de datos

### `Configuracion` (clave-valor)
- `residencia`: dirección de origen habitual (solo uso local, no se expone)
- `recargo_por_km`: monto adicional por km de distancia

### `Servicio`
- `nombre`, `categoria`, `descripcion`
- `valor_hora`: precio por hora de trabajo
- `horas_minimas`: mínimo a cobrar (ej: 1.5 = nunca cobrás menos de 1h30)

## Ideas para extender

- [ ] Historial de presupuestos generados
- [ ] Guardar/clonar presupuestos anteriores
- [ ] Múltiples puntos de partida (si trabajás desde distintos lugares)
- [ ] Modo oscuro/claro toggle
- [ ] Auth básica si lo querés exponer en red local
- [ ] Exportar a PDF real (no solo impresión del navegador)