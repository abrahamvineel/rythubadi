from application.agents.crop_advisor_agent import AgentState, advise
from langgraph.graph import StateGraph, END
from application.ports.i_llm_client import ILLMClient
from application.ports.i_weather_provider import IWeatherProvider
from application.ports.i_soil_moisture_provider import ISoilMoistureProvider
from application.localisation.disclaimers import get_disclaimer

class CropAdvisorGraph:

    def __init__(self, 
                 llm_client: ILLMClient, 
                 weather_provider: IWeatherProvider, 
                 soil_moisture_provider: ISoilMoistureProvider):
        self._llm_client = llm_client
        self._weather_provider = weather_provider
        self._soil_moisture_provider = soil_moisture_provider

    def _advise_node(self, state: AgentState) -> AgentState:
        result = advise(state, self._llm_client)
        weather_context = result["weather_context"]
        data_disclaimer = "Data precision level unknown"
        if weather_context:
            data_disclaimer = get_disclaimer(weather_context.precision_level, result["language"])
        return {**result, "confidence": 0.9, "data_disclaimer": data_disclaimer}

    def _route_node(self, state: AgentState) -> str:
        if state["confidence"] >= 0.7:
            return "end"
        return "agronomist"
    
    def _fetch_weather_node(self, state: AgentState) -> AgentState:
        result = self._weather_provider.get_weather(state["region"], lat=state.get("lat"), lon=state.get("lon"))
        return {**state, "weather_context": result, "tools_called": state["tools_called"] + ["weather"]}
    
    def _fetch_soil_node(self, state: AgentState) -> AgentState:
        result = self._soil_moisture_provider.get_soil_moisture(state["region"].province_state)
        return {**state, "soil_moisture": result, "tools_called": state["tools_called"] + ["soil_moisture"]}

    def build(self):
        graph = StateGraph(AgentState)
        graph.add_node("advise", self._advise_node)
        graph.add_node("fetch_weather", self._fetch_weather_node)
        graph.add_node("fetch_soil", self._fetch_soil_node)
        graph.set_entry_point("fetch_weather")
        graph.add_edge("fetch_weather", "fetch_soil")
        graph.add_edge("fetch_soil", "advise")
        graph.add_conditional_edges("advise", self._route_node, {"end": END, "agronomist": END})
        return graph.compile()
    