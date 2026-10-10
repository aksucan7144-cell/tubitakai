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

# Kullanıcı Girişi
if user_input := st.chat_input("Bilim insanlarına bir soru sor veya tartışma konusu at..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Yapay Zeka Karakterlerinin Sırayla ve Bağlamı Görerek Yanıt Vermesi
    for name, system_prompt in CHARACTERS.items():
        messages_payload = [
            {
                "role": "system", 
                "content": f"Sen {name}'sin. Karakter kuralların: {system_prompt}. Kesinlikle başka dillerde (Almanca vb.) konuşma. Tamamen Türkçe, net, doğal ve abartısız bir dille, diğer bilim insanlarının önceki yanıtlarını da dikkate alarak kendi alanına göre katkı sun."
            }
        ]
        
        # Geçmiş sohbetleri modele aktar
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                messages_payload.append({"role": "user", "content": msg["content"]})
            else:
                sender_name = msg.get("sender", "Biri")
                messages_payload.append({"role": "assistant", "content": f"[{sender_name}]: {msg['content']}"})

        try:
            response = client.chat.completions.create(
                messages=messages_payload,
                model="openai/gpt-oss-20b",
            )
            
            bot_reply = response.choices[0].message.content
            
            # Karakter yanıtını kaydet ve ekrana yazdır
            st.session_state.messages.append({"role": "assistant", "sender": name, "content": bot_reply})
            with st.chat_message("assistant"):
                st.write(f"**{name}**: {bot_reply}")
                
        except Exception as e:
            st.error(f"{name} yanıt verirken bir hata oluştu: {e}")
