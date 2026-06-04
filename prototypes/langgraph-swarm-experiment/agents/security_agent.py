# Security Agent - Enhanced with blackboard

from agents.base_agent import BaseAgent


class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="security_agent", role="Security Monitor")

    def run(self, state: dict) -> dict:
        print(f"[{self.name}] Performing security scan...")
        
        blackboard = state.get("blackboard", {})
        messages = state.get("messages", [])
        
        # Simulate security analysis
        issues_found = False  # Can be made dynamic later
        
        if issues_found:
            result = "Potential anomaly detected on node-07"
            blackboard["security_status"] = "warning"
        else:
            result = "All nodes healthy. No anomalies found."
            blackboard["security_status"] = "ok"
        
        blackboard["last_security_check"] = result
        
        events = blackboard.get("recent_events", [])
        events.append(f"Security: {result}")
        blackboard["recent_events"] = events[-5:]
        
        new_messages = messages + [f"{self.name}: {result}"]
        
        return {
            "messages": new_messages,
            "blackboard": blackboard,
            "current_agent": self.name
        }