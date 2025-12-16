"""
Script principal para probar el sistema de selección de transportistas

Demuestra las diferentes funcionalidades:
- Selección del mejor transportista
- Comparación de todas las opciones
- Visualización detallada de cotizaciones
"""

import sys
from pathlib import Path
from decimal import Decimal

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from database import get_db_manager
from services import TransportistaSelector
from models import Pedido, Transportista, ServicioTransportista, Tarifa


def imprimir_separador(caracter="=", longitud=80):
    """Imprime una línea separadora"""
    print(caracter * longitud)


def imprimir_cotizacion(cotizacion, posicion=None):
    """Imprime una cotización de forma bonita"""
    prefijo = f"{posicion}. " if posicion else "• "
    print(f"{prefijo}{cotizacion.transportista_nombre} - {cotizacion.tipo_entrega.replace('_', ' ').title()}")
    print(f"   Método: {cotizacion.metodo_calculo.upper()}")
    print(f"   Cantidad: {cotizacion.cantidad_calculada:.2f}")
    print(f"   Precio: {cotizacion.precio_total:.2f}€")
    print(f"   Desglose: {cotizacion.detalles}")
    print(f"   Provincia tarifa: {cotizacion.provincia}")
    print()


def mostrar_mejor_transportista(pedido_id: int, session):
    """Muestra el mejor transportista para un pedido"""
    selector = TransportistaSelector(session)
    
    # Obtener información del pedido
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
    
    imprimir_separador()
    print(f"🎯 MEJOR TRANSPORTISTA - Pedido {pedido.numero_pedido}")
    imprimir_separador()
    print(f"Provincia: {pedido.provincia_entrega}")
    print(f"Tipo de entrega: {pedido.tipo_entrega.value.replace('_', ' ').title()}")
    print()
    
    # Calcular totales
    totales = selector.calcular_totales_pedido(pedido)
    print(f"📦 TOTALES DEL PEDIDO:")
    print(f"   Peso total: {totales['peso_total']:.2f} kg")
    print(f"   Volumen total: {totales['volumen_total']:.4f} m³")
    print(f"   Palets estimados: {totales['palets_total']:.2f}")
    print()
    
    print("📋 PRODUCTOS:")
    for pp in pedido.productos:
        print(f"   • {pp.producto.nombre} x{pp.cantidad}")
        print(f"     ({pp.producto.peso_kg}kg, {pp.producto.volumen_m3}m³ c/u)")
    print()
    
    # Seleccionar mejor transportista
    mejor = selector.seleccionar_mejor_transportista(pedido_id)
    
    if mejor:
        print("✅ MEJOR OPCIÓN:")
        imprimir_cotizacion(mejor)
    else:
        print("❌ No hay transportistas disponibles para este pedido")
    
    imprimir_separador()
    print()


