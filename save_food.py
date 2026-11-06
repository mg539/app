import streamlit as st
import unicodedata

# ==============================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================
st.set_page_config(
    page_title="Save Food",
    page_icon="🍎",
    layout="wide"
)

# ==============================================
# ARMAZENAMENTO DAS INFORMAÇÕES NA SESSÃO
# ==============================================
if "produtos" not in st.session_state:
    st.session_state.produtos = []

if "pedidos" not in st.session_state:
    st.session_state.pedidos = []


# ==============================================
# FUNÇÃO PARA NORMALIZAR TEXTOS DE PESQUISA
# Remove acentos e facilita pesquisas com maiúsculas,
# minúsculas e palavras no plural.
# ==============================================
def normalizar_texto(texto):
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caractere for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )
    return texto


def preparar_pesquisa(texto):
    texto = normalizar_texto(texto)

    # Exemplo: "BANANAS" passa a ser "banana".
    if len(texto) > 3 and texto.endswith("s"):
        texto = texto[:-1]

    return texto


# ==============================================
# FUNÇÃO PARA ESCOLHER O EMOJI DO ALIMENTO
# ==============================================
def escolher_imagem(nome):
    nome = normalizar_texto(nome)

    alimentos = {
        "pizza": "🍕",
        "hamburguer": "🍔",
        "arroz": "🍚",
        "feijao": "🫘",
        "pao": "🍞",
        "bolo": "🍰",
        "leite": "🥛",
        "banana": "🍌",
        "maca": "🍎",
        "laranja": "🍊",
        "uva": "🍇",
        "morango": "🍓",
        "melancia": "🍉",
        "cenoura": "🥕",
        "tomate": "🍅",
        "batata": "🥔",
        "queijo": "🧀",
        "ovo": "🥚",
        "frango": "🍗",
        "carne": "🥩",
        "peixe": "🐟",
        "sanduiche": "🥪",
        "salada": "🥗",
        "sorvete": "🍦",
        "cafe": "☕",
        "suco": "🧃",
        "biscoito": "🍪",
        "abacaxi": "🍍",
        "manga": "🥭",
        "coco": "🥥",
        "milho": "🌽",
        "pimentao": "🫑",
        "brocolis": "🥦",
        "cogumelo": "🍄",
        "cereja": "🍒",
        "pera": "🍐",
        "limao": "🍋",
        "kiwi": "🥝",
        "amendoim": "🥜",
        "castanha": "🌰",
        "camarao": "🍤",
        "macarrao": "🍝",
        "pipoca": "🍿",
        "panqueca": "🥞",
        "mel": "🍯",
        "batata frita": "🍟",
        "taco": "🌮",
        "sushi": "🍣",
        "pudim": "🍮"
    }

    return alimentos.get(nome, "🍽️")


# ==============================================
# FUNÇÃO PARA CALCULAR O PREÇO COM DESCONTO
# ==============================================
def calcular_preco(preco, desconto):
    return preco - (preco * desconto / 100)


# ==============================================
# FUNÇÃO PARA CADASTRAR ALIMENTOS
# ==============================================
def cadastrar_alimento(nome, estabelecimento, preco, desconto, quantidade):
    nome = nome.strip()
    estabelecimento = estabelecimento.strip()

    if not nome or not estabelecimento:
        return False, "Preencha todos os campos de texto!"

    if preco <= 0:
        return False, "O preço deve ser maior que zero!"

    if quantidade <= 0:
        return False, "A quantidade deve ser maior que zero!"

    if desconto < 0 or desconto > 50:
        return False, "O desconto deve estar entre 0% e 50%!"

    if any(
        p["nome"].lower() == nome.lower()
        and p["estabelecimento"].lower() == estabelecimento.lower()
        for p in st.session_state.produtos
    ):
        return False, "Esse alimento já está cadastrado nesse estabelecimento!"

    produto = {
        "nome": nome,
        "imagem": escolher_imagem(nome),
        "estabelecimento": estabelecimento,
        "preco": preco,
        "desconto": desconto,
        "preco_final": calcular_preco(preco, desconto),
        "quantidade": quantidade
    }

    st.session_state.produtos.append(produto)
    return True, "Alimento cadastrado com sucesso!"


