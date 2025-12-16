# Proceso de Selección de Transportista y Servicio

## Descripción General

El sistema de selección de transportistas determina automáticamente la opción más económica para entregar un pedido, evaluando todos los transportistas disponibles según sus tarifas, servicios y características específicas del envío.

## Flujo del Proceso

```
┌─────────────────────────────────────────────────────────┐
│          1. ANÁLISIS DEL PEDIDO                         │
│   - Productos y cantidades                              │
│   - Provincia de entrega                                │
│   - Tipo de entrega requerido                           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│          2. CÁLCULO DE TOTALES                          │
│   - Peso total (kg)                                     │
│   - Volumen total (m³)                                  │
│   - Palets estimados (volumen / 2)                      │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│          3. FILTRADO DE SERVICIOS                       │
│   - Solo servicios activos                              │
│   - Transportistas activos                              │
│   - Tipo de entrega coincidente                         │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│          4. COTIZACIÓN POR SERVICIO                     │
│   Para cada servicio compatible:                        │
│   a) Determinar cantidad según método                   │
│   b) Buscar tarifa aplicable                            │
│   c) Calcular precio                                    │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│          5. ORDENAMIENTO Y SELECCIÓN                    │
│   - Ordenar por precio (menor a mayor)                  │
│   - Seleccionar la opción más económica                 │
└─────────────────────────────────────────────────────────┘
```

## Detalle de Cada Paso

### 1. Análisis del Pedido

El sistema recibe como entrada:
- **Número de pedido**: Identificador único
- **Productos**: Lista de productos con sus cantidades
- **Provincia de entrega**: Destino del envío
- **Tipo de entrega**: 
  - `PIE_CALLE`: Entrega en planta baja
  - `SUBIDA_DOMICILIO`: Entrega con subida al domicilio
  - `SUBIDA_INSTALACION`: Entrega con instalación incluida

**Ejemplo:**
```
Pedido: PED-2024-001
Provincia: Madrid
Tipo: Pie de calle
Productos:
  - Mesa comedor (40kg, 0.8m³) x1
  - Silla (4.5kg, 0.125m³) x4
```

### 2. Cálculo de Totales

El sistema calcula tres métricas fundamentales:

#### Peso Total
```
Peso Total = Σ (Peso_Unitario × Cantidad)
```

#### Volumen Total
```
Volumen Total = Σ (Volumen_Unitario × Cantidad)
```

#### Palets Estimados
```
Palets = Volumen Total / 2
```
*Basado en el estándar de que un europalet tiene aproximadamente 2m³*

**Ejemplo:**
```
Peso Total = (40kg × 1) + (4.5kg × 4) = 58kg
Volumen Total = (0.8m³ × 1) + (0.125m³ × 4) = 1.3m³
Palets = 1.3m³ / 2 = 0.65 palets
```

### 3. Filtrado de Servicios Compatibles

El sistema busca en la base de datos servicios que cumplan **TODOS** estos criterios:

1. **Servicio activo**: `servicio.activo = TRUE`
2. **Transportista activo**: `transportista.activo = TRUE`
3. **Tipo de entrega coincidente**: `servicio.tipo_entrega = pedido.tipo_entrega`

**Ejemplo de servicios encontrados:**
```
- SEUR Pie Calle (PESO)
- MRW Pie Calle (VOLUMEN)
- GLS Pie Calle (PALETS)
- DHL Pie Calle (PESO)
- Correos Express Pie Calle (VOLUMEN)
- Nacex Pie Calle (PALETS)
```

### 4. Cotización por Servicio

Para cada servicio compatible, se realiza el siguiente proceso:

#### 4.1. Determinar Cantidad según Método

Cada servicio tiene un **método de cálculo** que determina qué métrica usar:

| Método | Cantidad Usada | Unidad |
|--------|---------------|--------|
| `PESO` | Peso Total | kg |
| `VOLUMEN` | Volumen Total | m³ |
| `PALETS` | Palets Estimados | palets |

