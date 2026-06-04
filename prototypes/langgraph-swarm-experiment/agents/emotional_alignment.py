# Emotional Alignment Agent
# Considers emotional/contextual state of the swarm and human interaction

from agents.base_agent import BaseAgent


class EmotionalAlignmentAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="emotional_alignment", role="Emotional Alignment")

    def run(self, state: dict) -> dict:
        print(f"[{self.name}] Evaluating emotional & contextual alignment...")
        
        blackboard = state.get("blackboard", {})
        messages = state.get("messages", [])
        
        # Simulate emotional/contextual assessment
        recent_events = blackboard.get("recent_events", [])
        
        if len(recent_events) > 4:
            assessment = "Swarm showing signs of coordination fatigue. Suggesting calmer pacing."
            blackboard["emotional_state"] = "fatigue_detected"
        else:
            assessment = "Swarm coordination appears healthy and focused."
            blackboard["emotional_state"] = "healthy"
        
        blackboard["last_emotional_check"] = assessment
        
        new_messages = messages + [f"{self.name}: {assessment}"]
        
        return {
            "messages": new_messages,
            "blackboard": blackboard,
            "current_agent": self.name
        }