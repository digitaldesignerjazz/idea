# Network Monitor Agent - Enhanced with blackboard usage

from agents.base_agent import BaseAgent


class NetworkMonitor(BaseAgent):
    def __init__(self):
        super().__init__(name="network_monitor", role="Network Monitor")

    def run(self, state: dict) -> dict:
        print(f"[{self.name}] Analyzing mesh conditions...")
        
        conditions = state.get("mesh_conditions", {})
        blackboard = state.get("blackboard", {})
        messages = state.get("messages", [])
        
        # Analyze conditions
        latency = conditions.get("latency", 0)
        packet_loss = conditions.get("packet_loss", 0)
        
        analysis = f"Latency: {latency}ms, Packet Loss: {packet_loss}%"
        
        # Decide if optimization is needed and write to blackboard
        needs_optimization = latency > 70 or packet_loss > 4
        blackboard["optimization_needed"] = needs_optimization
        blackboard["last_analysis"] = analysis
        
        # Record event
        events = blackboard.get("recent_events", [])
        events.append(f"Monitor: {analysis}")
        blackboard["recent_events"] = events[-5:]  # Keep last 5
        
        new_messages = messages + [f"{self.name}: {analysis}"]
        
        return {
            "messages": new_messages,
            "blackboard": blackboard,
            "current_agent": self.name
        }