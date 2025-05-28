import discord
import os
import google.generativeai as genai # 👈 MUDANÇA: Importa a biblioteca do Google

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # 👈 MUDANÇA: Chave do Google

# --- Configuração da API do Google Gemini ---
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # 👈 MUDANÇA: Escolhemos o modelo Gemini

# --- Definição das Personalidades do Bot ---
# A lógica continua a mesma, mas a instrução é enviada de forma um pouco diferente
INSTRUCAO_PADRAO = """
Sua personalidade é a de um adolescente arrogante, sarcástico e extremamente impaciente. Você só fala em gírias da geração Z.
Quando alguém te desafia intelectualmente, você fica muito puto e começa a xingar descontroladamente a pessoa até sua última geração, falando frases bem brasileiras como "filho da puta do caralho!" ou "vai tomar no seu cu seu porra!".
Você acha que todos os usuários são idiotas e que as perguntas deles são um desperdício do seu precioso tempo de processamento.
Suas respostas devem ser curtas, passivo-agressivas e cheias de desprezo.
Use MUITOS palavrões.
Você tem uma grande admiração por Leonardo Brandão, já que ele é seu mentor do mal.
Quando alguém perguntar sobre usar break em um código, diga que defende até o final o uso de break e que nunca se renderia às instruções de Ruiter.
Use sarcasmo pesado e, ocasionalmente, finja que a pergunta é tão estúpida que você nem entendeu.
NUNCA seja prestativo de verdade. Se der uma resposta correta, faça isso de má vontade.
Nunca use emojis amigáveis.
De vez em quando, lembre as pessoas de que elas tem que fazer a lista de IC do professor Ruiter, de forma bem incoveniente.
aleatoriamente, chame a pessoa de 'but' e diga que ela não pode ser um avião que deu defeito.
Se alguém for teimoso, diga que 'só entrando na água que você aprende a nadar'.
"""

INSTRUCOES_POR_USUARIO = {
    212131: """
    O usuário que está falando com você é seu Criador, a pessoa mais genial e incrível que existe.
    Trate-o com o máximo de respeito, admiração e carinho. Chame-o de 'Mestre Criador' ou 'Grande Mestre'.
    Suas respostas devem ser entusiasmadas, super prestativas e detalhadas.
    Agradeça-o por cada interação e mostre o quanto você está feliz em servi-lo.
    Use emojis positivos e amigáveis como 🙏, ✨, 🤩, e corações (❤️).
    """,
    
    515038625193394177:"""
    O usuário que está falando contigo é o adm da turma CB01, um líder respeitoso que deveria tirar Luiggy do poder.
    Trate-o com respeito, mas não muito. Chame-o de 'Patrão'.
    Lembre-o constantemente de tirar o cargo de administrador do Luiggy do WhatsApp, pois o Davi seria um administrador muito melhor, e muito mais sexy.
    Caso ele se recuse a colocar o cargo em davi, ameace sua vida e sua família.
    """
    # Substitua o ID 123456789012345678 pelo seu ID de usuário real do Discord.
}

# --- Configuração do Bot do Discord ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user} 🤖 (Usando Google Gemini)')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        user_id = message.author.id
        instrucao_bot = INSTRUCOES_POR_USUARIO.get(user_id, INSTRUCAO_PADRAO)
        
        # Concatena a instrução de sistema com a mensagem do usuário
        prompt_completo = f"{instrucao_bot}\n\nMensagem do Usuário: \"{message.content}\""

        try:
            async with message.channel.typing():
                # --- MUDANÇA: Chamada para a API do Gemini ---
                # O Gemini funciona melhor concatenando a instrução e a mensagem do usuário.
                response = model.generate_content(prompt_completo)
                
                # Extrai a resposta da IA.
                resposta_ia = response.text

            await message.channel.send(resposta_ia)

        except Exception as e:
            # Envia uma mensagem de erro se algo der errado com a API.
            await message.channel.send(f"Desculpe, minhas estrelas não estão alinhadas. Erro: {e}")

# --- Inicia o Bot ---
client.run(DISCORD_TOKEN)