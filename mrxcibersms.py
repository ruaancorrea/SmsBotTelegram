import telebot
import requests

# SISTEMA DE ENVIO DE SMS USANDO API INTEGRADO E CONSTRUIDO JUNTO AO UM BOT NO TELEGRAM

CHAVE_API = "sua chave do telegrambot"

bot = telebot.TeleBot(CHAVE_API)

# Exclui o webhook antes de usar o método getUpdates
requests.get(f"https://api.telegram.org/bot{CHAVE_API}/deleteWebhook")

@bot.message_handler(commands=["sms"])
def senha(mensagem):
    bot.reply_to(mensagem, 'Por favor, digite senha padrão do boot:')
    bot.register_next_step_handler(mensagem, obter_senha)

def obter_senha(mensagem):
    senha_digitada = mensagem.text

    if senha_digitada == "2602":
        bot.reply_to(mensagem, 'Senha correta! Acesso concedido.')
        # Continue o código aqui após a senha estar correta
        # Exemplo:
        sms(mensagem)
    else:
        bot.reply_to(mensagem, 'Senha incorreta! Acesso negado.')

def sms(mensagem):
    bot.reply_to(mensagem, 'Vamos enviar uma mensagem SMS!')
    bot.reply_to(mensagem, 'Por favor, digite sua chave adquirida com @mrxciber:')

    # Capturar a resposta do usuário para a chave
    bot.register_next_step_handler(mensagem, obter_chave)

def obter_chave(mensagem):
    key = mensagem.text
    bot.reply_to(mensagem, 'Digite o remetente Ex: CLARO,CHICO:')
    bot.register_next_step_handler(mensagem, obter_remetente, key)

def obter_remetente(mensagem, key):
    rem = mensagem.text
    bot.reply_to(mensagem, 'Digite o número com +55:')
    bot.register_next_step_handler(mensagem, obter_numero, key, rem)

def obter_numero(mensagem, key, rem):
    nub = mensagem.text
    bot.reply_to(mensagem, 'Digite a mensagem:')
    bot.register_next_step_handler(mensagem, enviar_sms, key, rem, nub)

def enviar_sms(mensagem, key, rem, nub):
  mesg = mensagem.text

  try:
      response = requests.post(
          "https://gatewayapi.com/rest/mtsms",
          auth=(key, ''),
          data={
              'sender': rem,
              'message': mesg,
              'recipients.0.msisdn': nub
          }
      )
      response.raise_for_status()  # Verificar se houve erro na resposta

      if response.status_code == 200:
        bot.reply_to(mensagem,'Mensagem SMS enviada com sucesso!')
      else:
        bot.reply_to(mensagem,'Erro ao enviar a mensagem SMS.')

  except requests.exceptions.RequestException as e:
       bot.reply_to(mensagem,'Erro ao enviar a mensagem SMS.')



@bot.message_handler(commands=["chave"])
def chave(mensagem):
    bot.send_message(mensagem.chat.id, "Adquira sua chave no privado do @MRXCIBER")


def verificar(mensagem):
  
  return True

@bot.message_handler(func=verificar)
def responder(mensagem):
  texto = """
Escolha uma opção para continuar (Clique no item):
  /sms Enviar sms
  /chave Adquirir sua chave para envio de sms
Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
  bot.reply_to(mensagem, texto)

bot.polling()
