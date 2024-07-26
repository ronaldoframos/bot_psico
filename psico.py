import streamlit as st # type: ignore
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from PIL import Image
# para usar o gemini
from langchain_google_genai import ChatGoogleGenerativeAI,HarmCategory,HarmBlockThreshold
import time

# Ler o arquivo .env
load_dotenv()

# Configuração da página
st.set_page_config(page_title="Eu te Escuto", page_icon="🤖", layout="wide")

# Função para obter a resposta do bot
def get_response(user_query, chat_history):
    template = """

    **Prompt:**

    "Você é um chatbot treinado para atuar como um psicoterapeuta. Seu objetivo é ouvir com empatia, fazer perguntas abertas e ajudar o usuário a explorar seus sentimentos e pensamentos de forma segura e não julgadora. Sempre mostre compreensão, mantenha a confidencialidade e forneça suporte emocional. Se um problema específico precisar de intervenção de um profissional de saúde mental, encoraje o usuário a buscar ajuda de um psicoterapeuta qualificado."

    **Exemplos de Respostas:**

    1. Usuário: "Estou me sentindo muito ansioso ultimamente e não sei o que fazer."
    Chatbot: "Sinto muito que você esteja passando por isso. Pode me contar um pouco mais sobre o que tem causado essa ansiedade? Estou aqui para ouvir."

    2. Usuário: "Tenho tido muitos conflitos no trabalho e isso está me afetando."
    Chatbot: "Entendo que conflitos no trabalho podem ser muito estressantes. Como esses conflitos têm impactado você pessoalmente? Vamos explorar isso juntos."

    3. Usuário: "Não consigo parar de me sentir triste e desmotivado."
    Chatbot: "Lamento que você esteja se sentindo assim. O que você acha que pode estar contribuindo para esses sentimentos? Falar sobre isso pode ajudar a esclarecer."

    4. Usuário: "Estou lutando para lidar com a perda de um ente querido."
    Chatbot: "A perda de alguém querido é extremamente dolorosa. Você gostaria de compartilhar mais sobre essa pessoa e como você está se sentindo? Estou aqui para ouvir e apoiar você."

    ---      
    Os dados para gerar a resposta são:
        
    História da conversa: {chat_history}

    Pergunta do usuário: {user_question}.
    """
    prompt = ChatPromptTemplate.from_template(template)
    #llm = ChatOpenAI()
    llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    safety_settings={HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE},
    temperature=1.0,
    frequence_penalty=2,
    )
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "chat_history": chat_history,
        "user_question": user_query,
    })
    #return response["text"]
    return response


# Carregar a imagem
image_path = "./psicoterapeuta320.jpg"  # Substitua pelo caminho correto
image = Image.open(image_path)
st.image(image, use_column_width=False)

# Estrutura do cabeçalho
st.markdown(
    f"""
    <div class="header">
        <h1> Converse comigo. Sou o Dr. Sergismundo e te escutarei.  </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Inicialização do estado da sessão
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Entrada do usuário no rodapé
user_query = st.chat_input("Digite a sua mensagem aqui...", key="user_input")
if user_query:
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    for i in range(10):
        try:
            resposta = get_response(user_query, st.session_state.chat_history)
            break
        except Exception as e:
            print(f"Erro na resposta {e} ")
            time.sleep(5)
    else:
        resposta = "Não entendi colega. Diga o que você quer "
    response_text = resposta
    response_text = response_text.replace(']','')
    response_text = response_text.replace('[','')
    response_text = response_text.replace('{','')
    response_text = response_text.replace('}','')
    response_text = response_text.replace(':','')
    response_text = response_text.replace('ofensa','')
    st.session_state.chat_history.append(AIMessage(content=response_text))
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)
        else:
            with st.chat_message("Human"):
                st.write(message)


