from fastapi import FastAPI
import gradio as gr
from fastapi.middleware.cors import CORSMiddleware
from gradio.routes import mount_gradio_app
from agente_credito import avaliar_credito

app = FastAPI(title="Agentic AI - Crédito")

# Libera CORS (opcional, bom pra conectar com frontend no futuro)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função de avaliação
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

# Interface Gradio
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

# Monta Gradio na rota /interface
mount_gradio_app(app, interface, path="/interface")
