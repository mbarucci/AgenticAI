import gradio as gr
from agente_credito import avaliar_credito

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

with gr.Blocks(title="Análise de Crédito Corporativa") as demo:
    gr.Markdown("# 🧠 Análise de Crédito com IA\nAutomação inteligente com parametrização de agente.")
    
    with gr.Group():
        gr.Markdown("## 📋 Dados do Cliente")

        with gr.Row():
            nome = gr.Textbox(label="Nome", placeholder="Ex: João Silva")
            score = gr.Number(label="Score")

        with gr.Row():
            renda = gr.Number(label="Renda Mensal (R$)")
            valor = gr.Number(label="Valor Solicitado (R$)")

        contrato = gr.Dropdown(["CLT", "PJ", "Autônomo", "Aposentado"], label="Tipo de Contrato", value="CLT")
        ocupacao = gr.Textbox(label="Ocupação", placeholder="Ex: Engenheiro Civil")
        tempo = gr.Number(label="Tempo de Serviço (anos)", value=0)

        observacoes = gr.Textbox(label="Observações adicionais", lines=3, placeholder="Ex: Possui imóvel quitado, bom relacionamento com o banco")

    with gr.Group():
        gr.Markdown("## ⚙️ Parâmetros do Agente")
        instrucoes = gr.Textbox(
            label="Instruções para o Agente de Crédito",
            placeholder="Ex: Seja empático, explique em linguagem simples, ofereça alternativa caso reprovado...",
            lines=4
        )

    with gr.Group():
        gr.Markdown("## 📊 Resultado")
        resultado = gr.Textbox(label="Resposta do Agente", lines=10)

    botao = gr.Button("🚀 Avaliar Crédito")

    botao.click(fn=executar_avaliacao,
                inputs=[nome, score, renda, valor, contrato, ocupacao, tempo, observacoes, instrucoes],
                outputs=[resultado])

if __name__ == "__main__":
    demo.launch()