**Ejemplo:**
- SEUR (PESO) → usa 58kg
- MRW (VOLUMEN) → usa 1.3m³
- GLS (PALETS) → usa 0.65 palets

#### 4.2. Buscar Tarifa Aplicable

El sistema busca la tarifa que cumpla:

1. **Servicio coincidente**: `tarifa.servicio_id = servicio.id`
2. **Provincia coincidente**: `tarifa.provincia IN (provincia_pedido, 'NACIONAL')`
3. **Rango aplicable**: `rango_min ≤ cantidad < rango_max` (o `rango_max = NULL` para infinito)

**Prioridad de provincias:**
1. Tarifa específica de la provincia
2. Tarifa nacional (`NACIONAL`)

**Ejemplo de búsqueda para MRW Pie Calle en Madrid (1.3m³):**
```sql
Servicio: MRW Pie Calle
Provincia: Madrid o NACIONAL
Cantidad: 1.3 m³

Tarifas encontradas:
├─ Madrid: 0.0 - 0.5 → NO (fuera de rango)
├─ Madrid: 0.5 - 1.5 → SÍ ✓ (1.3 está en el rango)
└─ NACIONAL: 0.0 - 1.5 → SÍ (pero se prefiere Madrid)

Seleccionada: Madrid 0.5 - 1.5 → 18.00€
```

#### 4.3. Calcular Precio

Con el nuevo sistema de **precio fijo por rango**, el cálculo es directo:

```
Precio Total = tarifa.precio_fijo
```

**Ya NO se usa la fórmula antigua:**
~~`Precio = precio_base + (cantidad × precio_unidad)`~~

**Ventajas del precio fijo:**
- ✅ Precios más predecibles
- ✅ Cálculo más simple
- ✅ Rangos más granulares
- ✅ Mejor para el cliente

**Ejemplo de cotizaciones:**
```
SEUR Pie Calle (PESO)
  58kg en rango [40-80kg] → 35.00€

MRW Pie Calle (VOLUMEN)
  1.3m³ en rango [0.5-1.5m³] → 18.00€

DHL Pie Calle (PESO)
  58kg en rango [30-80kg] → 22.00€
```

### 5. Ordenamiento y Selección

Una vez obtenidas todas las cotizaciones válidas:

1. **Ordenar** por precio total (menor a mayor)
2. **Seleccionar** la primera opción (más económica)
3. **Calcular ahorro** (diferencia entre mejor y peor opción)

**Ejemplo de ranking:**
```
🥇 1. MRW Pie Calle           18.00€  ← MEJOR OPCIÓN
🥈 2. DHL Pie Calle           22.00€
🥉 3. Correos Express         22.00€
   4. SEUR Pie Calle          35.00€
   5. GLS Pie Calle           42.00€
   6. Nacex Pie Calle         45.00€  ← OPCIÓN MÁS CARA

Ahorro: 27.00€ (60% más económico)
```

## Casos Especiales

### Sin Tarifas Disponibles

Si no existe ninguna tarifa aplicable para un servicio:
- El servicio **NO genera cotización**
- Se excluye del ranking
- Se continúa con otros servicios

### Múltiples Rangos

Un servicio puede tener varios rangos de precios:

```
DHL Pie Calle (Madrid - PESO):
├─ 0 - 15kg    → 6.50€
├─ 15 - 40kg   → 10.50€
├─ 40 - 80kg   → 18.00€   ← 58kg cae aquí
├─ 80 - 150kg  → 30.00€
└─ 150kg - ∞   → 48.00€
```

### Provincia Específica vs Nacional

Si existe tarifa para la provincia específica, **siempre se prefiere** sobre la nacional:

```
Pedido a Barcelona (100kg)

DHL Pie Calle tiene:
├─ Barcelona: 60-120kg → 25.00€  ✓ SE USA ESTA
└─ NACIONAL: 80-∞kg → 45.00€     ✗ Se ignora

Precio final: 25.00€
```

### Empates de Precio

Si múltiples servicios tienen el mismo precio:
- Se mantienen **todos** en el ranking
- El orden entre ellos es indeterminado (depende del orden de la base de datos)
- Se considera cualquiera de ellos como válido

