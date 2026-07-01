from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from modules.tareas.tarea_schema import TareaCreate, TareaUpdate
from core.logger import logger

class TareaService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all_tareas(self) -> list[dict]:
        logger.info("SQL Nativo: Consultando todos las tareas.")
        query = text("SELECT tareas.id, tareas.name, tareas.descripcion, tareas.fecha_vencimiento, users.username, users.id, tareas.estado FROM tareas INNER JOIN users ON tareas.responsable=users.id;")
        result = await self.db.execute(query)
        return [dict(row) for row in result.mappings().all()]
    
    async def get_tarea_by_name(self, el_nombre: str) -> list[dict]:
        logger.info("SQL Nativo: Consultar un tarea por su nombre")
        query = text("SELECT tareas.id, tareas.name, tareas.descripcion, tareas.fecha_vencimiento, users.username, tareas.estado FROM tareas INNER JOIN users ON tareas.responsable=users.id WHERE name LIKE :nombre")
        el_nombre = f"%{el_nombre}%"
        result = await self.db.execute(query, {"nombre": el_nombre})
        return [dict(row) for row in result.mappings().all()]

    async def create_tarea(self, tarea_data: TareaCreate) -> dict:
        logger.info(f"SQL Nativo: Insertando rol {tarea_data.name}")
        
        check = await self.db.execute(text("SELECT id FROM tareas WHERE name = :name;"), {"name": tarea_data.name})
        if check.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La tarea ya existe.")

        query = text("INSERT INTO tareas (name, descripcion, fecha_vencimiento, estado) VALUES (:name, :descripcion, :fecha_vencimiento, 'Pendiente') RETURNING id, name, descripcion, fecha_vencimiento, estado;")
        try:
            result = await self.db.execute(query, {"name": tarea_data.name, "descripcion": tarea_data.descripcion, "fecha_vencimiento": tarea_data.fecha_vencimiento})
            await self.db.commit()
            return dict(result.mappings().first())
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error al insertar la tarea: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor.")

    async def delete_tarea_by_id(self, el_id:int) -> dict:
        logger.info("SQL Nativo: Consultar un id con su número.")
        query_check = text ("SELECT id FROM tareas WHERE id = :identificacion")
        check = await self.db.execute(query_check, {"identificacion": el_id})
        if not check.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tarea no existente.")
        query=text("DELETE FROM tareas WHERE id = :identy")
        try:
            await self.db.execute(query,{"identy": el_id})
            await self.db.commit()
            return {"messange": f"Tarea {el_id} eliminado con exito."}
        
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error al eliminar la tarea: {str(e)}")
            
    async def update_tarea(self, tarea_data: TareaUpdate, el_id: int) -> dict:
        logger.info("SQL Nativo: Consultar un id con su número.")
        query_check = text ("SELECT id FROM tareas WHERE id = :identificacion")
        check = await self.db.execute(query_check, {"identificacion": el_id})
        if not check.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tarea no existente.")
        logger.info(f"SQL Nativo: Actualizando {tarea_data.name}")

        query = text("UPDATE tareas SET(responsable, estado) VALUES (:responsable, :estado) RETURNING id, name, descripcion, fecha_vencimiento, responsable, estado;")
        try:
            result = await self.db.execute(query, {"responsable": tarea_data.responsable, "estado": tarea_data.estado})
            await self.db.commit()
            return dict(result.mappings().first())
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error al actualizar la tarea: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor.")   