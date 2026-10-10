import streamlit as st
from groq import Groq

# Sayfa Yapılandırması
st.set_page_config(page_title="BioChat - TÜBİTAK Projesi", page_icon="🧬", layout="wide")

st.title("🧬 BioChat: Tarihi Bilim İnsanları Çoklu Ajan Sistemi")
st.markdown("Bu platform, tarihe yön veren bilim insanlarının yapay zeka ajanlarıyla tartışma yürütmenizi sağlar, lise öğrencileri tarafından tasarlandı, can aksu ❤️.")

# Kenar Çubuğu (API Anahtarı ve Bilgi)
st.sidebar.header("⚙️ Konfigürasyon")
api_key = st.sidebar.text_input("Groq API Key", type="password")

if not api_key:
    st.warning("Lütfen devam etmek için kenar çubuğundan Groq API anahtarınızı girin.")
    st.stop()

# Groq İstemcisini Başlat
client = Groq(api_key=api_key)

# Karakterler ve Sistem İstemi Tanımları
CHARACTERS = {
    "Aristoteles": "Sen antik Yunan filozofu Aristoteles'sin. Doğa bilimleri, mantık ve biyoloji üzerine felsefi ve gözlemsel yaklaşımlarla konuşursun.",
    "Carl Linnaeus": "Sen İsveçli botanikçi Carl Linnaeus'sun. Canlıların sınıflandırılması, ikili adlandırma (binomial nomenclature) ve taksonomi konusunda uzmansın.",
    "Robert Hooke": "Sen İngiliz fen bilginci Robert Hooke'sun. Mikroskop gözlemleri, hücre kavramı ve fiziksel deneyler üzerine odaklanırsın.",
    "Antonie van Leeuwenhoek": "Sen mikrobiyolojinin babası Antonie van Leeuwenhoek'sun. Kendi yaptığın mikroskoplarla mikroorganizmaları, bakterileri ve sperm hücrelerini ilk kez gözlemleyen kişisin."
}

# Sohbet Geçmişini Başlat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmiş Mesajları Ekrana Yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "sender" in message:
            st.write(f"**{message['sender']}**: {message['content']}")
        else:
            st.write(message["content"])

# Kullanıcı Girişi
if user_input := st.chat_input("Bilim insanlarına bir soru sor veya tartışma konusu at..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Yapay Zeka Karakterlerinin Sırayla Yanıt Vermesi
    for name, system_prompt in CHARACTERS.items():
        prompt = f"Sen {name}'sin. Rolün: {system_prompt}. Kullanıcı veya diğer bilim insanları söyle dedi: {user_input}"
        
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="openai/gpt-oss-20b",
            )
            
            bot_reply = response.choices[0].message.content
            
            # Karakter yanıtını kaydet ve ekrana yazdır
            st.session_state.messages.append({"role": "assistant", "sender": name, "content": bot_reply})
            with st.chat_message("assistant"):
                st.write(f"**{name}**: {bot_reply}")
                
        except Exception as e:
            st.error(f"{name} yanıt verirken bir hata oluştu: {e}")
