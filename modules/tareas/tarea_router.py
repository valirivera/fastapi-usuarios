from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from modules.tareas.tarea_schema import TareaCreate, TareaResponse, TareaUpdate
from modules.tareas.tarea_service import TareaService

router = APIRouter(prefix="/tareas", tags=["Tareas"])

@router.get("/", response_model=list[TareaResponse], status_code=status.HTTP_200_OK)
async def read_tareas(db: AsyncSession = Depends(get_db)):
    service = TareaService(db)
    return await service.get_all_tareas()

@router.get("/get_by_name", response_model=list[TareaResponse], status_code=status.HTTP_200_OK)
async def read_tareas_by_name(nombre: str, db: AsyncSession = Depends(get_db)):
    service = TareaService(db)
    return await service.get_tarea_by_name(nombre)

@router.post("/", response_model=TareaResponse, status_code=status.HTTP_201_CREATED)
async def add_tarea(tarea_in: TareaCreate, db: AsyncSession = Depends(get_db)):
    service = TareaService(db)
    return await service.create_tarea(tarea_in)

@router.put("/", response_model=TareaResponse, status_code=status.HTTP_200_OK)
async def update_tarea(tarea_in: TareaUpdate, db: AsyncSession = Depends(get_db)):
    service = TareaService(db)
    return await service.update_tarea(tarea_in)

@router.delete("/", response_model=dict, status_code=status.HTTP_200_OK)
async def dele_tarea_by_id(id:int, db: AsyncSession = Depends(get_db)):
    service = TareaService(db)
    return await service.delete_tarea_by_id(id)