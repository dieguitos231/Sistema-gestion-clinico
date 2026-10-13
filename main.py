from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel
from typing import List

#Inicialización de la aplicacion FastAPI
app=FastAPI(
    title="API Gestion Clinica y Citas medicas",
    description="API RESTful completa con operaciones CRUD para auditoria de servicios web",
    version="1.0.0"
)

#Modelo de Datos con Pydantic para validacion automatica
class Paciente(BaseModel):
    id:int
    documento_identidad:str
    nombre_completo:str
    eps:str
    edad:int =0

#Modelo Auxiliar para la actualizacion parcial o total
class PacienteUpdate(BaseModel):
    documento_identidad:str
    nombre_completo:str
    eps:str
    edad:int 

# Base de datos simulada en memoria

db_pacientes:List[Paciente]=[
    Paciente(id=1,documento_identidad="10226328",nombre_completo="Luisa Alejandra Morales Ruiz",eps="Nueva Eps",edad=24),
    Paciente(id=2,documento_identidad="80342834",nombre_completo="Ana Marcela Nuñez Mora",eps="Famisanar",edad=18)
]


#--------------------------------------------------------
# ENDPOINTS / RUTAS DE LA API
#--------------------------------------------------------

# 1. READ ALL (Obtener todos los pacientes)

@app.get("/api/v1/pacientes",response_model=List[Paciente],status_code=status.HTTP_200_OK)
def obtener_todos_los_pacientes():
    return db_pacientes

# 2. READ ONE (Obtener un paciente por su ID especifico)

@app.get("/api/v1/paciente/{id}",response_model=Paciente,status_code=status.HTTP_200_OK)
def buscar_paciente_por_id(id:int):
    for paciente in  db_pacientes:
        if paciente.id == id :
            return paciente
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El paciente con ID {id} no existe en el sistema clinico."
    )

#  3.CREATE (Registrar un nuevo paciente)
@app.post("/api/v1/paciente",response_model=Paciente,status_code=status.HTTP_201_CREATED)
def crear_nuevo_paciente(paciente : Paciente):
    #Validar si el ID ya existe
    for p in db_pacientes:
        if p.id == paciente.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error de registro: Ya existe un paciente con el ID {paciente.id}"
            )
    db_pacientes.append(paciente)
    return paciente

# 4.UPDATE (Actualizar un paciente existente)

@app.put("/api/v1/paciente/{id}",response_model=PacienteUpdate,status_code=status.HTTP_200_OK)
def actualizar_libro(id:int,datos_actualizados:PacienteUpdate):
    for index,paciente in  enumerate(db_pacientes):
        if paciente.id == id:
            pacienteModificado=Paciente(
                id=id,
                documento_identidad=datos_actualizados.documento_identidad,
                nombre_completo=datos_actualizados.nombre_completo,
                eps=datos_actualizados.eps,
                edad=datos_actualizados.edad
            )
            db_pacientes[index]=pacienteModificado
            return pacienteModificado
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible actualizar. El paciente con ID {id} no fue encontrado"
    )

#  5.DELETE (Eliminar un paciente de la clinica)
@app.delete("/api/v1/paciente/{id}",status_code=status.HTTP_200_OK)
def eliminar_paciente(id : int):
    for index,paciente in enumerate(db_pacientes):
        if paciente.id == id:
            db_pacientes.pop(index)
            return {"mensaje": f"El paciente con ID {id} fue eliminado exitosamente"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible eliminar.El paciente con ID {id} no existe."
    )