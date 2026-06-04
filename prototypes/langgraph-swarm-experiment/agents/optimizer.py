# Optimizer Agent - Concrete implementation

from agents.base_agent import BaseAgent


class Optimizer(BaseAgent):
    def __init__(self):
        super().__init__(name="optimizer", role="Network Optimizer")

    def run(self, state: dict) -> dict:
        print(f"[{self.name}] Running optimization on mesh routes...")
        
        messages = state.get("messages", [])
        blackboard = state.get("blackboard", {})
        
        # Simulate optimization work
        optimization_result = "Applied route optimization: reduced average latency by ~15%"
        
        new_messages = messages + [f"{self.name}: {optimization_result}"]
        blackboard["last_optimization"] = optimization_result
        
        # Update mesh conditions to reflect improvement
        conditions = state.get("mesh_conditions", {}).copy()
        conditions["needs_optimization"] = False
        conditions["latency"] = max(conditions.get("latency", 50) - 10, 20)
        
        return {
            "messages": new_messages,
            "blackboard": blackboard,
            "mesh_conditions": conditions,
            "current_agent": self.name
        }

    def decide_handoff(self, state: dict) -> str:
        return "end"