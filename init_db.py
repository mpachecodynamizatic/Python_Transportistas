"""
Script de inicialización de la base de datos

Crea las tablas y carga los datos de ejemplo
"""

import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from database import get_db_manager
from data import cargar_datos_ejemplo


def main():
    """Inicializa la base de datos con datos de ejemplo"""
    print("=" * 60)
    print("INICIALIZACIÓN DE LA BASE DE DATOS")
    print("=" * 60)
    
    # Obtener gestor de base de datos
    db_manager = get_db_manager()
    
    # Preguntar si resetear la base de datos
    respuesta = input("\n¿Deseas resetear la base de datos? (s/N): ").strip().lower()
    
    if respuesta == 's':
        print("\n🔄 Reseteando base de datos...")
        db_manager.reset_database()
    else:
        print("\n📝 Creando tablas (si no existen)...")
        db_manager.create_tables()
    
    # Cargar datos de ejemplo
    respuesta_datos = input("\n¿Deseas cargar datos de ejemplo? (S/n): ").strip().lower()
    
    if respuesta_datos != 'n':
        with db_manager.get_session() as session:
            cargar_datos_ejemplo(session)
    
    print("\n✅ Inicialización completada")
    print(f"📍 Base de datos ubicada en: {db_manager.db_path}\n")


if __name__ == "__main__":
    main()
