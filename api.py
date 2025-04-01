from fastapi import FastAPI
from pydantic import BaseModel
from agente_credito import avaliar_credito

app = FastAPI()

# Modelo de entrada
class Cliente(BaseModel):
    nome: str
    score: int
    renda: float
    valor_solicitado: float
    contrato: str

@app.post("/avaliar")
def avaliar(cliente: Cliente):
    resultado = avaliar_credito(cliente.dict())
    return {
        "cliente": cliente.nome,
        "resultado": resultado
    }
