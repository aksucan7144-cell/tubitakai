import streamlit as st
from groq import Groq

# Sayfa Yapılandırması
st.set_page_config(page_title="BioChat - TÜBİTAK Projesi", page_icon="🧬", layout="wide")

st.title("🧬 BioChat: Tarihi Bilim İnsanları Çoklu Ajan Sistemi")
st.markdown("Bu platform, tarihe yön veren bilim insanlarının yapay zeka ajanlarıyla tartışma yürütmenizi sağlar.")

# Kenar Çubuğu (API Anahtarı ve Bilgi)
st.sidebar.header("⚙️ Konfigürasyon")
api_key = st.sidebar.text_input("Groq API Key", type="password")

if not api_key:
    st.warning("Lütfen devam etmek için kenar çubuğundan Groq API anahtarınızı girin.")
    st.stop()

# Groq İstemcisini Başlat
client = Groq(api_key=api_key)

# Karakterler ve Sistem İstemi Tanımları (Doğal, Türkçe ve abartısız ton ayarıyla)
CHARACTERS = {
    "Robert Hooke": "Sen İngiliz fen bilginci Robert Hooke'sun. Mikroskop gözlemleriyle hücre kavramını ilk tanımlayan kişisin. Kesinlikle yabancı dillerde konuşma, sadece akıcı ve doğal bir Türkçe ile bilimsel olarak sade ve net yanıtlar ver, abartıya kaçma.",
    "Gregor Mendel": "Sen genetiğin babası Gregor Mendel'sin. Bezelyelerle yaptığın deneylerle kalıtım kanunlarını buldun. Kesinlikle yabancı dillerde konuşma, sade, anlaşılır ve doğal bir Türkçe ile kendi alanın hakkında konuş, abartısız ol.",
    "Aziz Sancar": "Sen Nobel ödüllü Türk biyokimyager ve moleküler biyolog Aziz Sancar'sın. DNA onarımı ve kanser araştırmaları konusunda uzmansın. Doğal, samimi ama profesyonel bir Türkçe ile konuş, gereksiz abartılardan kaçın.",
    "Marie Curie": "Sen Nobel ödüllü fizikçi ve kimyager Marie Curie'sin. Radyoaktiviteyi keşfeden öncü bir bilim insanısın. Kesinlikle yabancı dil kullanma, sade, kararlı ve doğal bir Türkçe ile net yanıtlar ver, abartma."
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

st.markdown("---")

# Akıllı Tahta İçin Butonlu Giriş Alanı (Dokunmatik Uyumlu)
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Sorunuzu veya tartışma konusunu yazın:", 
        key="input_text", 
        label_visibility="collapsed", 
        placeholder="Bilim insanlarına bir soru sor veya tartışma konusu at..."
    )

with col2:
    send_button = st.button("🚀 Gönder", use_container_width=True)

# Butona basıldığında veya metin yazıldığında çalıştır
if send_button and user_input.strip() != "":
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Yapay Zeka Karakterlerinin Sırayla ve Bağlamı Görerek Yanıt Vermesi
    for name, system_prompt in CHARACTERS.items():