# ==============================================
# CABEÇALHO COM EMOJI ANIMADO
# O ícone alterna entre vários alimentos.
# ==============================================
st.markdown(
    """
    <style>
    .savefood-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 4px;
    }

    .savefood-title {
        font-size: 2.7rem;
        font-weight: 750;
        line-height: 1.2;
    }

    .food-animation {
        position: relative;
        display: inline-block;
        width: 66px;
        height: 66px;
        font-size: 3.1rem;
        line-height: 66px;
        text-align: center;
        vertical-align: middle;
    }

    .food-animation span {
        position: absolute;
        inset: 0;
        opacity: 0;
        animation: food-change 6s infinite;
    }

    .food-animation span:nth-child(1) { animation-delay: 0s; }
    .food-animation span:nth-child(2) { animation-delay: 1s; }
    .food-animation span:nth-child(3) { animation-delay: 2s; }
    .food-animation span:nth-child(4) { animation-delay: 3s; }
    .food-animation span:nth-child(5) { animation-delay: 4s; }
    .food-animation span:nth-child(6) { animation-delay: 5s; }

    @keyframes food-change {
        0%   { opacity: 0; transform: scale(0.75) rotate(-12deg); }
        8%   { opacity: 1; transform: scale(1.08) rotate(0deg); }
        16%  { opacity: 1; transform: scale(1) rotate(0deg); }
        20%  { opacity: 0; transform: scale(0.85) rotate(12deg); }
        100% { opacity: 0; }
    }

    @media (prefers-reduced-motion: reduce) {
        .food-animation span { animation: none; }
        .food-animation span:first-child { opacity: 1; }
    }
    </style>

    <div class="savefood-header">
        <div class="food-animation" aria-label="Alimentos">
            <span>🍎</span>
            <span>🍌</span>
            <span>🍕</span>
            <span>🥕</span>
            <span>🍓</span>
            <span>🥑</span>
        </div>
        <div class="savefood-title">Save Food</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("Economize alimentos, combata o desperdício!")
st.write(
    "Encontre alimentos com descontos de até 50% "
    "e ajude a reduzir o desperdício."
)
st.divider()


# ==============================================
# ABAS DO APLICATIVO
# ==============================================
aba1, aba2, aba3 = st.tabs([
    "📦 Cadastrar alimentos",
    "🛒 Ofertas disponíveis",
    "📋 Meus pedidos"
])


# ==============================================
# ABA 1 - CADASTRO
# ==============================================
with aba1:
    st.header("Cadastrar novo alimento")

    with st.form("formulario_cadastro"):
        nome = st.text_input("Nome do alimento")
        estabelecimento = st.text_input("Nome do estabelecimento")

        preco = st.number_input(
            "Preço original (R$)",
            min_value=0.01,
            value=10.0,
            step=0.50
        )

        desconto = st.slider(
            "Desconto (%)",
            min_value=0,
            max_value=50,
            value=10
        )

        quantidade = st.number_input(
            "Quantidade disponível",
            min_value=1,
            value=1,
            step=1
        )

        enviar = st.form_submit_button("Cadastrar alimento")

        if enviar:
            sucesso, mensagem = cadastrar_alimento(
                nome,
                estabelecimento,
                preco,
                desconto,
                quantidade
            )

            if sucesso:
                st.success(mensagem)
            else:
                st.error(mensagem)


# ==============================================
# ABA 2 - OFERTAS E PESQUISA
# ==============================================
with aba2:
    st.header("Alimentos disponíveis")

    pesquisa = st.text_input(
        "🔎 Pesquisar alimento ou estabelecimento",
        placeholder="Ex.: banana, bananas, padaria..."
    )

    termo = preparar_pesquisa(pesquisa)

    ofertas = []
    for produto in st.session_state.produtos:
        nome_normalizado = normalizar_texto(produto["nome"])
        estabelecimento_normalizado = normalizar_texto(
            produto["estabelecimento"]
        )

        nome_pesquisavel = preparar_pesquisa(produto["nome"])
        estabelecimento_pesquisavel = preparar_pesquisa(
            produto["estabelecimento"]
        )

        corresponde = (
            not termo
            or termo in nome_normalizado
            or termo in estabelecimento_normalizado
            or termo in nome_pesquisavel
            or termo in estabelecimento_pesquisavel
        )

        if produto["quantidade"] > 0 and corresponde:
            ofertas.append(produto)

    if ofertas:
        for produto in ofertas:
            with st.container(border=True):
                st.subheader(
                    f'{produto["imagem"]} {produto["nome"]}'
                )

                st.write(
                    "Estabelecimento: " + produto["estabelecimento"]
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Preço original",
                    f'R$ {produto["preco"]:.2f}'
                )

                col2.metric(
                    "Preço promocional",
                    f'R$ {produto["preco_final"]:.2f}'
                )

                col3.metric(
                    "Desconto",
                    f'{produto["desconto"]}%'
                )

                st.caption(
                    f'Quantidade disponível: {produto["quantidade"]}'
                )

    elif not st.session_state.produtos:
        st.info(
            "Ainda não há alimentos cadastrados. "
            "Acesse a aba 'Cadastrar alimentos' para adicionar a primeira oferta."
        )

    else:
        st.info(
            "Nenhum alimento disponível corresponde à sua pesquisa. "
            "Confira a escrita ou tente pesquisar no singular, por exemplo: banana."
        )


# ==============================================
# ABA 3 - PEDIDOS E HISTÓRICO
# ==============================================
with aba3:
    st.header("Realizar pedido")

    produtos_disponiveis = [
        p for p in st.session_state.produtos
        if p["quantidade"] > 0
    ]

    if produtos_disponiveis:
        nomes = [p["nome"] for p in produtos_disponiveis]

        with st.form("formulario_pedido"):
            alimento_escolhido = st.selectbox(
                "Escolha um alimento",
                nomes,
                format_func=lambda nome: f"{escolher_imagem(nome)} {nome}"
            )

            quantidade_pedido = st.number_input(
                "Quantidade desejada",
                min_value=1,
                value=1,
                step=1
            )

            confirmar = st.form_submit_button("Confirmar pedido")

            if confirmar:
                produto = next(
                    p for p in produtos_disponiveis
                    if p["nome"] == alimento_escolhido
                )

                if quantidade_pedido <= produto["quantidade"]:
                    total = produto["preco_final"] * quantidade_pedido
                    produto["quantidade"] -= quantidade_pedido

                    st.session_state.pedidos.append({
                        "alimento": produto["nome"],
                        "imagem": produto["imagem"],
                        "quantidade": quantidade_pedido,
                        "total": total
                    })

                    st.success("Pedido realizado com sucesso!")
                    st.write(
                        f'Alimento: {produto["imagem"]} {produto["nome"]}'
                    )
                    st.write(f"Quantidade: {quantidade_pedido}")
                    st.write(f"Valor total: R$ {total:.2f}")

                else:
                    st.error(
                        "Quantidade maior que o estoque disponível!"
                    )
    else:
        st.info("Não existem alimentos disponíveis para pedidos.")

    st.divider()
    st.subheader("Histórico de pedidos")

    if st.session_state.pedidos:
        for pedido in st.session_state.pedidos:
            st.write(
                f'{pedido["imagem"]} {pedido["alimento"]} | '
                f'Quantidade: {pedido["quantidade"]} | '
                f'Total: R$ {pedido["total"]:.2f}'
            )
    else:
        st.write("Você ainda não realizou pedidos.")
