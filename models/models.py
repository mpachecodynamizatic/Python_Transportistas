"""
Modelos de datos para el sistema de selección de transportistas

El modelo soporta:
- Múltiples transportistas con varios servicios
- Tarifas por volumen, peso o palets
- Tarifas por provincia y tipo de entrega
- Rangos de precios según cantidad
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class TipoEntrega(enum.Enum):
    """Tipos de entrega disponibles"""
    PIE_CALLE = "pie_calle"
    SUBIDA_DOMICILIO = "subida_domicilio"
    SUBIDA_INSTALACION = "subida_instalacion"


class MetodoCalculo(enum.Enum):
    """Método de cálculo de la tarifa"""
    VOLUMEN = "volumen"  # Por m³
    PESO = "peso"        # Por kg
    PALETS = "palets"    # Por palets (volumen / 2)


class Transportista(Base):
    """Empresa de transporte"""
    __tablename__ = 'transportistas'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    activo = Column(Boolean, default=True, nullable=False)
    
    # Relaciones
    servicios = relationship("ServicioTransportista", back_populates="transportista", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Transportista(id={self.id}, nombre='{self.nombre}')>"


class ServicioTransportista(Base):
    """Servicio ofrecido por un transportista"""
    __tablename__ = 'servicios_transportista'
    
    id = Column(Integer, primary_key=True)
    transportista_id = Column(Integer, ForeignKey('transportistas.id'), nullable=False)
    tipo_entrega = Column(Enum(TipoEntrega), nullable=False)
    metodo_calculo = Column(Enum(MetodoCalculo), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    
    # Relaciones
    transportista = relationship("Transportista", back_populates="servicios")
    tarifas = relationship("Tarifa", back_populates="servicio", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ServicioTransportista(id={self.id}, transportista='{self.transportista.nombre if self.transportista else None}', tipo='{self.tipo_entrega.value}')>"


class Tarifa(Base):
    """
    Tarifa de un servicio de transportista
    
    Estructura de precios por rangos:
    - rango_min a rango_max (en kg, m³ o palets según metodo_calculo)
    - precio_fijo: precio total por el envío en ese rango
    
    Ejemplo: Para 150kg en rango [100-200kg]:
        precio_total = precio_fijo
    """
    __tablename__ = 'tarifas'
    
    id = Column(Integer, primary_key=True)
    servicio_id = Column(Integer, ForeignKey('servicios_transportista.id'), nullable=False)
    provincia = Column(String(50), nullable=False)  # "Madrid", "Barcelona", "NACIONAL"
    rango_min = Column(Numeric(10, 2), nullable=False)  # Mínimo del rango
    rango_max = Column(Numeric(10, 2), nullable=True)   # Máximo del rango (NULL = infinito)
    precio_fijo = Column(Numeric(10, 2), nullable=False)  # Precio total fijo por el rango
    
    # Relaciones
    servicio = relationship("ServicioTransportista", back_populates="tarifas")
    
    def __repr__(self):
        return f"<Tarifa(id={self.id}, provincia='{self.provincia}', rango={self.rango_min}-{self.rango_max}, precio={self.precio_fijo}€)>"


class Producto(Base):
    """Producto con sus características físicas"""
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(200), nullable=False)
    peso_kg = Column(Numeric(10, 2), nullable=False)  # Peso en kilogramos
    volumen_m3 = Column(Numeric(10, 4), nullable=False)  # Volumen en metros cúbicos
    
    # Relaciones
    pedidos = relationship("PedidoProducto", back_populates="producto")
    
    def __repr__(self):
        return f"<Producto(codigo='{self.codigo}', nombre='{self.nombre}', peso={self.peso_kg}kg, volumen={self.volumen_m3}m³)>"


class Pedido(Base):
    """Pedido que contiene productos"""
    __tablename__ = 'pedidos'
    
    id = Column(Integer, primary_key=True)
    numero_pedido = Column(String(50), nullable=False, unique=True)
    provincia_entrega = Column(String(50), nullable=False)
    tipo_entrega = Column(Enum(TipoEntrega), nullable=False)
    
    # Relaciones
    productos = relationship("PedidoProducto", back_populates="pedido", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Pedido(numero='{self.numero_pedido}', provincia='{self.provincia_entrega}', tipo='{self.tipo_entrega.value}')>"


class PedidoProducto(Base):
    """Relación entre pedido y producto (con cantidad)"""
    __tablename__ = 'pedido_producto'
    
    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    
    # Relaciones
    pedido = relationship("Pedido", back_populates="productos")
    producto = relationship("Producto", back_populates="pedidos")
    
    def __repr__(self):
        return f"<PedidoProducto(pedido_id={self.pedido_id}, producto_id={self.producto_id}, cantidad={self.cantidad})>"
