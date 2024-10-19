import io

import PIL
from IPython.display import Image, display
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from src.response_format import Location
from src.tools import ToolsContainer


class Agent:
    def __init__(self, image = None):
        self.model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, timeout=None, max_retries=5, retry_delay=2.0)
        tc = ToolsContainer(image)
        self.tools = tc.get_tools()

    def _should_continue(self, state: MessagesState):
        messages = state['messages']
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return "end"

    def _call_model(self, state: MessagesState):
        messages = state['messages']
        model_with_tools = self.model.bind_tools(self.tools)
        try:
            response = model_with_tools.invoke(messages)
        except Exception as e:
            response = AIMessage(content=f"Error: {str(e)}")
        return {"messages": [response]}

    def _get_final_coordinates(self, state: MessagesState):
        messages = state['messages']
        messages.append(HumanMessage(content="Given previous messages generate a location from the image (latitude, longitude) and reasoning why you picked this location. If you think you don't have enough information, just guess the location."))
        structured_model = self.model.with_structured_output(Location)
        response = structured_model.invoke(messages)
        return {"messages": [str(response.model_dump_json())]}

    def create_graph(self):
        workflow = StateGraph(MessagesState)
        tool_node = ToolNode(self.tools)

        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", tool_node)
        workflow.add_node("final_location", self._get_final_coordinates)

        workflow.add_edge(START, "agent")
        workflow.add_edge("tools", 'agent')
        workflow.add_conditional_edges("agent", self._should_continue, {"tools": "tools", "end": "final_location"})
        workflow.add_edge("final_location", END)

        graph = workflow.compile()
        return graph

    def viz_graph(self, ipynb=False):
        if ipynb:
            display(Image(self.create_graph().get_graph().draw_mermaid_png())) 
        else:
            img = Image(self.create_graph().get_graph().draw_mermaid_png())
            pimg = PIL.Image.open(io.BytesIO(img.data))
            pimg.show()
