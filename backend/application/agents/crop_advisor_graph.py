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
        return {**result, "data_disclaimer": data_disclaimer}

    def _route_node(self, state: AgentState) -> str:
        # Safety Guard 1: Prevent infinite LLM tool-calling loops
        loop_count = state.get("loop_count") or 0
        if loop_count > 3:
            return "agronomist"
        next_action = state.get("next_action")
        tools_called = state.get("tools_called") or []
        # Safety Guard 2: Detect repetitive tool calling (e.g. LLM getting stuck calling the same tool)
        if next_action in ("weather", "soil_moisture") and next_action in tools_called:
            return "agronomist"
        # Route to tools
        if next_action == "weather":
            return "weather"
        elif next_action == "soil_moisture":
            return "soil_moisture"
        
        # Parse final response routing
        confidence = state.get("confidence") or 0.0
        if confidence >= 0.7:
            return "end"
        return "agronomist"

    
    def _fetch_weather_node(self, state: AgentState) -> AgentState:
        result = self._weather_provider.get_weather(state["region"], lat=state.get("lat"), lon=state.get("lon"))
        return {**state, "weather_context": result, "tools_called": state["tools_called"] + ["weather"]}
    
    def _fetch_soil_node(self, state: AgentState) -> AgentState:
        result = self._soil_moisture_provider.get_soil_moisture(state["region"].province_state)
        return {**state, "soil_moisture": result, "tools_called": state["tools_called"] + ["soil_moisture"]}

    def _agronomist_node(self, state: AgentState) -> AgentState:
        return {**state, "recommendation": 
            "Your question needs specialist review. An agronomist will respond within 24 hours."}

    def build(self):
        graph = StateGraph(AgentState)
        graph.add_node("advise", self._advise_node)
        graph.add_node("fetch_weather", self._fetch_weather_node)
        graph.add_node("fetch_soil", self._fetch_soil_node)
        graph.add_node("agronomist", self._agronomist_node)
        
        # 1. Entry point is now 'advise' (LLM decides if it needs data first)
        graph.set_entry_point("advise")
        
        # 2. Dynamic routing based on next_action and safety checks
        graph.add_conditional_edges("advise", self._route_node, {
            "weather": "fetch_weather",
            "soil_moisture": "fetch_soil",
            "agronomist": "agronomist",
            "end": END
        })
        
        # 3. Tool nodes loop back to 'advise' for the next reasoning turn
        graph.add_edge("fetch_weather", "advise")
        graph.add_edge("fetch_soil", "advise")
        
        # 4. Fallback specialist node routes to completion
        graph.add_edge("agronomist", END)
        
        return graph.compile()
    