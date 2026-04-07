from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horaservice.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ─── MODELOS ───────────────────────────────────────────────────────────────────

class Configuracion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(64), unique=True, nullable=False)
    valor = db.Column(db.String(256), nullable=False)

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    categoria = db.Column(db.String(64), nullable=False)
    descripcion = db.Column(db.Text)
    valor_hora = db.Column(db.Float, nullable=False)
    horas_minimas = db.Column(db.Float, nullable=False, default=1.0)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'descripcion': self.descripcion,
            'valor_hora': self.valor_hora,
            'horas_minimas': self.horas_minimas
        }

# ─── GEOCODING (Nominatim / OpenStreetMap) ────────────────────────────────────

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OSRM_URL = "https://router.project-osrm.org/route/v1/driving"

def geocodificar(direccion):
    """Convierte una dirección en coordenadas lat/lon."""
    params = {
        'q': direccion,
        'format': 'json',
        'limit': 1,
        'countrycodes': 'ar'
    }
    headers = {'User-Agent': 'HoraService/1.0 (app local)'}
    r = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=8)
    r.raise_for_status()
    data = r.json()
    if not data:
        return None
    return float(data[0]['lat']), float(data[0]['lon'])

def calcular_distancia_km(origen_coords, destino_coords):
    """Distancia en km usando OSRM (ruta real, no línea recta)."""
    lat1, lon1 = origen_coords
    lat2, lon2 = destino_coords
    url = f"{OSRM_URL}/{lon1},{lat1};{lon2},{lat2}"
    params = {'overview': 'false'}
    r = requests.get(url, params=params, timeout=8)
    r.raise_for_status()
    data = r.json()
    if data.get('code') != 'Ok':
        return None
    distancia_m = data['routes'][0]['distance']
    return round(distancia_m / 1000, 2)

# ─── RUTAS API ─────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

# --- Configuración (residencia base) ---

@app.route('/api/config', methods=['GET'])
def get_config():
    items = Configuracion.query.all()
    return jsonify({c.clave: c.valor for c in items})

@app.route('/api/config', methods=['POST'])
def set_config():
    data = request.json
    for clave, valor in data.items():
        c = Configuracion.query.filter_by(clave=clave).first()
        if c:
            c.valor = str(valor)
        else:
            db.session.add(Configuracion(clave=clave, valor=str(valor)))
    db.session.commit()
    return jsonify({'ok': True})

@app.route('/api/config-publica', methods=['GET'])
def get_config_publica():
    items = Configuracion.query.all()
    config = {c.clave: c.valor for c in items}
    config['residencia'] = ''
    return jsonify(config)

# --- Servicios ---

@app.route('/api/servicios', methods=['GET'])
def get_servicios():
    servicios = Servicio.query.order_by(Servicio.categoria, Servicio.nombre).all()
    return jsonify([s.to_dict() for s in servicios])

@app.route('/api/servicios', methods=['POST'])
def crear_servicio():
    d = request.json
    s = Servicio(
        nombre=d['nombre'],
        categoria=d['categoria'],
        descripcion=d.get('descripcion', ''),
        valor_hora=float(d['valor_hora']),
        horas_minimas=float(d.get('horas_minimas', 1.0))
    )
    db.session.add(s)
    db.session.commit()
    return jsonify(s.to_dict()), 201

@app.route('/api/servicios/<int:sid>', methods=['PUT'])
def actualizar_servicio(sid):
    s = Servicio.query.get_or_404(sid)
    d = request.json
    s.nombre = d.get('nombre', s.nombre)
    s.categoria = d.get('categoria', s.categoria)
    s.descripcion = d.get('descripcion', s.descripcion)
    s.valor_hora = float(d.get('valor_hora', s.valor_hora))
    s.horas_minimas = float(d.get('horas_minimas', s.horas_minimas))
    db.session.commit()
    return jsonify(s.to_dict())

@app.route('/api/servicios/<int:sid>', methods=['DELETE'])
def eliminar_servicio(sid):
    s = Servicio.query.get_or_404(sid)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'ok': True})

# --- Calculadora ---

@app.route('/api/calcular', methods=['POST'])
def calcular():
    d = request.json
    servicio_id = d.get('servicio_id')
    destino = d.get('destino', '').strip()
    horas_extra = float(d.get('horas_extra', 0))

    if not servicio_id or not destino:
        return jsonify({'error': 'Faltan datos'}), 400

    servicio = Servicio.query.get_or_404(servicio_id)

    # Obtener dirección base
    config = {c.clave: c.valor for c in Configuracion.query.all()}
    residencia = config.get('residencia', '')
    recargo_por_km = float(config.get('recargo_por_km', 0))

    resultado = {
        'servicio': servicio.to_dict(),
        'horas_cobradas': servicio.horas_minimas + horas_extra,
        'costo_base': (servicio.horas_minimas + horas_extra) * servicio.valor_hora,
        'distancia_km': None,
        'recargo_distancia': 0,
        'costo_total': 0,
        'advertencia': None
    }

    # Calcular distancia si hay residencia configurada
    if residencia:
        try:
            origen_coords = geocodificar(residencia)
            destino_coords = geocodificar(f"{destino}, Buenos Aires, Argentina")

            if origen_coords and destino_coords:
                km = calcular_distancia_km(origen_coords, destino_coords)
                resultado['distancia_km'] = km
                resultado['recargo_distancia'] = round(km * recargo_por_km, 2)
                if km > 30:
                    resultado['advertencia'] = f"Destino a {km} km — considerá si conviene."
            else:
                resultado['advertencia'] = 'No se pudo geocodificar alguna dirección.'
        except Exception as e:
            resultado['advertencia'] = f'Error al calcular distancia: {str(e)}'

    resultado['costo_total'] = round(resultado['costo_base'] + resultado['recargo_distancia'], 2)
    return jsonify(resultado)

# ─── INIT ──────────────────────────────────────────────────────────────────────

with app.app_context():
    db.create_all()
    # Seed config por defecto si está vacía
    if not Configuracion.query.first():
        defaults = [
            Configuracion(clave='residencia', valor=''),
            Configuracion(clave='recargo_por_km', valor='0'),
        ]
        db.session.add_all(defaults)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