```
Precio: 22.00€
├─ DHL Pie Calle
└─ Correos Express Pie Calle
```

## Estructura de Datos

### Entrada (Pedido)
```python
{
    "id": 1,
    "numero_pedido": "PED-2024-001",
    "provincia_entrega": "Madrid",
    "tipo_entrega": "PIE_CALLE",
    "productos": [
        {
            "producto": {
                "codigo": "MES001",
                "nombre": "Mesa comedor",
                "peso_kg": 40.0,
                "volumen_m3": 0.8
            },
            "cantidad": 1
        },
        {
            "producto": {
                "codigo": "SIL001",
                "nombre": "Silla",
                "peso_kg": 4.5,
                "volumen_m3": 0.125
            },
            "cantidad": 4
        }
    ]
}
```

### Salida (Cotización)
```python
{
    "transportista_id": 2,
    "transportista_nombre": "MRW",
    "servicio_id": 4,
    "tipo_entrega": "PIE_CALLE",
    "metodo_calculo": "VOLUMEN",
    "precio_total": 18.00,
    "cantidad_calculada": 1.30,  # m³
    "tarifa_id": 45,
    "provincia": "Madrid",
    "detalles": "1.30 m³ en rango [0.50 - 1.50] = 18.00€"
}
```

## Ventajas del Sistema

1. **Automático**: No requiere intervención manual
2. **Optimizado**: Siempre selecciona la opción más económica
3. **Transparente**: Muestra desglose completo de precios
4. **Flexible**: Soporta múltiples métodos de cálculo
5. **Escalable**: Fácil añadir nuevos transportistas o tarifas
6. **Auditable**: Registro completo de cómo se calculó cada precio

## Ejemplos Prácticos

### Ejemplo 1: Pedido Ligero - Pie de Calle

```
Pedido: PED-2024-009
Provincia: Sevilla
Tipo: Pie de calle
Totales: 73.5kg, 1.19m³, 0.60 palets

Resultado:
🥇 Correos Express (VOLUMEN) - 18.00€
   1.19 m³ en rango [0-2] = 18.00€

🥈 MRW (VOLUMEN) - 22.00€
   1.19 m³ en rango [0-1.5] = 22.00€

Ahorro: 4.00€ (18%)
```

### Ejemplo 2: Pedido Pesado - Subida con Instalación

```
Pedido: PED-2024-006
Provincia: Madrid
Tipo: Subida con instalación
Totales: 292kg, 8.62m³, 4.31 palets

Resultado:
🥇 DHL (PESO) - 105.00€
   292kg en rango [60-∞] = 105.00€

🥈 MRW (VOLUMEN) - 130.00€
   8.62 m³ en rango [2-∞] = 130.00€

Ahorro: 25.00€ (19%)
```

### Ejemplo 3: Pedido con Muchos Productos

```
Pedido: PED-2024-007
Provincia: Barcelona
Tipo: Pie de calle
Productos: 5 Escritorios + 5 Sillas + 3 Estanterías
Totales: 204kg, 5.3m³, 2.65 palets

Resultado:
🥇 DHL (PESO) - 45.00€
   204kg en rango [80-∞] = 45.00€

🥈 SEUR (PESO) - 85.00€
🥈 MRW (VOLUMEN) - 85.00€
🥈 GLS (PALETS) - 85.00€
🥈 Correos Express (VOLUMEN) - 85.00€

Ahorro: 40.00€ (47%)
```

## Notas Técnicas

- **Precisión**: Todos los cálculos usan `Decimal` para evitar errores de redondeo
- **Performance**: Consultas optimizadas con índices en provincia y rangos
- **Transacciones**: Lecturas en sesiones de base de datos aisladas
- **Cache**: No se implementa cache para garantizar precios actualizados
- **Logging**: Cada cotización registra todos los detalles para auditoría

---

**Última actualización**: Diciembre 2025
**Versión del sistema**: 2.0 (Precio Fijo por Rango)
