import google.generativeai as genai
from config import GOOGLE_API_KEY
import json

genai.configure(api_key=GOOGLE_API_KEY)

def aplicar_regras(score, renda, valor):
    if score > 800:
        limite = renda * 0.4
    elif 700 <= score <= 800:
        limite = renda * 0.35
    elif 600 <= score < 700:
        limite = renda * 0.25
    else:
        return "reprovado", 0

    if valor <= limite:
        return "aprovado", limite
    else:
        return "parcial", limite

def modelo_preditivo(score, renda, valor, contrato):
    risco = 0

    if score < 600:
        risco += 2
    elif score < 700:
        risco += 1

    if renda < 3000:
        risco += 1

    if valor > 10000:
        risco += 1

    if contrato != "CLT":
        risco += 1

    if risco <= 1:
        return "baixo risco"
    elif risco == 2:
        return "médio risco"
    else:
        return "alto risco"

def avaliar_credito(cliente: dict, observacoes: str = "", instrucoes: str = ""):
    model = genai.GenerativeModel('gemini-1.5-pro')

    # 🧠 Extrai e garante os dados básicos
    nome = cliente.get("nome", "Não informado")
    score = cliente.get("score", 0)
    renda = cliente.get("renda", 0)
    valor = cliente.get("valor_solicitado", 0)
    contrato = cliente.get("contrato", "Não informado")

    # ✅ Aplica as regras e modelo preditivo
    regra, limite = aplicar_regras(score, renda, valor)
    risco = modelo_preditivo(score, renda, valor, contrato)

    # 💡 Calcula comprometimento da renda
    comprometimento = (valor / renda) * 100 if renda else 0

    # 🧾 Monta o prompt completo com instruções customizadas
    prompt = (
        f"Análise técnica:\n"
        f"- Resultado das regras: {regra} (limite de R$ {limite:.2f})\n"
        f"- Classificação do modelo preditivo: {risco}\n"
        f"- Comprometimento da renda: {comprometimento:.2f}%\n"
        f"- Observações adicionais: {observacoes}\n\n"
        f"Dados recebidos:\n{json.dumps(cliente, indent=2, ensure_ascii=False)}\n\n"
        f"Instruções para o analista IA: {instrucoes}\n\n"
        f"Com base nisso, forneça uma análise clara, profissional e personalizada para o cliente."
    )

    resposta = model.generate_content(prompt)
    return resposta.text
