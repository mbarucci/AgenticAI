from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import gradio as gr
from gradio.routes import mount_gradio_app
from agente_credito import avaliar_credito

# 🔧 Inicializa FastAPI
app = FastAPI(title="Agentic AI - Crédito", version="0.1.0")

# Libera CORS (útil se for integrar com outros frontends)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧠 Função chamada pela IA
def executar_avaliacao(nome, score, renda, valor, contrato, ocupacao, tempo, observacoes, instrucoes):
    cliente = {
        "nome": nome,
        "score": int(score),
        "renda": float(renda),
        "valor_solicitado": float(valor),
        "contrato": contrato,
        "ocupacao": ocupacao,
        "tempo_de_servico": tempo
    }
    return avaliar_credito(cliente, observacoes, instrucoes)

# 🧾 Interface visual (Gradio)
interface = gr.Interface(
    fn=executar_avaliacao,
    inputs=[
        gr.Textbox(label="Nome"),
        gr.Number(label="Score"),
        gr.Number(label="Renda mensal"),
        gr.Number(label="Valor solicitado"),
        gr.Dropdown(["CLT", "PJ", "Autônomo", "Aposentado"], label="Contrato"),
        gr.Textbox(label="Ocupação"),
        gr.Number(label="Tempo de serviço"),
        gr.Textbox(label="Observações"),
        gr.Textbox(label="Instruções para o agente", lines=4)
    ],
    outputs=gr.Textbox(label="Resultado da IA"),
    title="Análise de Crédito com IA",
    description="Informe os dados do cliente e as instruções desejadas para o agente de crédito"
)

# 🔗 Monta Gradio em /interface
mount_gradio_app(app, interface, path="/interface")

# 📬 Modelo para requisição API REST
class ClienteEntrada(BaseModel):
    dados: dict
    observacoes: str = ""
    instrucoes: str = ""

# 🚀 Endpoint REST: POST /avaliar
@app.post("/avaliar")
def avaliar(entrada: ClienteEntrada):
    resultado = avaliar_credito(entrada.dados, entrada.observacoes, entrada.instrucoes)
    return {
        "cliente": entrada.dados.get("nome", "Desconhecido"),
        "resultado": resultado
    }
