# HoraService 🛠️

Calculadora de presupuestos para servicios técnicos freelance.  
Calcula el costo total según tipo de servicio, horas trabajadas y distancia al cliente (usando OpenStreetMap, sin costo).

## ¿Qué hace?

- **Servicios configurables**: creás tus servicios con categoría, descripción, valor/hora y horas mínimas
- **Cálculo de distancia real**: usa Nominatim (geocodificación) + OSRM (ruteo real por calles) — todo gratis, sin API key
- **Recargo por km**: configurás un valor fijo por kilómetro que se suma automáticamente
- **Advertencia por distancia**: si el destino está a más de 30 km, te avisa para que decidas si conviene

## Estructura

```
hora-service/
├── app.py              # Flask app + lógica de negocio
├── requirements.txt
├── templates/
│   └── index.html      # UI completa (una sola página)
└── instance/
    └── horaservice.db  # SQLite (se crea automático)
```

## Setup

```bash
# Clonar / copiar el proyecto
cd hora-service

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Correr
python app.py
```

Abrir en `http://localhost:5000`

## Primeros pasos

1. Ir a **Configuración** → cargar tu domicilio y el recargo por km que querés aplicar
2. Ir a **Servicios** → agregar tus tipos de servicio con precio/hora y mínimo de horas
3. Ir a **Calculadora** → seleccionar servicio, ingresar la dirección del cliente → calcular

## Servicios de geolocalización usados

| Servicio | Función | Límite |
|---|---|---|
| [Nominatim](https://nominatim.openstreetmap.org) | Convierte dirección → coordenadas | 1 req/seg (uso personal) |
| [OSRM](https://router.project-osrm.org) | Calcula ruta real por calles | Sin límite estricto |

> ⚠️ Nominatim pide uso razonable. Para volumen alto se puede hostear localmente o usar Photon.

## Modelo de datos

### `Configuracion` (clave-valor)
- `residencia`: dirección de origen habitual
- `recargo_por_km`: monto adicional por km de distancia

### `Servicio`
- `nombre`, `categoria`, `descripcion`
- `valor_hora`: precio por hora de trabajo
- `horas_minimas`: mínimo a cobrar (ej: 1.5 = nunca cobrás menos de 1h30)

## Ideas para extender

- [ ] Historial de presupuestos generados
- [ ] Exportar presupuesto a PDF
- [ ] Múltiples puntos de partida (si trabajás desde distintos lugares)
- [ ] Modo oscuro/claro toggle
- [ ] Auth básica si lo querés exponer en red local
