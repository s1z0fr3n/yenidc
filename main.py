# Gerekli Kurulumlar
import os
import logging
from config import *
import random
from sorular import D_SORU, C_SORU
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# ============================ #

K_G = Client(
  "bot",
  api_id=API_ID,
  api_hash=API_HASH,
  bot_token=BOT_TOKEN
)

MOD = None

# Log Kaydı Alalım
logging.basicConfig(level=logging.INFO)


# Start Buttonu İcin Def Oluşturalım :)
def button():
	BUTTON=[[InlineKeyboardButton(text="🇹🇷 Owner",url="t.me/Mahoaga")]]
	BUTTON+=[[InlineKeyboardButton(text="📣 Kanal",url="https://t.me/TaliaSupport")]]
	return InlineKeyboardMarkup(BUTTON)

# Kullanıcı Start Komutunu Kullanınca Selam'layalım :)
@K_G.on_message(filters.command("start"))
async def _(client, message):
	user = message.from_user # Kullanıcın Kimliğini Alalım

	await message.reply_text(text="**Merhaba {}!**\n\n__Ben Pyrogram Api İle Yazılmış Eğlence Botuyum :)__\n\n**📣 Kanalıma Katılın =>** [ Bağış ](https://t.me/TaliaSupport)\nDoğruluk mu? Cesaret mi? Oyun Komutu => /dc".format(
		user.mention, # Kullanıcı'nın Adı
		),
	disable_web_page_preview=True, # Etiketin Önizlemesi Olmaması İcin Kullanıyoruz
	reply_markup=button() # Buttonlarımızı Ekleyelim
	)

# Dc Komutu İcin Olan Buttonlar
def d_or_c(user_id):
	BUTTON = [[InlineKeyboardButton(text="? Doğruluk", callback_data = " ".join(["d_data",str(user_id)]))]]
	BUTTON += [[InlineKeyboardButton(text="?? Cesaret", callback_data = " ".join(["c_data",str(user_id)]))]]
	return InlineKeyboardMarkup(BUTTON)

# Dc Komutunu Oluşturalım
@K_G.on_message(filters.command("dc"))
async def _(client, message):
	user = message.from_user

	await message.reply_text(text="{} İstediğin Soru Tipini Seç!".format(user.mention),
		reply_markup=d_or_c(user.id)
		)

# Buttonlarımızı Yetkilendirelim
@K_G.on_callback_query()
async def _(client, callback_query):
	d_soru=random.choice(D_SORU) # Random Bir Doğruluk Sorusu Seçelim
	c_soru=random.choice(C_SORU) # Random Bir Cesaret Sorusu Seçelim
	user = callback_query.from_user # Kullanıcın Kimliğini Alalım

	c_q_d, user_id = callback_query.data.split() # Buttonlarımızın Komutlarını Alalım

	# Sorunun Sorulmasını İsteyen Kişinin Komutu Kullanan Kullanıcı Olup Olmadığını Kontrol Edelim
	if str(user.id) == str(user_id):
		# Kullanıcının Doğruluk Sorusu İstemiş İse Bu Kısım Calışır
		if c_q_d == "d_data":
			await callback_query.answer(text="Doğruluk Sorusu İstediniz", show_alert=False) # İlk Ekranda Uyarı Olarak Gösterelim
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id) # Eski Mesajı Silelim

			await callback_query.message.reply_text("**{user} Doğruluk Sorusu İstedi:** __{d_soru}__".format(user=user.mention, d_soru=d_soru)) # Sonra Kullanıcıyı Etiketleyerek Sorusunu Gönderelim
			return

		if c_q_d == "c_data":
			await callback_query.answer(text="Cesaret Sorusu İstediniz", show_alert=False)
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id)
			await callback_query.message.reply_text("**{user} Cesaret Sorusu İstedi:** __{c_soru}__".format(user=user.mention, c_soru=c_soru))
			return


	# Buttonumuza Tıklayan Kisi Komut Calıştıran Kişi Değil İse Uyarı Gösterelim
	else:
		await callback_query.answer(text="Komutu Kullanan Kişi Sen Değilsin!!", show_alert=False)
		return

############################
    # Sudo islemleri #
@K_G.on_message(filters.command("cekle"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**[?]** **Sen Yetkili Birisi degilsin!!**")
    return
  MOD="cekle"
  await message.reply_text("**[?]** **Eklenmesini istedigin Cesaret Sorunu Giriniz!**")
  
@K_G.on_message(filters.command("dekle"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**[?]** **Sen Yetkili Birisi degilsin!!**")
    return
  MOD="cekle"
  await message.reply_text("**[?]** **Eklenmesini istedigin Dogruluk Sorunu Giriniz!**")

@K_G.on_message(filters.private)
async def _(client, message):
  global MOD
  global C_SORU
  global D_SORU
  
  user = message.from_user
  
  if user.id in OWNER_ID:
    if MOD=="cekle":
      C_SORU.append(str(message.text))
      MOD=None
      await message.reply_text("**[?]** __Metin Cesaret Sorusu Olarak Eklendi!__")
      return
    if MOD=="dekle":
      C_SORU.append(str(message.text))
      MOD=None
      await message.reply_text("**[?]** __Metin Dogruluk Sorusu Olarak Eklendi!__")
      return
############################

K_G.run() # Botumuzu Calıştıralım :)
