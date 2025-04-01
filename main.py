from agente_credito import avaliar_credito

cliente = {
    "nome": "João Silva",
    "score": 720,
    "renda": 5000,
    "valor_solicitado": 15000,
    "contrato": "CLT"
}

resposta = avaliar_credito(cliente)
print("\n💬 Resposta da IA:\n")
print(resposta)
