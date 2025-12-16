# Sistema de Selección de Transportistas

## Descripción
Aplicación para seleccionar el mejor transportista y servicio en función de:
- Productos del pedido (volumen, peso)
- Provincia de entrega
- Tipo de entrega (a pie de calle, subida a domicilio, subida e instalación)

## Características
- Tarifas flexibles por volumen, peso o palets
- Comparación automática de precios
- Base de datos SQLite
- Datos de ejemplo incluidos

## Estructura del Proyecto
```
Python_Transportistas/
├── models/              # Modelos de datos
│   └── models.py
├── database/            # Gestión de base de datos
│   └── db_manager.py
├── services/            # Lógica de negocio
│   └── selector.py
├── data/                # Datos de ejemplo
│   └── sample_data.py
├── main.py              # Script principal
├── init_db.py           # Inicialización de BD
└── requirements.txt     # Dependencias
```

## Instalación
```bash
# Ejecutar el instalador
.\install.bat

# O manualmente:
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
```

## Uso
```bash
python main.py
```

## Modelo de Datos

### Transportistas
- ID, nombre, activo

### Servicios de Transportista
- Tipo de entrega (pie_calle, subida_domicilio, subida_instalacion)
- Método de cálculo (volumen, peso, palets)

### Tarifas
- Por provincia y rango de medida (peso/volumen/palets)
- Precio base + precio por unidad

### Productos
- Volumen, peso, descripción
