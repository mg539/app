
import streamlit as st

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Save Food",
    page_icon="🍎",
    layout="wide"
)

# ARMAZENAMENTO DAS INFORMAÇÕES
if "produtos" not in st.session_state:
    st.session_state.produtos = []

if "pedidos" not in st.session_state:
    st.session_state.pedidos = []


# FUNÇÃO PARA CALCULAR O PREÇO COM DESCONTO
def calcular_preco(preco, desconto):
    return preco - (preco * desconto / 100)


# FUNÇÃO PARA CADASTRAR ALIMENTOS
def cadastrar_alimento(nome, estabelecimento, preco, desconto, quantidade):

    if not nome.strip() or not estabelecimento.strip():
        return False, "Preencha todos os campos de texto!"

    if preco <= 0:
        return False, "O preço deve ser maior que zero!"

    if quantidade <= 0:
        return False, "A quantidade deve ser maior que zero!"

    if any(p["nome"].lower() == nome.strip().lower()
           for p in st.session_state.produtos):
        return False, "Esse alimento já está cadastrado!"

    produto = {
        "nome": nome.strip(),
        "estabelecimento": estabelecimento.strip(),
        "preco": preco,
        "desconto": desconto,
        "preco_final": calcular_preco(preco, desconto),
        "quantidade": quantidade
    }

    st.session_state.produtos.append(produto)

    return True, "Alimento cadastrado com sucesso!"


# TÍTULO E DESCRIÇÃO
st.title("🍎 Save Food")
st.subheader("Economize alimentos, combata o desperdício!")

st.write(
    "Encontre alimentos com descontos de até 50% "
    "e ajude a reduzir o desperdício."
)

st.divider()


# ABAS DO APLICATIVO
aba1, aba2, aba3 = st.tabs([
    "📦 Cadastrar alimentos",
    "🛒 Ofertas disponíveis",
    "📋 Meus pedidos"
])


# ABA 1 - CADASTRO
with aba1:

    st.header("Cadastrar novo alimento")

    with st.form("formulario_cadastro"):

        nome = st.text_input("Nome do alimento")

        estabelecimento = st.text_input(
            "Nome do estabelecimento"
        )

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

        enviar = st.form_submit_button(
            "Cadastrar alimento"
        )

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


# ABA 2 - OFERTAS
with aba2:

    st.header("Alimentos disponíveis")

    pesquisa = st.text_input(
        "🔎 Pesquisar alimento ou estabelecimento"
    )

    ofertas = [
        p for p in st.session_state.produtos
        if p["quantidade"] > 0
        and (
            pesquisa.lower() in p["nome"].lower()
            or pesquisa.lower() in p["estabelecimento"].lower()
        )
    ]

    if ofertas:

        for produto in ofertas:

            with st.container(border=True):

                st.subheader("🍽️ " + produto["nome"])

                st.write(
                    "Estabelecimento: "
                    + produto["estabelecimento"]
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

    else:

        st.info("Nenhum alimento disponível encontrado.")


# ABA 3 - PEDIDOS
with aba3:

    st.header("Realizar pedido")

    produtos_disponiveis = [
        p for p in st.session_state.produtos
        if p["quantidade"] > 0
    ]

    if produtos_disponiveis:

        nomes = [
            p["nome"] for p in produtos_disponiveis
        ]

        with st.form("formulario_pedido"):

            alimento_escolhido = st.selectbox(
                "Escolha um alimento",
                nomes
            )

            quantidade_pedido = st.number_input(
                "Quantidade desejada",
                min_value=1,
                value=1,
                step=1
            )

            confirmar = st.form_submit_button(
                "Confirmar pedido"
            )

            if confirmar:

                produto = next(
                    p for p in produtos_disponiveis
                    if p["nome"] == alimento_escolhido
                )

                if quantidade_pedido <= produto["quantidade"]:

                    total = (
                        produto["preco_final"]
                        * quantidade_pedido
                    )

                    produto["quantidade"] -= quantidade_pedido

                    st.session_state.pedidos.append({
                        "alimento": produto["nome"],
                        "quantidade": quantidade_pedido,
                        "total": total
                    })

                    st.success("Pedido realizado com sucesso!")

                    st.write(f"Alimento: {produto['nome']}")
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
                f"🍎 {pedido['alimento']} | "
                f"Quantidade: {pedido['quantidade']} | "
                f"Total: R$ {pedido['total']:.2f}"
            )

    else:

        st.write("Você ainda não realizou pedidos.")

