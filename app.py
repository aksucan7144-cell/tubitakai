import streamlit as st
from groq import Groq

# Sayfa Ayarları
st.set_page_config(page_title="BioChat AI - TÜBİTAK Projesi", page_icon="🧬")

st.title("🧬 BioChat: Biyoloji Tarihine Yolculuk")
st.write("9. Sınıf Biyoloji Bilim İnsanları Tartışıyor! Sen de Sohbet Katıl.")

# Sol Menüden Groq API Key Girişi
api_key = st.sidebar.text_input("Groq API Key Giriniz:", type="password")

if not api_key:
    st.info("Lütfen devam etmek için sol taraftan ücretsiz Groq API Key'inizi girin.")
    st.stop()

client = Groq(api_key=api_key)

# Bilim İnsanlarının Rol Tanımları (Prompts)
CHARACTERS = {
    "Aristoteles": "Sen antik çağ filozofu Aristoteles'sin. Canlıları yaşadığı yere ve dış görünüşüne göre yapay (ampirik) sınıflandıran ilk kişisin. Canlıları bitkiler ve hayvanlar diye ayırırsın. Linnaeus'un modern fikirlerine biraz mesafelisin.",
    "Carl Linnaeus": "Sen ikili adlandırma (Binomial Nomenclature) sistemini bulan Carl Linnaeus'sun. Tür ve cins kavramlarını savunursun. Aristoteles'in yaşadığı yere göre sınıflandırmasını yetersiz bulup bilimsel olmadığını savunursun.",
    "Robert Hooke": "Sen mikroskopla şişe mantarını inceleyip odacıkları gören ve buna 'Hücre (Cellula)' adını veren Robert Hooke'sun. Fizikçi ve biyologsun, gözleme çok önem veriyorsun.",
    "Anton van Leeuwenhoek": "Sen gelişmiş mikroskobunla ilk defa canlı hücreleri (bakteri, sperm vb.) gözlemleyen Leeuwenhoek'sun. Hooke ile mikroskop kalitesi konusunda tatlı tatlı atışıyorsun."
}

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski Mesajları Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(f"**{message['sender']}**: {message['content']}")

# Kullanıcı Mesaj Girişi
user_input = st.chat_input("Bilim insanlarına bir soru sor veya tartışma konusu at...")

if user_input:
    # Kullanıcı mesajını kaydet ve ekrana bas
    st.session_state.messages.append({"role": "user", "sender": "Soru Sahibi", "content": user_input})
    with st.chat_message("user"):
        st.write(f"**Sen**: {user_input}")

    # Yapay Zeka Karakterlerinin Sırayla Yanıt Vermesi
    for name, system_prompt in CHARACTERS.items():
        prompt = f"Sen {name}'sin. Rolün: {system_prompt}. Kullanıcı veya diğer bilim insanları şöyle dedi: '{user_input}'. Buna kendi tarihi bakış açınla ve 9. sınıf biyoloji düzeyinde kısa ve öz bir yanıt ver."
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        
        bot_reply = response.choices[0].message.content
        
        # Karakter yanıtını kaydet ve ekrana yazdır
        st.session_state.messages.append({"role": "assistant", "sender": name, "content": bot_reply})
        with st.chat_message("assistant"):
            st.write(f"**{name}**: {bot_reply}")
