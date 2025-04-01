import google.generativeai as genai
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

def avaliar_credito(cliente: dict):
    model = genai.GenerativeModel('gemini-1.5-pro')

    prompt = (
        "Você é um analista de crédito inteligente. "
        "Use as seguintes regras para avaliar a solicitação:\n"
        "- Score > 800: até 40% da renda\n"
        "- Score 700-800: até 35%\n"
        "- Score 600-700: até 25%\n"
        "- Score < 600: Reprovar\n\n"
        f"Cliente: {cliente['nome']}\n"
        f"Score: {cliente['score']}\n"
        f"Renda: R${cliente['renda']}\n"
        f"Valor solicitado: R${cliente['valor_solicitado']}\n"
        f"Contrato: {cliente['contrato']}"
    )

    resposta = model.generate_content(prompt)
    return resposta.text
