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

### Servicios
Creá servicios con categoría, descripción, valor/hora y horas mínimas. Organizados por categorías para fácil acceso.

### Repuestos
Gestioná repuestos con nombre, categoría, descripción, precio y link de compra. Podés agregar múltiples repuestos a un presupuesto.

### Cálculo de distancia
Usa Nominatim + OSRM (sin API key, gratis) para calcular la distancia real por calles entre tu residencia y el cliente.

### Recargo por km
Configurable en la sección Config, se suma automáticamente al total según la distancia calculada.

### Presupuesto
- Armá presupuestos con múltiples servicios y repuestos
- **Guardado persistente**: Los presupuestos se guardan en la base de datos (no se pierden al cerrar el navegador)
- Cargá presupuestos guardados para editarlos o reutilizarlos
- Eliminá presupuestos que ya no necesites
- Generá PDF para el cliente con un clic
- Limpiá la planilla cuando termines

### Backup e Importación Inteligente (v2)
- **Exportar**: Descargá un archivo JSON con todos tus servicios, repuestos, presupuestos y configuración
- **Importar**: Cargá datos desde un archivo JSON
  - ✅ **No duplica**: Si un servicio/repuesto/presupuesto ya existe, lo ignora
  - ✅ **Agrega lo nuevo**: Solo importa lo que no tenés en tu máquina
  - ✅ **No pisa configuración**: Solo agrega configs que no existen
  - ✅ **Te avisa**: Muestra cuántos se agregaron y cuántos ya existían
- Ideal para sincronizar entre múltiples máquinas (notebook + PC escritorio)
- Compatible con versiones anteriores (v1 del export)

## Estructura

```
hora-service/
├── application.py       # Flask app
├── setup.bat           # Primera configuración
├── iniciar.bat        # Iniciar app
├── requirements.txt
├── templates/
│   └── index.html      # UI (incluye JS para export/import)
├── static/
│   └── favicon.png    # Logo
└── instance/
    └── horaservice.db # SQLite (auto)
```

## Primeros pasos

1. **Config** → cargar tu domicilio y recargo por km
2. **Servicios** → agregar tipos de servicio
3. **Repuestos** → agregar repuestos disponibles (opcional)
4. **Calculadora** → seleccionar servicio, ingresar dirección → calcular
5. **Presupuesto** → armar planilla con servicios y repuestos, generar PDF

## Sincronización entre máquinas

Para tener tus datos en múltiples dispositivos:

1. En la máquina origen: **Exportar** → se descarga `horaservice-backup-YYYY-MM-DD.json`
2. Copiá el archivo a la otra máquina
3. En la máquina destino: **Importar** → **Seleccionar archivo** → elegí el JSON
4. Se agregan solo los servicios/repuestos que te faltaban (sin duplicar)

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
- El import valida la estructura del JSON antes de procesar