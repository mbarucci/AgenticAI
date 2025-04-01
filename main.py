from fastapi import FastAPI
from starlette.responses import HTMLResponse
import gradio as gr
from agente_credito import avaliar_credito

app = FastAPI()

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
    outputs=gr.Textbox(label="Resultado")
)

@app.get("/", response_class=HTMLResponse)
def gradio_ui():
    return interface.launch(prevent_thread_lock=True, inline=True)
