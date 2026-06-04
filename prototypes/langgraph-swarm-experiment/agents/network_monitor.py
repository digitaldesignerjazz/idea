# Network Monitor Agent

from agents.base_agent import BaseAgent


class NetworkMonitor(BaseAgent):
    def __init__(self):
        super().__init__(name="network_monitor", role="Network Monitor")

    def run(self, state: dict) -> dict:
        print(f"[{self.name}] Analyzing mesh conditions...")
        # TODO: Implement monitoring logic
        return {
            "messages": [f"{self.name}: Mesh looks stable."],
            "current_agent": self.name
        }

    def decide_handoff(self, state: dict) -> str:
        # Simple logic for now
        if state.get("mesh_conditions", {}).get("needs_optimization"):
            return "optimizer"
        return "end"