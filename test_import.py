"""Script de prueba para importar tarifas modificadas"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database import get_db_manager
from main import importar_tarifas_excel

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Buscar el archivo más reciente
        excel_files = list(Path(".").glob("tarifas_export_*.xlsx"))
        if excel_files:
            # Ordenar por fecha de modificación
            archivo = sorted(excel_files, key=lambda x: x.stat().st_mtime, reverse=True)[0]
            print(f"Usando el archivo más reciente: {archivo.name}")
        else:
            print("❌ No se encontró ningún archivo de tarifas.")
            print("Uso: python test_import.py <archivo.xlsx>")
            sys.exit(1)
    else:
        archivo = sys.argv[1]
    
    print("=" * 60)
    print("PRUEBA DE IMPORTACIÓN DE TARIFAS")
    print("=" * 60)
    print(f"\nArchivo: {archivo}")
    print("\nNOTA: Esta es una prueba. Se te pedirá confirmación antes de aplicar cambios.")
    print("=" * 60)
    
    # Simular input del usuario
    import builtins
    original_input = builtins.input
    
    def mock_input(prompt):
        if "Nombre del archivo Excel" in prompt:
            return str(archivo)
        else:
            return original_input(prompt)
    
    builtins.input = mock_input
    
    try:
        db_manager = get_db_manager()
        with db_manager.get_session() as session:
            importar_tarifas_excel(session)
    finally:
        builtins.input = original_input
