# Network Monitor Agent - Concrete implementation

from agents.base_agent import BaseAgent


class NetworkMonitor(BaseAgent):
    def __init__(self):
        super().__init__(name="network_monitor", role="Network Monitor")

    def run(self, state: dict) -> dict:
        print(f"[{self.name}] Analyzing current mesh conditions...")
        
        conditions = state.get("mesh_conditions", {})
        messages = state.get("messages", [])
        
        # Simulate monitoring logic
        analysis = f"Mesh status: latency={conditions.get('latency', 'N/A')}ms, " \
                   f"packet_loss={conditions.get('packet_loss', 'N/A')}%"
        
        new_messages = messages + [f"{self.name}: {analysis}"]
        
        # Update blackboard with observations
        blackboard = state.get("blackboard", {})
        blackboard["last_monitoring"] = analysis
        
        return {
            "messages": new_messages,
            "blackboard": blackboard,
            "current_agent": self.name
        }

    def decide_handoff(self, state: dict) -> str:
        conditions = state.get("mesh_conditions", {})
        if conditions.get("needs_optimization"):
            return "optimizer"
        elif conditions.get("security_alert"):
            return "security_agent"
        return "end"