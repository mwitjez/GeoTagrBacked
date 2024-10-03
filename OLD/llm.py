from langchain.llms.openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools import WikipediaQueryRun, GoogleSearchResults


if __name__ == "__main__":
    llm = ChatOpenAI(
        temperature=0.0, base_url="http://localhost:1234/v1", api_key="not-needed"
    )
    tools = [WikipediaQueryRun, GoogleSearchResults]
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Your taks is to find a precise location of a given photo. Give a name of a country and a city.",
            ),
            ("user", "Where this photo was taken?"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    llm_with_tools = llm.bind_tools(tools)
    