def comparar_transportistas(pedido_id: int, session):
    """Compara todos los transportistas disponibles para un pedido"""
    selector = TransportistaSelector(session)
    comparacion = selector.comparar_transportistas(pedido_id)
    
    pedido_info = comparacion['pedido']
    mejor = comparacion['mejor_opcion']
    todas = comparacion['todas_cotizaciones']
    ahorro = comparacion['ahorro_mejor_vs_peor']
    
    imprimir_separador()
    print(f"📊 COMPARACIÓN DE TRANSPORTISTAS - Pedido {pedido_info['numero']}")
    imprimir_separador()
    print(f"Provincia: {pedido_info['provincia']}")
    print(f"Tipo de entrega: {pedido_info['tipo_entrega'].replace('_', ' ').title()}")
    print(f"Peso total: {pedido_info['peso_total_kg']:.2f} kg")
    print(f"Volumen total: {pedido_info['volumen_total_m3']:.4f} m³")
    print(f"Palets estimados: {pedido_info['palets_total']:.2f}")
    print()
    
    if not todas:
        print("❌ No hay transportistas disponibles para este pedido")
        imprimir_separador()
        return
    
    print(f"🏆 RANKING DE OPCIONES ({len(todas)} disponibles):")
    print()
    
    for i, cotizacion in enumerate(todas, 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
        print(f"{emoji} ", end="")
        imprimir_cotizacion(cotizacion, i)
    
    if len(todas) > 1:
        print(f"💰 AHORRO: {ahorro:.2f}€ eligiendo la mejor opción")
        porcentaje = (ahorro / float(todas[-1].precio_total)) * 100
        print(f"   ({porcentaje:.1f}% más económico que la opción más cara)")
    
    imprimir_separador()
    print()


def listar_tarifas(session):
    """Lista todas las tarifas organizadas por transportista y servicio"""
    imprimir_separador()
    print("💰 LISTADO DE TARIFAS")
    imprimir_separador()
    
    transportistas = session.query(Transportista).filter(Transportista.activo == True).all()
    
    if not transportistas:
        print("❌ No hay transportistas disponibles")
        return
    
    for transportista in transportistas:
        print(f"\n📦 {transportista.nombre}")
        print("=" * 60)
        
        servicios = session.query(ServicioTransportista).filter(
            ServicioTransportista.transportista_id == transportista.id,
            ServicioTransportista.activo == True
        ).all()
        
        if not servicios:
            print("  Sin servicios activos")
            continue
        
        for servicio in servicios:
            print(f"\n  🚚 Servicio: {servicio.tipo_entrega.value.replace('_', ' ').title()}")
            print(f"     Método de cálculo: {servicio.metodo_calculo.value.upper()}")
            
            tarifas = session.query(Tarifa).filter(
                Tarifa.servicio_id == servicio.id
            ).order_by(Tarifa.provincia, Tarifa.rango_min).all()
            
            if not tarifas:
                print("     Sin tarifas configuradas")
                continue
            
            # Agrupar por provincia
            provincias = {}
            for tarifa in tarifas:
                if tarifa.provincia not in provincias:
                    provincias[tarifa.provincia] = []
                provincias[tarifa.provincia].append(tarifa)
            
            for provincia, tarifas_prov in provincias.items():
                print(f"\n     📍 {provincia}:")
                for tarifa in tarifas_prov:
                    rango_max = f"{tarifa.rango_max:.2f}" if tarifa.rango_max else "∞"
                    unidad = {
                        'peso': 'kg',
                        'volumen': 'm³',
                        'palets': 'palets'
                    }[servicio.metodo_calculo.value]
                    
                    print(f"        • {tarifa.rango_min:.2f} - {rango_max} {unidad}: {tarifa.precio_fijo:.2f}€")
    
    print()
    imprimir_separador()


def menu_principal():
    """Menú interactivo principal"""
    db_manager = get_db_manager()
    
    while True:
        print("\n" + "=" * 60)
        print("🚚 SISTEMA DE SELECCIÓN DE TRANSPORTISTAS")
        print("=" * 60)
        print("\nOpciones:")
        print("1. Ver mejor transportista para cada pedido")
        print("2. Comparar transportistas para un pedido específico")
        print("3. Comparar transportistas para TODOS los pedidos")
        print("4. Listar todos los pedidos")
        print("5. Listar tarifas de todos los transportistas")
        print("6. Salir")
        print()
        
        opcion = input("Selecciona una opción (1-6): ").strip()
        
        if opcion == '1':
            with db_manager.get_session() as session:
                pedidos = session.query(Pedido).all()
                for pedido in pedidos:
                    mostrar_mejor_transportista(pedido.id, session)
                    input("Presiona ENTER para continuar...")
        
        elif opcion == '2':
            with db_manager.get_session() as session:
                pedidos = session.query(Pedido).all()
                print("\nPedidos disponibles:")
                for i, p in enumerate(pedidos, 1):
                    print(f"{i}. {p.numero_pedido} - {p.provincia_entrega} - {p.tipo_entrega.value}")
                
                try:
                    seleccion = int(input("\nSelecciona un pedido (número): ")) - 1
                    if 0 <= seleccion < len(pedidos):
                        comparar_transportistas(pedidos[seleccion].id, session)
                        input("Presiona ENTER para continuar...")
                    else:
                        print("❌ Selección inválida")
                except ValueError:
                    print("❌ Entrada inválida")
        
        elif opcion == '3':
            with db_manager.get_session() as session:
                pedidos = session.query(Pedido).all()
                for pedido in pedidos:
                    comparar_transportistas(pedido.id, session)
                    input("Presiona ENTER para continuar...")
        
        elif opcion == '4':
            with db_manager.get_session() as session:
                selector = TransportistaSelector(session)
                pedidos = session.query(Pedido).all()
                print("\n📦 LISTADO DE PEDIDOS:")
                print()
                # Encabezado de la tabla
                print(f"{'Pedido':<15} {'Provincia':<15} {'Tipo Entrega':<25} {'Prods':>5} {'Peso (kg)':>10} {'Volumen (m³)':>13} {'Palets':>8}")
                print("=" * 120)
                # Datos
                for pedido in pedidos:
                    totales = selector.calcular_totales_pedido(pedido)
                    tipo_entrega = pedido.tipo_entrega.value.replace('_', ' ').title()
                    print(f"{pedido.numero_pedido:<15} {pedido.provincia_entrega:<15} {tipo_entrega:<25} {len(pedido.productos):>5} {totales['peso_total']:>10.2f} {totales['volumen_total']:>13.4f} {totales['palets_total']:>8.2f}")
                print()
                input("Presiona ENTER para continuar...")
        
        elif opcion == '5':
            with db_manager.get_session() as session:
                listar_tarifas(session)
                input("Presiona ENTER para continuar...")
        
        elif opcion == '6':
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida")


def demo_rapido():
    """Demostración rápida del sistema"""
    print("\n" + "=" * 60)
    print("🚀 DEMOSTRACIÓN RÁPIDA DEL SISTEMA")
    print("=" * 60)
    print()
    
    db_manager = get_db_manager()
    
    with db_manager.get_session() as session:
        pedidos = session.query(Pedido).all()
        
        print(f"Se analizarán {len(pedidos)} pedidos de ejemplo...\n")
        
        for pedido in pedidos:
            comparar_transportistas(pedido.id, session)
            print()


if __name__ == "__main__":
    # Verificar si la base de datos existe
    db_path = Path(__file__).parent / "transportistas.db"
    
    if not db_path.exists():
        print("\n⚠️  La base de datos no existe.")
        print("Por favor, ejecuta primero: python init_db.py\n")
        sys.exit(1)
    
    # Preguntar modo de ejecución
    print("\n¿Cómo deseas ejecutar el programa?")
    print("1. Demostración rápida (muestra todos los pedidos)")
    print("2. Menú interactivo")
    
    modo = input("\nSelecciona (1 o 2): ").strip()
    
    if modo == '1':
        demo_rapido()
    else:
        menu_principal()
