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
- **Exportación de tarifas a Excel**
- **Importación de tarifas desde Excel (añadir/modificar)**

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

### Menú Principal
1. **Ver mejor transportista para cada pedido**: Muestra la opción más económica para todos los pedidos
2. **Comparar transportistas para un pedido específico**: Análisis detallado de un pedido
3. **Comparar transportistas para TODOS los pedidos**: Comparación completa
4. **Listar todos los pedidos**: Vista tabular de todos los pedidos con sus totales
5. **Listar tarifas de todos los transportistas**: Ver todas las tarifas disponibles
6. **Exportar tarifas a Excel**: Exporta todas las tarifas a un archivo .xlsx
7. **Importar tarifas desde Excel**: Importa tarifas desde Excel (añade/modifica)
8. **Salir**

### Gestión de Tarifas con Excel

#### Exportar Tarifas
Desde el menú principal, selecciona la opción **6**:
```
6. Exportar tarifas a Excel
```

El sistema creará un archivo Excel con el formato:
```
tarifas_export_YYYYMMDD_HHMMSS.xlsx
```

Columnas del archivo:
- **ID**: Identificador de la tarifa (para actualización)
- **Transportista**: Nombre del transportista
- **Servicio**: Descripción del servicio
- **Tipo Entrega**: PIE_CALLE, SUBIDA_DOMICILIO o SUBIDA_INSTALACION
- **Método Cálculo**: PESO, VOLUMEN o PALETS
- **Provincia**: Provincia o NACIONAL
- **Rango Min**: Valor mínimo del rango
- **Rango Max**: Valor máximo del rango (vacío = infinito)
- **Precio Fijo**: Precio total para ese rango

#### Importar Tarifas
1. Exporta las tarifas actuales (opción 6)
2. Abre el archivo Excel generado
3. Modifica los precios o añade nuevas filas
4. Guarda el archivo
5. Desde el menú principal, selecciona la opción **7**
6. Ingresa el nombre del archivo Excel
7. Revisa el resumen de cambios
8. Confirma la importación

**Reglas de importación:**
- Si la tarifa tiene ID y existe → se **actualiza** el precio
- Si la tarifa no tiene ID pero coincide (servicio+provincia+rangos) → se **actualiza**
- Si la tarifa no existe → se **crea nueva**
- Los transportistas y servicios deben existir previamente en la base de datos
- Las provincias deben coincidir exactamente (case-sensitive)

**Ejemplo de modificación:**
```
Antes:  SEUR | Pie Calle | Madrid | 0-10kg  | 8.50€
Después: SEUR | Pie Calle | Madrid | 0-10kg  | 9.00€  ← Precio actualizado
```

**Ejemplo de nueva tarifa:**
```
Nueva fila: SEUR | Pie Calle | Málaga | 0-15kg | 12.00€  ← Tarifa nueva para Málaga
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
