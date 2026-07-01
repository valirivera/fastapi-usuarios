from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional

class TareaBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Nombre de la tarea")
    descripcion: Optional[str] = Field(None, max_length=200)
    fecha_vencimiento: date

class TareaCreate(TareaBase):
    pass

class TareaUpdate(TareaBase):
    responsable: str
    estado: str
    

class TareaResponse(TareaBase):
    id: int
    responsable: str

    model_config = ConfigDict(from_attributes=True)