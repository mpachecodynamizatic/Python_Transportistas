"""
Datos de ejemplo para el sistema de transportistas

Incluye:
- 6 Transportistas (SEUR, MRW, GLS, DHL, Correos Express, Nacex)
- Múltiples servicios con diferentes tipos de entrega
- Tarifas por provincia y rangos
- Productos de ejemplo variados
- Pedidos de prueba diversos
"""

from decimal import Decimal
from sqlalchemy.orm import Session

from models.models import (
    Transportista, ServicioTransportista, Tarifa, Producto, 
    Pedido, PedidoProducto, TipoEntrega, MetodoCalculo
)


def cargar_datos_ejemplo(session: Session):
    """
    Carga datos de ejemplo en la base de datos
    
    Args:
        session: Sesión de base de datos
    """
    print("\n📦 Cargando datos de ejemplo...")
    
    # ========== TRANSPORTISTAS ==========
    print("\n1️⃣ Creando transportistas...")
    seur = Transportista(nombre="SEUR", activo=True)
    mrw = Transportista(nombre="MRW", activo=True)
    gls = Transportista(nombre="GLS", activo=True)
    dhl = Transportista(nombre="DHL", activo=True)
    correos = Transportista(nombre="Correos Express", activo=True)
    nacex = Transportista(nombre="Nacex", activo=True)
    
    session.add_all([seur, mrw, gls, dhl, correos, nacex])
    session.flush()
    print(f"   ✓ {seur.nombre} (ID: {seur.id})")
    print(f"   ✓ {mrw.nombre} (ID: {mrw.id})")
    print(f"   ✓ {gls.nombre} (ID: {gls.id})")
    print(f"   ✓ {dhl.nombre} (ID: {dhl.id})")
    print(f"   ✓ {correos.nombre} (ID: {correos.id})")
    print(f"   ✓ {nacex.nombre} (ID: {nacex.id})")
    
    # ========== SERVICIOS DE TRANSPORTISTAS ==========
    print("\n2️⃣ Creando servicios de transportistas...")
    
    # SEUR - Servicios por PESO
    seur_pie_calle = ServicioTransportista(
        transportista=seur,
        tipo_entrega=TipoEntrega.PIE_CALLE,
        metodo_calculo=MetodoCalculo.PESO,
        activo=True
    )
    seur_subida_domicilio = ServicioTransportista(
        transportista=seur,
        tipo_entrega=TipoEntrega.SUBIDA_DOMICILIO,
        metodo_calculo=MetodoCalculo.PESO,
        activo=True
    )
    seur_instalacion = ServicioTransportista(
        transportista=seur,
        tipo_entrega=TipoEntrega.SUBIDA_INSTALACION,
        metodo_calculo=MetodoCalculo.PESO,
        activo=True
    )
    
    # MRW - Servicios por VOLUMEN
    mrw_pie_calle = ServicioTransportista(
        transportista=mrw,
        tipo_entrega=TipoEntrega.PIE_CALLE,
        metodo_calculo=MetodoCalculo.VOLUMEN,
        activo=True
    )
    mrw_subida_domicilio = ServicioTransportista(
        transportista=mrw,
        tipo_entrega=TipoEntrega.SUBIDA_DOMICILIO,
        metodo_calculo=MetodoCalculo.VOLUMEN,
        activo=True
    )
    mrw_instalacion = ServicioTransportista(
        transportista=mrw,
        tipo_entrega=TipoEntrega.SUBIDA_INSTALACION,
        metodo_calculo=MetodoCalculo.VOLUMEN,
        activo=True
    )
    
    # GLS - Servicios por PALETS
    gls_pie_calle = ServicioTransportista(
        transportista=gls,
        tipo_entrega=TipoEntrega.PIE_CALLE,
        metodo_calculo=MetodoCalculo.PALETS,
        activo=True
    )
    gls_subida_domicilio = ServicioTransportista(
        transportista=gls,
        tipo_entrega=TipoEntrega.SUBIDA_DOMICILIO,
        metodo_calculo=MetodoCalculo.PALETS,
        activo=True
    )
    
    # DHL - Servicios por PESO (competitivo)
    dhl_pie_calle = ServicioTransportista(
        transportista=dhl,
        tipo_entrega=TipoEntrega.PIE_CALLE,
        metodo_calculo=MetodoCalculo.PESO,
        activo=True
    )
    dhl_subida_domicilio = ServicioTransportista(
        transportista=dhl,
        tipo_entrega=TipoEntrega.SUBIDA_DOMICILIO,
        metodo_calculo=MetodoCalculo.PESO,
        activo=True
    )
    dhl_instalacion = ServicioTransportista(
        transportista=dhl,
        tipo_entrega=TipoEntrega.SUBIDA_INSTALACION,
        metodo_calculo=MetodoCalculo.PESO,
        activo=True
    )
    
    # Correos Express - Servicios por VOLUMEN (económico para volúmenes pequeños)
    correos_pie_calle = ServicioTransportista(
        transportista=correos,
        tipo_entrega=TipoEntrega.PIE_CALLE,
        metodo_calculo=MetodoCalculo.VOLUMEN,
        activo=True
    )
    correos_subida_domicilio = ServicioTransportista(
        transportista=correos,
        tipo_entrega=TipoEntrega.SUBIDA_DOMICILIO,
        metodo_calculo=MetodoCalculo.VOLUMEN,
        activo=True
    )
    
    # Nacex - Servicios por PALETS (competitivo para grandes volúmenes)
    nacex_pie_calle = ServicioTransportista(
        transportista=nacex,
        tipo_entrega=TipoEntrega.PIE_CALLE,
        metodo_calculo=MetodoCalculo.PALETS,
        activo=True
    )
    nacex_subida_domicilio = ServicioTransportista(
        transportista=nacex,
        tipo_entrega=TipoEntrega.SUBIDA_DOMICILIO,
        metodo_calculo=MetodoCalculo.PALETS,
        activo=True
    )
    nacex_instalacion = ServicioTransportista(
        transportista=nacex,
        tipo_entrega=TipoEntrega.SUBIDA_INSTALACION,
        metodo_calculo=MetodoCalculo.PALETS,
        activo=True
    )
    
    session.add_all([
        seur_pie_calle, seur_subida_domicilio, seur_instalacion,
        mrw_pie_calle, mrw_subida_domicilio, mrw_instalacion,
        gls_pie_calle, gls_subida_domicilio,
        dhl_pie_calle, dhl_subida_domicilio, dhl_instalacion,
        correos_pie_calle, correos_subida_domicilio,
        nacex_pie_calle, nacex_subida_domicilio, nacex_instalacion
    ])
    session.flush()
    print(f"   ✓ 16 servicios creados")
    
    # ========== TARIFAS ==========
    print("\n3️⃣ Creando tarifas...")
    
    tarifas = []
    
    # --- SEUR (por PESO) - Pie de calle ---
    # Madrid - Más rangos escalonados
    tarifas.extend([
        Tarifa(servicio=seur_pie_calle, provincia="Madrid", 
               rango_min=0, rango_max=10, precio_fijo=8.50),
        Tarifa(servicio=seur_pie_calle, provincia="Madrid", 
               rango_min=10, rango_max=25, precio_fijo=12.00),
        Tarifa(servicio=seur_pie_calle, provincia="Madrid", 
               rango_min=25, rango_max=50, precio_fijo=18.50),
        Tarifa(servicio=seur_pie_calle, provincia="Madrid", 
               rango_min=50, rango_max=100, precio_fijo=28.00),
        Tarifa(servicio=seur_pie_calle, provincia="Madrid", 
               rango_min=100, rango_max=200, precio_fijo=45.00),
        Tarifa(servicio=seur_pie_calle, provincia="Madrid", 
               rango_min=200, rango_max=None, precio_fijo=75.00),
        
        # Barcelona
        Tarifa(servicio=seur_pie_calle, provincia="Barcelona", 
               rango_min=0, rango_max=15, precio_fijo=10.00),
        Tarifa(servicio=seur_pie_calle, provincia="Barcelona", 
               rango_min=15, rango_max=35, precio_fijo=15.50),
        Tarifa(servicio=seur_pie_calle, provincia="Barcelona", 
               rango_min=35, rango_max=75, precio_fijo=24.00),
        Tarifa(servicio=seur_pie_calle, provincia="Barcelona", 
               rango_min=75, rango_max=150, precio_fijo=38.00),
        Tarifa(servicio=seur_pie_calle, provincia="Barcelona", 
               rango_min=150, rango_max=None, precio_fijo=65.00),
        
        # Valencia
        Tarifa(servicio=seur_pie_calle, provincia="Valencia", 
               rango_min=0, rango_max=20, precio_fijo=11.00),
        Tarifa(servicio=seur_pie_calle, provincia="Valencia", 
               rango_min=20, rango_max=50, precio_fijo=19.00),
        Tarifa(servicio=seur_pie_calle, provincia="Valencia", 
               rango_min=50, rango_max=120, precio_fijo=32.00),
        Tarifa(servicio=seur_pie_calle, provincia="Valencia", 
               rango_min=120, rango_max=None, precio_fijo=58.00),
        
        # Sevilla
        Tarifa(servicio=seur_pie_calle, provincia="Sevilla", 
               rango_min=0, rango_max=20, precio_fijo=12.00),
        Tarifa(servicio=seur_pie_calle, provincia="Sevilla", 
               rango_min=20, rango_max=60, precio_fijo=21.00),
        Tarifa(servicio=seur_pie_calle, provincia="Sevilla", 
               rango_min=60, rango_max=130, precio_fijo=36.00),
        Tarifa(servicio=seur_pie_calle, provincia="Sevilla", 
               rango_min=130, rango_max=None, precio_fijo=62.00),
        
        # NACIONAL (resto de provincias)
        Tarifa(servicio=seur_pie_calle, provincia="NACIONAL", 
               rango_min=0, rango_max=15, precio_fijo=13.50),
        Tarifa(servicio=seur_pie_calle, provincia="NACIONAL", 
               rango_min=15, rango_max=40, precio_fijo=22.00),
        Tarifa(servicio=seur_pie_calle, provincia="NACIONAL", 
               rango_min=40, rango_max=80, precio_fijo=35.00),
        Tarifa(servicio=seur_pie_calle, provincia="NACIONAL", 
               rango_min=80, rango_max=150, precio_fijo=52.00),
        Tarifa(servicio=seur_pie_calle, provincia="NACIONAL", 
               rango_min=150, rango_max=None, precio_fijo=85.00),
    ])
    
    # --- SEUR - Subida a domicilio ---
    tarifas.extend([
        Tarifa(servicio=seur_subida_domicilio, provincia="Madrid", 
               rango_min=0, rango_max=20, precio_fijo=18.00),
        Tarifa(servicio=seur_subida_domicilio, provincia="Madrid", 
               rango_min=20, rango_max=50, precio_fijo=28.00),
        Tarifa(servicio=seur_subida_domicilio, provincia="Madrid", 
               rango_min=50, rango_max=100, precio_fijo=42.00),
        Tarifa(servicio=seur_subida_domicilio, provincia="Madrid", 
               rango_min=100, rango_max=None, precio_fijo=68.00),
        
        Tarifa(servicio=seur_subida_domicilio, provincia="Barcelona", 
               rango_min=0, rango_max=25, precio_fijo=20.00),
        Tarifa(servicio=seur_subida_domicilio, provincia="Barcelona", 
               rango_min=25, rango_max=75, precio_fijo=35.00),
        Tarifa(servicio=seur_subida_domicilio, provincia="Barcelona", 
               rango_min=75, rango_max=None, precio_fijo=58.00),
        
        Tarifa(servicio=seur_subida_domicilio, provincia="NACIONAL", 
               rango_min=0, rango_max=30, precio_fijo=25.00),
        Tarifa(servicio=seur_subida_domicilio, provincia="NACIONAL", 
               rango_min=30, rango_max=80, precio_fijo=42.00),
        Tarifa(servicio=seur_subida_domicilio, provincia="NACIONAL", 
               rango_min=80, rango_max=None, precio_fijo=72.00),
    ])
    
    # --- SEUR - Instalación ---
    tarifas.extend([
        Tarifa(servicio=seur_instalacion, provincia="Madrid", 
               rango_min=0, rango_max=50, precio_fijo=65.00),
        Tarifa(servicio=seur_instalacion, provincia="Madrid", 
               rango_min=50, rango_max=150, precio_fijo=95.00),
        Tarifa(servicio=seur_instalacion, provincia="Madrid", 
               rango_min=150, rango_max=None, precio_fijo=145.00),
        
        Tarifa(servicio=seur_instalacion, provincia="Barcelona", 
               rango_min=0, rango_max=60, precio_fijo=72.00),
        Tarifa(servicio=seur_instalacion, provincia="Barcelona", 
               rango_min=60, rango_max=None, precio_fijo=115.00),
        
        Tarifa(servicio=seur_instalacion, provincia="NACIONAL", 
               rango_min=0, rango_max=60, precio_fijo=85.00),
        Tarifa(servicio=seur_instalacion, provincia="NACIONAL", 
               rango_min=60, rango_max=150, precio_fijo=125.00),
        Tarifa(servicio=seur_instalacion, provincia="NACIONAL", 
               rango_min=150, rango_max=None, precio_fijo=185.00),
    ])
    
    # --- MRW (por VOLUMEN m³) - Pie de calle ---
    tarifas.extend([
        Tarifa(servicio=mrw_pie_calle, provincia="Madrid", 
               rango_min=0, rango_max=0.5, precio_fijo=10.00),
        Tarifa(servicio=mrw_pie_calle, provincia="Madrid", 
               rango_min=0.5, rango_max=1.5, precio_fijo=18.00),
        Tarifa(servicio=mrw_pie_calle, provincia="Madrid", 
               rango_min=1.5, rango_max=3, precio_fijo=32.00),
        Tarifa(servicio=mrw_pie_calle, provincia="Madrid", 
               rango_min=3, rango_max=5, precio_fijo=52.00),
        Tarifa(servicio=mrw_pie_calle, provincia="Madrid", 
               rango_min=5, rango_max=None, precio_fijo=75.00),
        
        Tarifa(servicio=mrw_pie_calle, provincia="Barcelona", 
               rango_min=0, rango_max=1, precio_fijo=15.00),
        Tarifa(servicio=mrw_pie_calle, provincia="Barcelona", 
               rango_min=1, rango_max=2.5, precio_fijo=28.00),
        Tarifa(servicio=mrw_pie_calle, provincia="Barcelona", 
               rango_min=2.5, rango_max=5, precio_fijo=48.00),
        Tarifa(servicio=mrw_pie_calle, provincia="Barcelona", 
               rango_min=5, rango_max=None, precio_fijo=80.00),
        
        Tarifa(servicio=mrw_pie_calle, provincia="Valencia", 
               rango_min=0, rango_max=2, precio_fijo=20.00),
        Tarifa(servicio=mrw_pie_calle, provincia="Valencia", 
               rango_min=2, rango_max=5, precio_fijo=42.00),
        Tarifa(servicio=mrw_pie_calle, provincia="Valencia", 
               rango_min=5, rango_max=None, precio_fijo=75.00),
        
        Tarifa(servicio=mrw_pie_calle, provincia="NACIONAL", 
               rango_min=0, rango_max=1.5, precio_fijo=22.00),
        Tarifa(servicio=mrw_pie_calle, provincia="NACIONAL", 
               rango_min=1.5, rango_max=4, precio_fijo=45.00),
        Tarifa(servicio=mrw_pie_calle, provincia="NACIONAL", 
               rango_min=4, rango_max=None, precio_fijo=85.00),
    ])
    
    # --- MRW - Subida a domicilio ---
    tarifas.extend([
        Tarifa(servicio=mrw_subida_domicilio, provincia="Madrid", 
               rango_min=0, rango_max=1, precio_fijo=25.00),
        Tarifa(servicio=mrw_subida_domicilio, provincia="Madrid", 
               rango_min=1, rango_max=3, precio_fijo=45.00),
        Tarifa(servicio=mrw_subida_domicilio, provincia="Madrid", 
               rango_min=3, rango_max=None, precio_fijo=75.00),
        
        Tarifa(servicio=mrw_subida_domicilio, provincia="NACIONAL", 
               rango_min=0, rango_max=2.5, precio_fijo=38.00),
        Tarifa(servicio=mrw_subida_domicilio, provincia="NACIONAL", 
               rango_min=2.5, rango_max=None, precio_fijo=72.00),
    ])
    
    # --- MRW - Instalación ---
    tarifas.extend([
        Tarifa(servicio=mrw_instalacion, provincia="Madrid", 
               rango_min=0, rango_max=1, precio_fijo=60.00),
        Tarifa(servicio=mrw_instalacion, provincia="Madrid", 
               rango_min=1, rango_max=3, precio_fijo=95.00),
        Tarifa(servicio=mrw_instalacion, provincia="Madrid", 
               rango_min=3, rango_max=None, precio_fijo=145.00),
        
        Tarifa(servicio=mrw_instalacion, provincia="NACIONAL", 
               rango_min=0, rango_max=2, precio_fijo=75.00),
        Tarifa(servicio=mrw_instalacion, provincia="NACIONAL", 
               rango_min=2, rango_max=None, precio_fijo=130.00),
    ])
    
    # --- GLS (por PALETS) - Pie de calle ---
    tarifas.extend([
        Tarifa(servicio=gls_pie_calle, provincia="Madrid", 
               rango_min=0, rango_max=1, precio_fijo=28.00),
        Tarifa(servicio=gls_pie_calle, provincia="Madrid", 
               rango_min=1, rango_max=3, precio_fijo=55.00),
        Tarifa(servicio=gls_pie_calle, provincia="Madrid", 
               rango_min=3, rango_max=6, precio_fijo=95.00),
        Tarifa(servicio=gls_pie_calle, provincia="Madrid", 
               rango_min=6, rango_max=None, precio_fijo=145.00),
        
        Tarifa(servicio=gls_pie_calle, provincia="Barcelona", 
               rango_min=0, rango_max=2, precio_fijo=38.00),
        Tarifa(servicio=gls_pie_calle, provincia="Barcelona", 
               rango_min=2, rango_max=5, precio_fijo=75.00),
        Tarifa(servicio=gls_pie_calle, provincia="Barcelona", 
               rango_min=5, rango_max=None, precio_fijo=135.00),
        
        Tarifa(servicio=gls_pie_calle, provincia="NACIONAL", 
               rango_min=0, rango_max=2, precio_fijo=42.00),
        Tarifa(servicio=gls_pie_calle, provincia="NACIONAL", 
               rango_min=2, rango_max=5, precio_fijo=85.00),
        Tarifa(servicio=gls_pie_calle, provincia="NACIONAL", 
               rango_min=5, rango_max=None, precio_fijo=155.00),
    ])
    
    # --- GLS - Subida a domicilio ---
    tarifas.extend([
        Tarifa(servicio=gls_subida_domicilio, provincia="Madrid", 
               rango_min=0, rango_max=2, precio_fijo=45.00),
        Tarifa(servicio=gls_subida_domicilio, provincia="Madrid", 
               rango_min=2, rango_max=5, precio_fijo=85.00),
        Tarifa(servicio=gls_subida_domicilio, provincia="Madrid", 
               rango_min=5, rango_max=None, precio_fijo=145.00),
        
        Tarifa(servicio=gls_subida_domicilio, provincia="NACIONAL", 
               rango_min=0, rango_max=3, precio_fijo=62.00),
        Tarifa(servicio=gls_subida_domicilio, provincia="NACIONAL", 
               rango_min=3, rango_max=None, precio_fijo=115.00),
    ])
    
    # --- DHL (por PESO) - Pie de calle (MUY COMPETITIVO) ---
    tarifas.extend([
        Tarifa(servicio=dhl_pie_calle, provincia="Madrid", 
               rango_min=0, rango_max=15, precio_fijo=6.50),
        Tarifa(servicio=dhl_pie_calle, provincia="Madrid", 
               rango_min=15, rango_max=40, precio_fijo=10.50),
        Tarifa(servicio=dhl_pie_calle, provincia="Madrid", 
               rango_min=40, rango_max=80, precio_fijo=18.00),
        Tarifa(servicio=dhl_pie_calle, provincia="Madrid", 
               rango_min=80, rango_max=150, precio_fijo=30.00),
        Tarifa(servicio=dhl_pie_calle, provincia="Madrid", 
               rango_min=150, rango_max=None, precio_fijo=48.00),
        
        Tarifa(servicio=dhl_pie_calle, provincia="Barcelona", 
               rango_min=0, rango_max=20, precio_fijo=8.00),
        Tarifa(servicio=dhl_pie_calle, provincia="Barcelona", 
               rango_min=20, rango_max=60, precio_fijo=14.00),
        Tarifa(servicio=dhl_pie_calle, provincia="Barcelona", 
               rango_min=60, rango_max=120, precio_fijo=25.00),
        Tarifa(servicio=dhl_pie_calle, provincia="Barcelona", 
               rango_min=120, rango_max=None, precio_fijo=45.00),
        
        Tarifa(servicio=dhl_pie_calle, provincia="Valencia", 
               rango_min=0, rango_max=25, precio_fijo=9.50),
        Tarifa(servicio=dhl_pie_calle, provincia="Valencia", 
               rango_min=25, rango_max=75, precio_fijo=17.00),
        Tarifa(servicio=dhl_pie_calle, provincia="Valencia", 
               rango_min=75, rango_max=None, precio_fijo=35.00),
        
        Tarifa(servicio=dhl_pie_calle, provincia="NACIONAL", 
               rango_min=0, rango_max=30, precio_fijo=12.00),
        Tarifa(servicio=dhl_pie_calle, provincia="NACIONAL", 
               rango_min=30, rango_max=80, precio_fijo=22.00),
        Tarifa(servicio=dhl_pie_calle, provincia="NACIONAL", 
               rango_min=80, rango_max=None, precio_fijo=45.00),
    ])
    
    # --- DHL - Subida a domicilio ---
    tarifas.extend([
        Tarifa(servicio=dhl_subida_domicilio, provincia="Madrid", 
               rango_min=0, rango_max=30, precio_fijo=17.00),
        Tarifa(servicio=dhl_subida_domicilio, provincia="Madrid", 
               rango_min=30, rango_max=80, precio_fijo=28.00),
        Tarifa(servicio=dhl_subida_domicilio, provincia="Madrid", 
               rango_min=80, rango_max=None, precio_fijo=48.00),
        
        Tarifa(servicio=dhl_subida_domicilio, provincia="Barcelona", 
               rango_min=0, rango_max=40, precio_fijo=20.00),
        Tarifa(servicio=dhl_subida_domicilio, provincia="Barcelona", 
               rango_min=40, rango_max=None, precio_fijo=35.00),
        
        Tarifa(servicio=dhl_subida_domicilio, provincia="NACIONAL", 
               rango_min=0, rango_max=50, precio_fijo=24.00),
        Tarifa(servicio=dhl_subida_domicilio, provincia="NACIONAL", 
               rango_min=50, rango_max=None, precio_fijo=42.00),
    ])
    
    # --- DHL - Instalación ---
    tarifas.extend([
        Tarifa(servicio=dhl_instalacion, provincia="Madrid", 
               rango_min=0, rango_max=40, precio_fijo=48.00),
        Tarifa(servicio=dhl_instalacion, provincia="Madrid", 
               rango_min=40, rango_max=100, precio_fijo=72.00),
        Tarifa(servicio=dhl_instalacion, provincia="Madrid", 
               rango_min=100, rango_max=None, precio_fijo=110.00),
        
        Tarifa(servicio=dhl_instalacion, provincia="Barcelona", 
               rango_min=0, rango_max=50, precio_fijo=55.00),
        Tarifa(servicio=dhl_instalacion, provincia="Barcelona", 
               rango_min=50, rango_max=None, precio_fijo=85.00),
        
        Tarifa(servicio=dhl_instalacion, provincia="NACIONAL", 
               rango_min=0, rango_max=60, precio_fijo=68.00),
        Tarifa(servicio=dhl_instalacion, provincia="NACIONAL", 
               rango_min=60, rango_max=None, precio_fijo=105.00),
    ])
    
    # --- Correos Express (por VOLUMEN) - Económico para pequeños volúmenes ---
    tarifas.extend([
        Tarifa(servicio=correos_pie_calle, provincia="Madrid", 
               rango_min=0, rango_max=0.5, precio_fijo=8.00),
        Tarifa(servicio=correos_pie_calle, provincia="Madrid", 
               rango_min=0.5, rango_max=1.5, precio_fijo=14.00),
        Tarifa(servicio=correos_pie_calle, provincia="Madrid", 
               rango_min=1.5, rango_max=3, precio_fijo=26.00),
        Tarifa(servicio=correos_pie_calle, provincia="Madrid", 
               rango_min=3, rango_max=5, precio_fijo=42.00),
        Tarifa(servicio=correos_pie_calle, provincia="Madrid", 
               rango_min=5, rango_max=None, precio_fijo=65.00),
        
        Tarifa(servicio=correos_pie_calle, provincia="Barcelona", 
               rango_min=0, rango_max=1, precio_fijo=11.00),
        Tarifa(servicio=correos_pie_calle, provincia="Barcelona", 
               rango_min=1, rango_max=2.5, precio_fijo=22.00),
        Tarifa(servicio=correos_pie_calle, provincia="Barcelona", 
               rango_min=2.5, rango_max=None, precio_fijo=45.00),
        
        Tarifa(servicio=correos_pie_calle, provincia="Valencia", 
               rango_min=0, rango_max=1.5, precio_fijo=14.00),
        Tarifa(servicio=correos_pie_calle, provincia="Valencia", 
               rango_min=1.5, rango_max=4, precio_fijo=32.00),
        Tarifa(servicio=correos_pie_calle, provincia="Valencia", 
               rango_min=4, rango_max=None, precio_fijo=58.00),
        
        Tarifa(servicio=correos_pie_calle, provincia="Sevilla", 
               rango_min=0, rango_max=2, precio_fijo=18.00),
        Tarifa(servicio=correos_pie_calle, provincia="Sevilla", 
               rango_min=2, rango_max=None, precio_fijo=42.00),
        
        Tarifa(servicio=correos_pie_calle, provincia="NACIONAL", 
               rango_min=0, rango_max=2, precio_fijo=22.00),
        Tarifa(servicio=correos_pie_calle, provincia="NACIONAL", 
               rango_min=2, rango_max=5, precio_fijo=48.00),
        Tarifa(servicio=correos_pie_calle, provincia="NACIONAL", 
               rango_min=5, rango_max=None, precio_fijo=85.00),
    ])
    
    # --- Correos Express - Subida a domicilio ---
    tarifas.extend([
        Tarifa(servicio=correos_subida_domicilio, provincia="Madrid", 
               rango_min=0, rango_max=1, precio_fijo=22.00),
        Tarifa(servicio=correos_subida_domicilio, provincia="Madrid", 
               rango_min=1, rango_max=3, precio_fijo=38.00),
        Tarifa(servicio=correos_subida_domicilio, provincia="Madrid", 
               rango_min=3, rango_max=None, precio_fijo=62.00),
        
        Tarifa(servicio=correos_subida_domicilio, provincia="Barcelona", 
               rango_min=0, rango_max=1.5, precio_fijo=28.00),
        Tarifa(servicio=correos_subida_domicilio, provincia="Barcelona", 
               rango_min=1.5, rango_max=None, precio_fijo=52.00),
        
        Tarifa(servicio=correos_subida_domicilio, provincia="NACIONAL", 
               rango_min=0, rango_max=2, precio_fijo=35.00),
        Tarifa(servicio=correos_subida_domicilio, provincia="NACIONAL", 
               rango_min=2, rango_max=None, precio_fijo=68.00),
    ])
    
    # --- Nacex (por PALETS) - Competitivo para grandes volúmenes ---
    tarifas.extend([
        Tarifa(servicio=nacex_pie_calle, provincia="Madrid", 
               rango_min=0, rango_max=1, precio_fijo=26.00),
        Tarifa(servicio=nacex_pie_calle, provincia="Madrid", 
               rango_min=1, rango_max=3, precio_fijo=52.00),
        Tarifa(servicio=nacex_pie_calle, provincia="Madrid", 
               rango_min=3, rango_max=6, precio_fijo=92.00),
        Tarifa(servicio=nacex_pie_calle, provincia="Madrid", 
               rango_min=6, rango_max=None, precio_fijo=142.00),
        
        Tarifa(servicio=nacex_pie_calle, provincia="Barcelona", 
               rango_min=0, rango_max=2, precio_fijo=36.00),
        Tarifa(servicio=nacex_pie_calle, provincia="Barcelona", 
               rango_min=2, rango_max=5, precio_fijo=72.00),
        Tarifa(servicio=nacex_pie_calle, provincia="Barcelona", 
               rango_min=5, rango_max=None, precio_fijo=132.00),
        
        Tarifa(servicio=nacex_pie_calle, provincia="Valencia", 
               rango_min=0, rango_max=2.5, precio_fijo=42.00),
        Tarifa(servicio=nacex_pie_calle, provincia="Valencia", 
               rango_min=2.5, rango_max=None, precio_fijo=85.00),
        
        Tarifa(servicio=nacex_pie_calle, provincia="NACIONAL", 
               rango_min=0, rango_max=2, precio_fijo=45.00),
        Tarifa(servicio=nacex_pie_calle, provincia="NACIONAL", 
               rango_min=2, rango_max=5, precio_fijo=88.00),
        Tarifa(servicio=nacex_pie_calle, provincia="NACIONAL", 
               rango_min=5, rango_max=None, precio_fijo=158.00),
    ])
    
    # --- Nacex - Subida a domicilio ---
    tarifas.extend([
        Tarifa(servicio=nacex_subida_domicilio, provincia="Madrid", 
               rango_min=0, rango_max=2, precio_fijo=42.00),
        Tarifa(servicio=nacex_subida_domicilio, provincia="Madrid", 
               rango_min=2, rango_max=5, precio_fijo=82.00),
        Tarifa(servicio=nacex_subida_domicilio, provincia="Madrid", 
               rango_min=5, rango_max=None, precio_fijo=142.00),
        
        Tarifa(servicio=nacex_subida_domicilio, provincia="Barcelona", 
               rango_min=0, rango_max=3, precio_fijo=52.00),
        Tarifa(servicio=nacex_subida_domicilio, provincia="Barcelona", 
               rango_min=3, rango_max=None, precio_fijo=98.00),
        
        Tarifa(servicio=nacex_subida_domicilio, provincia="NACIONAL", 
               rango_min=0, rango_max=3, precio_fijo=68.00),
        Tarifa(servicio=nacex_subida_domicilio, provincia="NACIONAL", 
               rango_min=3, rango_max=None, precio_fijo=125.00),
    ])
    
    # --- Nacex - Instalación ---
    tarifas.extend([
        Tarifa(servicio=nacex_instalacion, provincia="Madrid", 
               rango_min=0, rango_max=2, precio_fijo=65.00),
        Tarifa(servicio=nacex_instalacion, provincia="Madrid", 
               rango_min=2, rango_max=5, precio_fijo=105.00),
        Tarifa(servicio=nacex_instalacion, provincia="Madrid", 
               rango_min=5, rango_max=None, precio_fijo=165.00),
        
        Tarifa(servicio=nacex_instalacion, provincia="Barcelona", 
               rango_min=0, rango_max=3, precio_fijo=78.00),
        Tarifa(servicio=nacex_instalacion, provincia="Barcelona", 
               rango_min=3, rango_max=None, precio_fijo=135.00),
        
        Tarifa(servicio=nacex_instalacion, provincia="NACIONAL", 
               rango_min=0, rango_max=3, precio_fijo=92.00),
        Tarifa(servicio=nacex_instalacion, provincia="NACIONAL", 
               rango_min=3, rango_max=None, precio_fijo=158.00),
    ])
    
    session.add_all(tarifas)
    session.flush()
    print(f"   ✓ {len(tarifas)} tarifas creadas")
    
    # ========== PRODUCTOS ==========
    print("\n4️⃣ Creando productos...")
    
    productos = [
        # Muebles grandes
        Producto(codigo="SOF001", nombre="Sofá 2 plazas", peso_kg=45.0, volumen_m3=1.8),
        Producto(codigo="SOF002", nombre="Sofá 3 plazas", peso_kg=62.0, volumen_m3=2.4),
        Producto(codigo="SOF003", nombre="Sofá cama", peso_kg=75.0, volumen_m3=2.0),
        Producto(codigo="ARM001", nombre="Armario 3 puertas", peso_kg=65.0, volumen_m3=2.2),
        Producto(codigo="ARM002", nombre="Armario 2 puertas", peso_kg=42.0, volumen_m3=1.5),
        Producto(codigo="CAM001", nombre="Cama matrimonio", peso_kg=55.0, volumen_m3=1.5),
        Producto(codigo="CAM002", nombre="Cama individual", peso_kg=32.0, volumen_m3=0.9),
        Producto(codigo="LIT001", nombre="Litera infantil", peso_kg=48.0, volumen_m3=1.8),
        
        # Mesas y sillas
        Producto(codigo="MES001", nombre="Mesa comedor madera", peso_kg=28.0, volumen_m3=0.5),
        Producto(codigo="MES002", nombre="Mesa extensible", peso_kg=35.0, volumen_m3=0.7),
        Producto(codigo="MES003", nombre="Mesa escritorio", peso_kg=18.0, volumen_m3=0.4),
        Producto(codigo="SIL001", nombre="Silla oficina ergonómica", peso_kg=12.0, volumen_m3=0.3),
        Producto(codigo="SIL002", nombre="Silla comedor", peso_kg=7.5, volumen_m3=0.2),
        Producto(codigo="SIL003", nombre="Sillón relax", peso_kg=38.0, volumen_m3=1.2),
        
        # Almacenamiento
        Producto(codigo="EST001", nombre="Estantería 5 baldas", peso_kg=18.0, volumen_m3=0.6),
        Producto(codigo="EST002", nombre="Estantería modular", peso_kg=25.0, volumen_m3=0.8),
        Producto(codigo="COM001", nombre="Cómoda 4 cajones", peso_kg=35.0, volumen_m3=0.7),
        Producto(codigo="VIT001", nombre="Vitrina cristal", peso_kg=52.0, volumen_m3=1.1),
        
        # Decoración y accesorios
        Producto(codigo="LAM001", nombre="Lámpara pie", peso_kg=3.5, volumen_m3=0.1),
        Producto(codigo="LAM002", nombre="Lámpara techo", peso_kg=2.5, volumen_m3=0.08),
        Producto(codigo="ALF001", nombre="Alfombra 200x300cm", peso_kg=8.0, volumen_m3=0.2),
        Producto(codigo="ALF002", nombre="Alfombra 150x200cm", peso_kg=5.0, volumen_m3=0.12),
        Producto(codigo="ESP001", nombre="Espejo pared grande", peso_kg=15.0, volumen_m3=0.15),
        Producto(codigo="CUA001", nombre="Cuadro decorativo", peso_kg=4.0, volumen_m3=0.05),
        
        # Electrodomésticos (peso significativo)
        Producto(codigo="NEV001", nombre="Nevera 2 puertas", peso_kg=85.0, volumen_m3=1.2),
        Producto(codigo="LAV001", nombre="Lavadora 8kg", peso_kg=70.0, volumen_m3=0.8),
        Producto(codigo="LVJ001", nombre="Lavavajillas", peso_kg=45.0, volumen_m3=0.6),
        Producto(codigo="HOR001", nombre="Horno eléctrico", peso_kg=35.0, volumen_m3=0.4),
    ]
    
    session.add_all(productos)
    session.flush()
    print(f"   ✓ {len(productos)} productos creados")
    
    # ========== PEDIDOS DE PRUEBA ==========
    print("\n5️⃣ Creando pedidos de prueba...")
    
    # Pedido 1: Pequeño - Pie de calle - Madrid
    pedido1 = Pedido(
        numero_pedido="PED-2024-001",
        provincia_entrega="Madrid",
        tipo_entrega=TipoEntrega.PIE_CALLE
    )
    session.add(pedido1)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido1, producto=next(p for p in productos if p.codigo == "MES001"), cantidad=1),
        PedidoProducto(pedido=pedido1, producto=next(p for p in productos if p.codigo == "SIL002"), cantidad=4),
    ])
    print(f"   ✓ {pedido1.numero_pedido} - Madrid, Pie de calle (Mesa + 4 Sillas)")
    
    # Pedido 2: Mediano - Subida a domicilio - Barcelona
    pedido2 = Pedido(
        numero_pedido="PED-2024-002",
        provincia_entrega="Barcelona",
        tipo_entrega=TipoEntrega.SUBIDA_DOMICILIO
    )
    session.add(pedido2)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido2, producto=next(p for p in productos if p.codigo == "SOF001"), cantidad=1),
        PedidoProducto(pedido=pedido2, producto=next(p for p in productos if p.codigo == "LAM001"), cantidad=2),
        PedidoProducto(pedido=pedido2, producto=next(p for p in productos if p.codigo == "ALF001"), cantidad=1),
    ])
    print(f"   ✓ {pedido2.numero_pedido} - Barcelona, Subida a domicilio (Sofá + Lámparas + Alfombra)")
    
    # Pedido 3: Grande - Instalación - Madrid
    pedido3 = Pedido(
        numero_pedido="PED-2024-003",
        provincia_entrega="Madrid",
        tipo_entrega=TipoEntrega.SUBIDA_INSTALACION
    )
    session.add(pedido3)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido3, producto=next(p for p in productos if p.codigo == "CAM001"), cantidad=1),
        PedidoProducto(pedido=pedido3, producto=next(p for p in productos if p.codigo == "ARM001"), cantidad=1),
        PedidoProducto(pedido=pedido3, producto=next(p for p in productos if p.codigo == "EST001"), cantidad=2),
    ])
    print(f"   ✓ {pedido3.numero_pedido} - Madrid, Instalación (Cama + Armario + 2 Estanterías)")
    
    # Pedido 4: Muy pesado - Pie de calle - Sevilla (NACIONAL)
    pedido4 = Pedido(
        numero_pedido="PED-2024-004",
        provincia_entrega="Sevilla",
        tipo_entrega=TipoEntrega.PIE_CALLE
    )
    session.add(pedido4)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido4, producto=next(p for p in productos if p.codigo == "SOF002"), cantidad=2),
        PedidoProducto(pedido=pedido4, producto=next(p for p in productos if p.codigo == "ARM001"), cantidad=1),
        PedidoProducto(pedido=pedido4, producto=next(p for p in productos if p.codigo == "MES002"), cantidad=1),
    ])
    print(f"   ✓ {pedido4.numero_pedido} - Sevilla, Pie de calle (2 Sofás 3 plazas + Armario + Mesa extensible)")
    
    # Pedido 5: Muchos artículos pequeños - Subida a domicilio - Valencia
    pedido5 = Pedido(
        numero_pedido="PED-2024-005",
        provincia_entrega="Valencia",
        tipo_entrega=TipoEntrega.SUBIDA_DOMICILIO
    )
    session.add(pedido5)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido5, producto=next(p for p in productos if p.codigo == "SIL001"), cantidad=6),
        PedidoProducto(pedido=pedido5, producto=next(p for p in productos if p.codigo == "LAM001"), cantidad=3),
        PedidoProducto(pedido=pedido5, producto=next(p for p in productos if p.codigo == "ALF002"), cantidad=2),
    ])
    print(f"   ✓ {pedido5.numero_pedido} - Valencia, Subida a domicilio (6 Sillas + 3 Lámparas + 2 Alfombras)")
    
    # Pedido 6: Mudanza completa - Instalación - Madrid
    pedido6 = Pedido(
        numero_pedido="PED-2024-006",
        provincia_entrega="Madrid",
        tipo_entrega=TipoEntrega.SUBIDA_INSTALACION
    )
    session.add(pedido6)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido6, producto=next(p for p in productos if p.codigo == "SOF003"), cantidad=1),
        PedidoProducto(pedido=pedido6, producto=next(p for p in productos if p.codigo == "ARM002"), cantidad=2),
        PedidoProducto(pedido=pedido6, producto=next(p for p in productos if p.codigo == "MES001"), cantidad=1),
        PedidoProducto(pedido=pedido6, producto=next(p for p in productos if p.codigo == "SIL002"), cantidad=6),
        PedidoProducto(pedido=pedido6, producto=next(p for p in productos if p.codigo == "EST002"), cantidad=2),
        PedidoProducto(pedido=pedido6, producto=next(p for p in productos if p.codigo == "LAM002"), cantidad=4),
    ])
    print(f"   ✓ {pedido6.numero_pedido} - Madrid, Instalación (Mudanza completa: Sofá + 2 Armarios + Mesa + 6 Sillas + 2 Estanterías + 4 Lámparas)")
    
    # Pedido 7: Oficina - Pie de calle - Barcelona
    pedido7 = Pedido(
        numero_pedido="PED-2024-007",
        provincia_entrega="Barcelona",
        tipo_entrega=TipoEntrega.PIE_CALLE
    )
    session.add(pedido7)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido7, producto=next(p for p in productos if p.codigo == "MES003"), cantidad=5),
        PedidoProducto(pedido=pedido7, producto=next(p for p in productos if p.codigo == "SIL001"), cantidad=5),
        PedidoProducto(pedido=pedido7, producto=next(p for p in productos if p.codigo == "EST001"), cantidad=3),
    ])
    print(f"   ✓ {pedido7.numero_pedido} - Barcelona, Pie de calle (Oficina: 5 Escritorios + 5 Sillas ergonómicas + 3 Estanterías)")
    
    # Pedido 8: Electrodomésticos - Subida a domicilio - Valencia
    pedido8 = Pedido(
        numero_pedido="PED-2024-008",
        provincia_entrega="Valencia",
        tipo_entrega=TipoEntrega.SUBIDA_DOMICILIO
    )
    session.add(pedido8)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido8, producto=next(p for p in productos if p.codigo == "NEV001"), cantidad=1),
        PedidoProducto(pedido=pedido8, producto=next(p for p in productos if p.codigo == "LAV001"), cantidad=1),
        PedidoProducto(pedido=pedido8, producto=next(p for p in productos if p.codigo == "LVJ001"), cantidad=1),
    ])
    print(f"   ✓ {pedido8.numero_pedido} - Valencia, Subida a domicilio (Nevera + Lavadora + Lavavajillas)")
    
    # Pedido 9: Decoración - Pie de calle - Sevilla
    pedido9 = Pedido(
        numero_pedido="PED-2024-009",
        provincia_entrega="Sevilla",
        tipo_entrega=TipoEntrega.PIE_CALLE
    )
    session.add(pedido9)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido9, producto=next(p for p in productos if p.codigo == "ESP001"), cantidad=2),
        PedidoProducto(pedido=pedido9, producto=next(p for p in productos if p.codigo == "CUA001"), cantidad=5),
        PedidoProducto(pedido=pedido9, producto=next(p for p in productos if p.codigo == "LAM002"), cantidad=3),
        PedidoProducto(pedido=pedido9, producto=next(p for p in productos if p.codigo == "ALF001"), cantidad=2),
    ])
    print(f"   ✓ {pedido9.numero_pedido} - Sevilla, Pie de calle (Decoración: 2 Espejos + 5 Cuadros + 3 Lámparas + 2 Alfombras)")
    
    # Pedido 10: Dormitorio infantil - Instalación - Barcelona
    pedido10 = Pedido(
        numero_pedido="PED-2024-010",
        provincia_entrega="Barcelona",
        tipo_entrega=TipoEntrega.SUBIDA_INSTALACION
    )
    session.add(pedido10)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido10, producto=next(p for p in productos if p.codigo == "LIT001"), cantidad=1),
        PedidoProducto(pedido=pedido10, producto=next(p for p in productos if p.codigo == "ARM002"), cantidad=1),
        PedidoProducto(pedido=pedido10, producto=next(p for p in productos if p.codigo == "MES003"), cantidad=1),
        PedidoProducto(pedido=pedido10, producto=next(p for p in productos if p.codigo == "EST001"), cantidad=1),
    ])
    print(f"   ✓ {pedido10.numero_pedido} - Barcelona, Instalación (Dormitorio infantil: Litera + Armario + Escritorio + Estantería)")
    
    # Pedido 11: Salón completo - Instalación - Valencia
    pedido11 = Pedido(
        numero_pedido="PED-2024-011",
        provincia_entrega="Valencia",
        tipo_entrega=TipoEntrega.SUBIDA_INSTALACION
    )
    session.add(pedido11)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido11, producto=next(p for p in productos if p.codigo == "SOF002"), cantidad=1),
        PedidoProducto(pedido=pedido11, producto=next(p for p in productos if p.codigo == "SIL003"), cantidad=2),
        PedidoProducto(pedido=pedido11, producto=next(p for p in productos if p.codigo == "VIT001"), cantidad=1),
        PedidoProducto(pedido=pedido11, producto=next(p for p in productos if p.codigo == "MES001"), cantidad=1),
        PedidoProducto(pedido=pedido11, producto=next(p for p in productos if p.codigo == "LAM001"), cantidad=2),
    ])
    print(f"   ✓ {pedido11.numero_pedido} - Valencia, Instalación (Salón: Sofá 3p + 2 Sillones + Vitrina + Mesa + 2 Lámparas)")
    
    # Pedido 12: Tienda pequeña - Pie de calle - Madrid
    pedido12 = Pedido(
        numero_pedido="PED-2024-012",
        provincia_entrega="Madrid",
        tipo_entrega=TipoEntrega.PIE_CALLE
    )
    session.add(pedido12)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido12, producto=next(p for p in productos if p.codigo == "EST002"), cantidad=4),
        PedidoProducto(pedido=pedido12, producto=next(p for p in productos if p.codigo == "VIT001"), cantidad=2),
        PedidoProducto(pedido=pedido12, producto=next(p for p in productos if p.codigo == "ESP001"), cantidad=1),
    ])
    print(f"   ✓ {pedido12.numero_pedido} - Madrid, Pie de calle (Tienda: 4 Estanterías + 2 Vitrinas + Espejo)")
    
    # Pedido 13: Comedor extenso - Subida domicilio - Barcelona
    pedido13 = Pedido(
        numero_pedido="PED-2024-013",
        provincia_entrega="Barcelona",
        tipo_entrega=TipoEntrega.SUBIDA_DOMICILIO
    )
    session.add(pedido13)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido13, producto=next(p for p in productos if p.codigo == "MES002"), cantidad=1),
        PedidoProducto(pedido=pedido13, producto=next(p for p in productos if p.codigo == "SIL002"), cantidad=8),
        PedidoProducto(pedido=pedido13, producto=next(p for p in productos if p.codigo == "COM001"), cantidad=1),
        PedidoProducto(pedido=pedido13, producto=next(p for p in productos if p.codigo == "LAM002"), cantidad=1),
    ])
    print(f"   ✓ {pedido13.numero_pedido} - Barcelona, Subida domicilio (Comedor: Mesa ext. + 8 Sillas + Cómoda + Lámpara)")
    
    # Pedido 14: Hogar nuevo - Instalación - Sevilla
    pedido14 = Pedido(
        numero_pedido="PED-2024-014",
        provincia_entrega="Sevilla",
        tipo_entrega=TipoEntrega.SUBIDA_INSTALACION
    )
    session.add(pedido14)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido14, producto=next(p for p in productos if p.codigo == "CAM001"), cantidad=2),
        PedidoProducto(pedido=pedido14, producto=next(p for p in productos if p.codigo == "ARM001"), cantidad=2),
        PedidoProducto(pedido=pedido14, producto=next(p for p in productos if p.codigo == "SOF001"), cantidad=1),
        PedidoProducto(pedido=pedido14, producto=next(p for p in productos if p.codigo == "MES002"), cantidad=1),
        PedidoProducto(pedido=pedido14, producto=next(p for p in productos if p.codigo == "SIL002"), cantidad=6),
    ])
    print(f"   ✓ {pedido14.numero_pedido} - Sevilla, Instalación (Hogar: 2 Camas + 2 Armarios + Sofá + Mesa + 6 Sillas)")
    
    # Pedido 15: Cocina completa - Subida domicilio - Madrid
    pedido15 = Pedido(
        numero_pedido="PED-2024-015",
        provincia_entrega="Madrid",
        tipo_entrega=TipoEntrega.SUBIDA_DOMICILIO
    )
    session.add(pedido15)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido15, producto=next(p for p in productos if p.codigo == "NEV001"), cantidad=1),
        PedidoProducto(pedido=pedido15, producto=next(p for p in productos if p.codigo == "LVJ001"), cantidad=1),
        PedidoProducto(pedido=pedido15, producto=next(p for p in productos if p.codigo == "HOR001"), cantidad=1),
        PedidoProducto(pedido=pedido15, producto=next(p for p in productos if p.codigo == "MES001"), cantidad=1),
        PedidoProducto(pedido=pedido15, producto=next(p for p in productos if p.codigo == "SIL002"), cantidad=4),
    ])
    print(f"   ✓ {pedido15.numero_pedido} - Madrid, Subida domicilio (Cocina: Nevera + Lavavajillas + Horno + Mesa + 4 Sillas)")
    
    # Pedido 16: Despacho profesional - Pie de calle - Valencia
    pedido16 = Pedido(
        numero_pedido="PED-2024-016",
        provincia_entrega="Valencia",
        tipo_entrega=TipoEntrega.PIE_CALLE
    )
    session.add(pedido16)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido16, producto=next(p for p in productos if p.codigo == "MES003"), cantidad=3),
        PedidoProducto(pedido=pedido16, producto=next(p for p in productos if p.codigo == "SIL001"), cantidad=3),
        PedidoProducto(pedido=pedido16, producto=next(p for p in productos if p.codigo == "EST002"), cantidad=5),
        PedidoProducto(pedido=pedido16, producto=next(p for p in productos if p.codigo == "VIT001"), cantidad=1),
    ])
    print(f"   ✓ {pedido16.numero_pedido} - Valencia, Pie de calle (Despacho: 3 Escritorios + 3 Sillas + 5 Estanterías + Vitrina)")
    
    # Pedido 17: Habitación juvenil - Instalación - Barcelona
    pedido17 = Pedido(
        numero_pedido="PED-2024-017",
        provincia_entrega="Barcelona",
        tipo_entrega=TipoEntrega.SUBIDA_INSTALACION
    )
    session.add(pedido17)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido17, producto=next(p for p in productos if p.codigo == "CAM002"), cantidad=1),
        PedidoProducto(pedido=pedido17, producto=next(p for p in productos if p.codigo == "ARM002"), cantidad=1),
        PedidoProducto(pedido=pedido17, producto=next(p for p in productos if p.codigo == "MES003"), cantidad=1),
        PedidoProducto(pedido=pedido17, producto=next(p for p in productos if p.codigo == "EST001"), cantidad=2),
        PedidoProducto(pedido=pedido17, producto=next(p for p in productos if p.codigo == "LAM001"), cantidad=1),
    ])
    print(f"   ✓ {pedido17.numero_pedido} - Barcelona, Instalación (Juvenil: Cama ind. + Armario + Escritorio + 2 Estanterías + Lámpara)")
    
    # Pedido 18: Restaurante pequeño - Pie de calle - Sevilla
    pedido18 = Pedido(
        numero_pedido="PED-2024-018",
        provincia_entrega="Sevilla",
        tipo_entrega=TipoEntrega.PIE_CALLE
    )
    session.add(pedido18)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido18, producto=next(p for p in productos if p.codigo == "MES001"), cantidad=8),
        PedidoProducto(pedido=pedido18, producto=next(p for p in productos if p.codigo == "SIL002"), cantidad=32),
        PedidoProducto(pedido=pedido18, producto=next(p for p in productos if p.codigo == "ESP001"), cantidad=2),
    ])
    print(f"   ✓ {pedido18.numero_pedido} - Sevilla, Pie de calle (Restaurante: 8 Mesas + 32 Sillas + 2 Espejos)")
    
    # Pedido 19: Piso compartido - Subida domicilio - Madrid
    pedido19 = Pedido(
        numero_pedido="PED-2024-019",
        provincia_entrega="Madrid",
        tipo_entrega=TipoEntrega.SUBIDA_DOMICILIO
    )
    session.add(pedido19)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido19, producto=next(p for p in productos if p.codigo == "CAM002"), cantidad=3),
        PedidoProducto(pedido=pedido19, producto=next(p for p in productos if p.codigo == "MES003"), cantidad=3),
        PedidoProducto(pedido=pedido19, producto=next(p for p in productos if p.codigo == "SIL001"), cantidad=3),
        PedidoProducto(pedido=pedido19, producto=next(p for p in productos if p.codigo == "LAV001"), cantidad=1),
    ])
    print(f"   ✓ {pedido19.numero_pedido} - Madrid, Subida domicilio (Piso compartido: 3 Camas + 3 Escritorios + 3 Sillas + Lavadora)")
    
    # Pedido 20: Almacén showroom - Instalación - Valencia
    pedido20 = Pedido(
        numero_pedido="PED-2024-020",
        provincia_entrega="Valencia",
        tipo_entrega=TipoEntrega.SUBIDA_INSTALACION
    )
    session.add(pedido20)
    session.flush()
    
    session.add_all([
        PedidoProducto(pedido=pedido20, producto=next(p for p in productos if p.codigo == "EST002"), cantidad=10),
        PedidoProducto(pedido=pedido20, producto=next(p for p in productos if p.codigo == "VIT001"), cantidad=3),
        PedidoProducto(pedido=pedido20, producto=next(p for p in productos if p.codigo == "ESP001"), cantidad=4),
        PedidoProducto(pedido=pedido20, producto=next(p for p in productos if p.codigo == "LAM001"), cantidad=6),
    ])
    print(f"   ✓ {pedido20.numero_pedido} - Valencia, Instalación (Showroom: 10 Estanterías + 3 Vitrinas + 4 Espejos + 6 Lámparas)")
    
    session.commit()
    print("\n✅ Datos de ejemplo cargados correctamente\n")
    
    # Resumen
    print("=" * 60)
    print("📊 RESUMEN DE DATOS CARGADOS")
    print("=" * 60)
    print(f"Transportistas:  6 (SEUR, MRW, GLS, DHL, Correos Express, Nacex)")
    print(f"Servicios:       16")
    print(f"Tarifas:         {len(tarifas)}")
    print(f"Productos:       {len(productos)}")
    print(f"Pedidos:         20")
    print("=" * 60)
