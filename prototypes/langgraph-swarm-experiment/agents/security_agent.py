# Security Agent

from agents.base_agent import BaseAgent


class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="security_agent", role="Security Monitor")

    def run(self, state: dict) -> dict:
        print(f"[{self.name}] Checking for anomalies...")
        # TODO: Implement security logic
        return {
            "messages": [f"{self.name}: No anomalies detected."],
            "current_agent": self.name
        }

    def decide_handoff(self, state: dict) -> str:
        return "end"