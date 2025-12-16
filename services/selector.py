"""
Servicio para seleccionar el mejor transportista según las condiciones del pedido

Algoritmo:
1. Calcular totales del pedido (peso, volumen, palets)
2. Buscar servicios compatibles (tipo de entrega)
3. Para cada servicio, calcular precio según su método
4. Seleccionar la opción más económica
"""

from typing import List, Optional, Dict, Any
from decimal import Decimal
from dataclasses import dataclass
from sqlalchemy.orm import Session

from models.models import (
    Pedido, Producto, PedidoProducto, Transportista, 
    ServicioTransportista, Tarifa, TipoEntrega, MetodoCalculo
)


@dataclass
class CotizacionResult:
    """Resultado de una cotización de transporte"""
    transportista_id: int
    transportista_nombre: str
    servicio_id: int
    tipo_entrega: str
    metodo_calculo: str
    precio_total: Decimal
    precio_base: Decimal
    precio_variable: Decimal
    cantidad_calculada: Decimal  # kg, m³ o palets
    tarifa_id: int
    provincia: str
    detalles: str
    
    def __repr__(self):
        return (f"CotizacionResult(transportista='{self.transportista_nombre}', "
                f"tipo='{self.tipo_entrega}', precio={self.precio_total}€)")


class TransportistaSelector:
    """Servicio para seleccionar el mejor transportista y calcular precios"""
    
    def __init__(self, session: Session):
        """
        Inicializa el selector
        
        Args:
            session: Sesión de base de datos
        """
        self.session = session
    
    def calcular_totales_pedido(self, pedido: Pedido) -> Dict[str, Decimal]:
        """
        Calcula los totales del pedido
        
        Args:
            pedido: Pedido a calcular
        
        Returns:
            Dict con peso_total, volumen_total y palets_total
        """
        peso_total = Decimal('0')
        volumen_total = Decimal('0')
        
        for pedido_producto in pedido.productos:
            producto = pedido_producto.producto
            cantidad = pedido_producto.cantidad
            
            peso_total += Decimal(str(producto.peso_kg)) * cantidad
            volumen_total += Decimal(str(producto.volumen_m3)) * cantidad
        
        # Calcular palets (volumen / 2)
        palets_total = volumen_total / Decimal('2')
        
        return {
            'peso_total': peso_total,
            'volumen_total': volumen_total,
            'palets_total': palets_total
        }
    
    def obtener_cantidad_segun_metodo(
        self, 
        totales: Dict[str, Decimal], 
        metodo: MetodoCalculo
    ) -> Decimal:
        """
        Obtiene la cantidad según el método de cálculo
        
        Args:
            totales: Diccionario con los totales del pedido
            metodo: Método de cálculo a usar
        
        Returns:
            Cantidad a usar para el cálculo
        """
        if metodo == MetodoCalculo.PESO:
            return totales['peso_total']
        elif metodo == MetodoCalculo.VOLUMEN:
            return totales['volumen_total']
        elif metodo == MetodoCalculo.PALETS:
            return totales['palets_total']
        else:
            raise ValueError(f"Método de cálculo desconocido: {metodo}")
    
    def buscar_tarifa_aplicable(
        self,
        servicio_id: int,
        provincia: str,
        cantidad: Decimal
    ) -> Optional[Tarifa]:
        """
        Busca la tarifa aplicable para un servicio, provincia y cantidad
        
        Busca primero tarifa específica de provincia, luego NACIONAL
        
        Args:
            servicio_id: ID del servicio
            provincia: Provincia de entrega
            cantidad: Cantidad calculada (kg, m³ o palets)
        
        Returns:
            Tarifa aplicable o None si no se encuentra
        """
        # Intentar primero con provincia específica
        tarifas = self.session.query(Tarifa).filter(
            Tarifa.servicio_id == servicio_id,
            Tarifa.provincia.in_([provincia, 'NACIONAL']),
            Tarifa.rango_min <= cantidad,
            (Tarifa.rango_max.is_(None)) | (Tarifa.rango_max >= cantidad)
        ).order_by(
            # Priorizar provincia específica sobre NACIONAL
            Tarifa.provincia.desc()
        ).all()
        
        # Retornar la primera tarifa (provincia específica si existe, sino NACIONAL)
        return tarifas[0] if tarifas else None
    
    def calcular_precio_servicio(
        self,
        servicio: ServicioTransportista,
        provincia: str,
        totales: Dict[str, Decimal]
    ) -> Optional[CotizacionResult]:
        """
        Calcula el precio para un servicio específico
        
        Args:
            servicio: Servicio de transportista
            provincia: Provincia de entrega
            totales: Totales del pedido
        
        Returns:
            CotizacionResult con el precio calculado o None si no aplica
        """
        # Obtener cantidad según método de cálculo
        cantidad = self.obtener_cantidad_segun_metodo(totales, servicio.metodo_calculo)
        
        # Buscar tarifa aplicable
        tarifa = self.buscar_tarifa_aplicable(servicio.id, provincia, cantidad)
        
        if not tarifa:
            return None
        
        # Calcular precio (ahora es fijo por rango)
        precio_total = Decimal(str(tarifa.precio_fijo))
        
        # Crear detalles
        unidad = {
            MetodoCalculo.PESO: 'kg',
            MetodoCalculo.VOLUMEN: 'm³',
            MetodoCalculo.PALETS: 'palets'
        }[servicio.metodo_calculo]
        
        rango_max_str = f"{tarifa.rango_max:.2f}" if tarifa.rango_max else "∞"
        detalles = f"{cantidad:.2f} {unidad} en rango [{tarifa.rango_min:.2f} - {rango_max_str}] = {precio_total:.2f}€"
        
        return CotizacionResult(
            transportista_id=servicio.transportista.id,
            transportista_nombre=servicio.transportista.nombre,
            servicio_id=servicio.id,
            tipo_entrega=servicio.tipo_entrega.value,
            metodo_calculo=servicio.metodo_calculo.value,
            precio_total=precio_total,
            precio_base=Decimal('0'),  # Ya no se usa
            precio_variable=precio_total,  # El precio completo
            cantidad_calculada=cantidad,
            tarifa_id=tarifa.id,
            provincia=tarifa.provincia,
            detalles=detalles
        )
    
    def obtener_mejores_cotizaciones(
        self,
        pedido_id: int,
        limite: int = 5
    ) -> List[CotizacionResult]:
        """
        Obtiene las mejores cotizaciones para un pedido
        
        Args:
            pedido_id: ID del pedido
            limite: Número máximo de cotizaciones a retornar
        
        Returns:
            Lista de cotizaciones ordenadas por precio (menor a mayor)
        """
        # Obtener pedido
        pedido = self.session.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            raise ValueError(f"Pedido {pedido_id} no encontrado")
        
        # Calcular totales
        totales = self.calcular_totales_pedido(pedido)
        
        # Buscar servicios activos que coincidan con el tipo de entrega
        servicios = self.session.query(ServicioTransportista).join(
            Transportista
        ).filter(
            ServicioTransportista.tipo_entrega == pedido.tipo_entrega,
            ServicioTransportista.activo == True,
            Transportista.activo == True
        ).all()
        
        # Calcular precios para cada servicio
        cotizaciones = []
        for servicio in servicios:
            cotizacion = self.calcular_precio_servicio(
                servicio,
                pedido.provincia_entrega,
                totales
            )
            if cotizacion:
                cotizaciones.append(cotizacion)
        
        # Ordenar por precio (menor a mayor)
        cotizaciones.sort(key=lambda x: x.precio_total)
        
        return cotizaciones[:limite]
    
    def seleccionar_mejor_transportista(
        self,
        pedido_id: int
    ) -> Optional[CotizacionResult]:
        """
        Selecciona el mejor transportista (más económico) para un pedido
        
        Args:
            pedido_id: ID del pedido
        
        Returns:
            CotizacionResult del mejor transportista o None si no hay opciones
        """
        cotizaciones = self.obtener_mejores_cotizaciones(pedido_id, limite=1)
        return cotizaciones[0] if cotizaciones else None
    
    def comparar_transportistas(
        self,
        pedido_id: int
    ) -> Dict[str, Any]:
        """
        Compara todos los transportistas disponibles para un pedido
        
        Args:
            pedido_id: ID del pedido
        
        Returns:
            Diccionario con información del pedido y todas las cotizaciones
        """
        pedido = self.session.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            raise ValueError(f"Pedido {pedido_id} no encontrado")
        
        totales = self.calcular_totales_pedido(pedido)
        cotizaciones = self.obtener_mejores_cotizaciones(pedido_id, limite=100)
        
        return {
            'pedido': {
                'numero': pedido.numero_pedido,
                'provincia': pedido.provincia_entrega,
                'tipo_entrega': pedido.tipo_entrega.value,
                'peso_total_kg': float(totales['peso_total']),
                'volumen_total_m3': float(totales['volumen_total']),
                'palets_total': float(totales['palets_total']),
                'productos': [
                    {
                        'codigo': pp.producto.codigo,
                        'nombre': pp.producto.nombre,
                        'cantidad': pp.cantidad,
                        'peso_unitario_kg': float(pp.producto.peso_kg),
                        'volumen_unitario_m3': float(pp.producto.volumen_m3)
                    }
                    for pp in pedido.productos
                ]
            },
            'mejor_opcion': cotizaciones[0] if cotizaciones else None,
            'todas_cotizaciones': cotizaciones,
            'ahorro_mejor_vs_peor': (
                float(cotizaciones[-1].precio_total - cotizaciones[0].precio_total)
                if len(cotizaciones) > 1 else 0
            )
        }
