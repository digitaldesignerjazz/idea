# Security Agent - Concrete implementation

from agents.base_agent import BaseAgent


class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="security_agent", role="Security Monitor")

    def run(self, state: dict) -> dict:
        print(f"[{self.name}] Scanning for security anomalies...")
        
        messages = state.get("messages", [])
        blackboard = state.get("blackboard", {})
        
        # Simulate security check
        security_result = "No anomalies detected. All nodes authenticated."
        
        new_messages = messages + [f"{self.name}: {security_result}"]
        blackboard["last_security_check"] = security_result
        
        return {
            "messages": new_messages,
            "blackboard": blackboard,
            "current_agent": self.name
        }

    def decide_handoff(self, state: dict) -> str:
        return "end"