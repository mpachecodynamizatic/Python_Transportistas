"""Script de prueba para exportar e importar tarifas"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database import get_db_manager
from main import exportar_tarifas_excel, importar_tarifas_excel

if __name__ == "__main__":
    db_manager = get_db_manager()
    
    print("=" * 60)
    print("PRUEBA DE EXPORTACIÓN/IMPORTACIÓN DE TARIFAS")
    print("=" * 60)
    
    # Exportar tarifas
    print("\n1. Exportando tarifas...")
    with db_manager.get_session() as session:
        exportar_tarifas_excel(session)
    
    print("\n" + "=" * 60)
    print("\nSi quieres probar la importación:")
    print("1. Abre el archivo Excel generado")
    print("2. Modifica algunos precios")
    print("3. Ejecuta: python test_excel_import.py <nombre_archivo>")
    print("\nO ejecuta directamente el menú principal: python main.py")
