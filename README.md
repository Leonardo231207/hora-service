# HoraService

Calculadora de presupuestos para servicios técnicos freelance.
Calcula el costo total según servicio, horas trabajadas y distancia al cliente.

## Quick Start

```cmd
# Primera vez
setup.bat

# Uso diario
iniciar.bat
```

Abrir en `http://127.0.0.1:5000`

## Funciones

- **Servicios**: creá servicios con categoría, descripción, valor/hora y horas mínimas
- **Cálculo de distancia**: usa Nominatim + OSRM (sin API key, gratis)
- **Recargo por km**: configurable, se suma automáticamente
- **Presupuesto**: armá presupuestos con múltiples servicios y generá PDF para el cliente
- **Backup**: exportá/importá tus datos en JSON

## Estructura

```
hora-service/
├── application.py       # Flask app
├── setup.bat           # Primera configuración
├── iniciar.bat        # Iniciar app
├── requirements.txt
├── templates/
│   └── index.html      # UI
├── static/
│   └── favicon.png    # Logo
└── instance/
    └── horaservice.db # SQLite (auto)
```

## Primeros pasos

1. **Config** → cargar tu domicilio y recargo por km
2. **Servicios** → agregar tipos de servicio
3. **Calculadora** → seleccionar servicio, ingresar dirección → calcular
4. **Presupuesto** → armar planilla, generar PDF

## Geolocalización

| Servicio | Función |
|---|---|
| [Nominatim](https://nominatim.openstreetmap.org) | Dirección → coordenadas |
| [OSRM](https://router.project-osrm.org) | Ruta real por calles |

> Límite: 1 req/seg en Nominatim.

## Seguridad

- La dirección de residencia solo se guarda localmente
- Los presupuestos no exponen tu ubicación
- `.gitignore` excluye: `instance/`, `venv/`, logs