from decouple import config as env_config
import re
from csv_loader import read_csv_file
from prompt import SYSTEM_PROMPT
from rag import create_retriever

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

OPENAI_API_KEY = env_config("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-5.5", temperature=0, api_key=env_config("OPENAI_API_KEY"))

retriever = create_retriever()


@tool
def get_categories() -> list[dict]:
    """
    Retrieves all product categories available on csv company's records database.

    Use this tool when you need to:
    - List all registered product categories.
    - Identify available product categories.
    - Retrieve category IDs and names.
    - Answer questions about the company's product categorization.

    Returns:
        A list of dictionaries containing the category records,
        including their respective IDs and names.
    """
    categories_df = read_csv_file("desafio_tecnico_ai_eng - categories.csv")
    return categories_df


@tool
def get_customers() -> list[dict]:
    """
    Retrieves all customer records from the CSV database.

    Use this tool when you need to:
    - List all registered customers.
    - Identify available customers.
    - Retrieve customer IDs and names.
    - Answer questions about the company's customer base.

    Returns:
        A list of dictionaries containing the customer records,
        including their respective IDs and names.
    """
    customers_df = read_csv_file("desafio_tecnico_ai_eng - customers.csv")
    return customers_df


@tool
def get_order_items() -> list[dict]:
    """
    Retrieves all order item records from the CSV database.

    Use this tool when you need to:
    - List all registered order items.
    - Identify available order items.
    - Retrieve order item IDs and names.
    - Answer questions about the company's order items.

    Returns:
        A list of dictionaries containing the order item records,
        including their respective IDs and names.
    """
    order_items_df = read_csv_file("desafio_tecnico_ai_eng - order_items.csv")
    return order_items_df


@tool
def get_orders() -> list[dict]:
    """
    Retrieves all orders records from the CSV database.

    Use this tool when you need to:
    - List all registered orders.
    - Identify available orders.
    - Retrieve order IDs and names.
    - Answer questions about the company's orders.

    Returns:
        A list of dictionaries containing the order records,
        including their respective IDs and names.
    """
    orders_df = read_csv_file("desafio_tecnico_ai_eng - orders.csv")
    return orders_df


@tool
def get_products() -> list[dict]:
    """
    Retrieves all product records from the CSV database.

    Use this tool when you need to:
    - List all registered products.
    - Identify available products.
    - Retrieve product IDs and names.
    - Answer questions about the company's products.

    Returns:
        A list of dictionaries containing the product records,
        including their respective IDs and names.
    """
    products_df = read_csv_file("desafio_tecnico_ai_eng - products.csv")
    return products_df


@tool
def get_promotions() -> list[dict]:
    """
    Retrieves all promotion records from the CSV database.

    Use this tool when you need to:
    - List all registered promotions.
    - Identify available promotions.
    - Retrieve promotion IDs and names.
    - Answer questions about the company's promotions.

    Returns:
        A list of dictionaries containing the promotion records,
        including their respective IDs and names.
    """
    promotions_df = read_csv_file("desafio_tecnico_ai_eng - promotions.csv")
    return promotions_df


@tool
def get_policies(query: str) -> str:
    """
    Retrieves all policies records from the pdf políticas_da_loja.pdf.

    Use this tool when you need to:
    - List all registered policies.
    - Identify available policies.
    - Answer questions about the company's policies.
    """

    documents = retriever.invoke(query)
    if not documents:
        return "Essa informacão não foi encontrada nas políticas da loja."
    context = "\n\n".join(document.page_content for document in documents)
    return context


tools = [
    get_categories,
    get_customers,
    get_order_items,
    get_orders,
    get_products,
    get_promotions,
    get_policies,
]


checkpointer = InMemorySaver()

agent = create_agent(
    model=llm, tools=tools, system_prompt=SYSTEM_PROMPT, checkpointer=checkpointer
)

agent_config = {"configurable": {"thread_id": "conversation_001"}}


def remove_markdown(text: str) -> str:
    # Remove negrito e itálico
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)

    # Remove títulos
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)

    # Remove crases de código
    text = re.sub(r"`{1,3}", "", text)

    return text


def chat(user_input: str) -> str:
    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]}, config=agent_config
    )

    assistant_response = response["messages"][-1].content
    assistant_response = remove_markdown(assistant_response)
    return assistant_response


print("Empório da Música!\n Como posso ajudá-lo?\n")
print("\nDigite 'sair' para encerrar.\n")

while True:

    user_input = input("Você: ").strip()

    if user_input.lower() == "sair":
        print("Agente encerrado!")
        break

    if not user_input:
        continue

    try:
        response = chat(user_input)
        print(f"\nAssistente: {response}\n")

    except Exception as error:
        print(f"Erro: {error}")
