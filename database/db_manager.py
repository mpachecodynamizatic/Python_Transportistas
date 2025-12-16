"""
Gestor de la base de datos SQLite
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from pathlib import Path
import os

from models.models import Base


class DatabaseManager:
    """Gestiona la conexión y operaciones de la base de datos"""
    
    def __init__(self, db_path: str = None):
        """
        Inicializa el gestor de base de datos
        
        Args:
            db_path: Ruta al archivo de base de datos. Si es None, usa 'transportistas.db'
        """
        if db_path is None:
            # Usar la carpeta raíz del proyecto
            project_root = Path(__file__).parent.parent
            db_path = project_root / "transportistas.db"
        
        self.db_path = str(db_path)
        self.engine = create_engine(f'sqlite:///{self.db_path}', echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
    
    def create_tables(self):
        """Crea todas las tablas en la base de datos"""
        Base.metadata.create_all(bind=self.engine)
        print(f"✓ Base de datos creada: {self.db_path}")
    
    def drop_tables(self):
        """Elimina todas las tablas de la base de datos"""
        Base.metadata.drop_all(bind=self.engine)
        print(f"✓ Tablas eliminadas")
    
    def reset_database(self):
        """Elimina y recrea todas las tablas"""
        self.drop_tables()
        self.create_tables()
        print(f"✓ Base de datos reiniciada")
    
    @contextmanager
    def get_session(self) -> Session:
        """
        Proporciona una sesión de base de datos con manejo automático de transacciones
        
        Uso:
            with db_manager.get_session() as session:
                # Operaciones con la sesión
                session.add(objeto)
                session.commit()
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_new_session(self) -> Session:
        """Crea y retorna una nueva sesión (debe cerrarse manualmente)"""
        return self.SessionLocal()


# Instancia global del gestor de base de datos
_db_manager = None


def get_db_manager(db_path: str = None) -> DatabaseManager:
    """
    Obtiene la instancia global del gestor de base de datos
    
    Args:
        db_path: Ruta a la base de datos (solo se usa en la primera llamada)
    
    Returns:
        DatabaseManager: Instancia del gestor
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager(db_path)
    return _db_manager


def get_session() -> Session:
    """
    Función de conveniencia para obtener una nueva sesión
    
    Returns:
        Session: Nueva sesión de base de datos
    """
    return get_db_manager().get_new_session()
