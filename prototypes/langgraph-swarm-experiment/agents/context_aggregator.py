# Context Aggregator Agent

from agents.base_agent import BaseAgent


class ContextAggregator(BaseAgent):
    def __init__(self):
        super().__init__(name="context_aggregator", role="Context Aggregator")

    def run(self, state: dict) -> dict:
        print(f"[{self.name}] Aggregating swarm activity...")
        
        blackboard = state.get("blackboard", {})
        messages = state.get("messages", [])
        
        events = blackboard.get("recent_events", [])
        iteration = state.get("iteration_count", 0)
        
        summary = f"Round {iteration}: Processed {len(events)} events."
        
        if events:
            summary += f" Recent: {events[-1]}"
        
        blackboard["context_summary"] = summary
        
        new_messages = messages + [f"{self.name}: {summary}"]
        
        return {
            "messages": new_messages,
            "blackboard": blackboard,
            "current_agent": self.name
        }