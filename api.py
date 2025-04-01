from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from agente_credito import avaliar_credito

app = FastAPI()

# Modelo genérico com campos dinâmicos
class Entrada(BaseModel):
    dados: Dict[str, Any]
    observacoes: str = ""

@app.post("/avaliar")
def avaliar(entrada: Entrada):
    cliente = entrada.dados
    observacoes = entrada.observacoes

    resultado = avaliar_credito(cliente, observacoes)
    return {
        "cliente": cliente.get("nome", "N/A"),
        "resultado": resultado
    }
