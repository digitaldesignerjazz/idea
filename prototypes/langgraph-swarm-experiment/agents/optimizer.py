# Optimizer Agent - Enhanced blackboard integration

from agents.base_agent import BaseAgent


class Optimizer(BaseAgent):
    def __init__(self):
        super().__init__(name="optimizer", role="Network Optimizer")

    def run(self, state: dict) -> dict:
        print(f"[{self.name}] Optimizing mesh routes...")
        
        blackboard = state.get("blackboard", {})
        messages = state.get("messages", [])
        conditions = state.get("mesh_conditions", {}).copy()
        
        # Read from blackboard what the monitor found
        last_analysis = blackboard.get("last_analysis", "No previous analysis")
        print(f"  -> Using monitor data: {last_analysis}")
        
        # Simulate intelligent optimization
        improvement = min(conditions.get("latency", 50) * 0.2, 25)
        new_latency = max(conditions.get("latency", 50) - improvement, 15)
        
        conditions["latency"] = round(new_latency)
        conditions["needs_optimization"] = False
        
        optimization_note = f"Reduced latency from {conditions.get('latency', 0) + improvement:.0f}ms to {new_latency}ms"
        
        blackboard["last_optimization"] = optimization_note
        
        # Log event
        events = blackboard.get("recent_events", [])
        events.append(f"Optimizer: {optimization_note}")
        blackboard["recent_events"] = events[-5:]
        
        new_messages = messages + [f"{self.name}: {optimization_note}"]
        
        return {
            "messages": new_messages,
            "blackboard": blackboard,
            "mesh_conditions": conditions,
            "current_agent": self.name
        }