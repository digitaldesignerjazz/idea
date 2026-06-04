# Context Aggregator Agent - Summarizes swarm activity

from agents.base_agent import BaseAgent


class ContextAggregator(BaseAgent):
    def __init__(self):
        super().__init__(name="context_aggregator", role="Context Aggregator")

    def run(self, state: dict) -> dict:
        print(f"[{self.name}] Aggregating swarm context and insights...")
        
        blackboard = state.get("blackboard", {})
        messages = state.get("messages", [])
        
        events = blackboard.get("recent_events", [])
        
        # Create a summary of recent activity
        if events:
            summary = f"Processed {len(events)} recent events. " \
                      f"Key activities: {', '.join(events[-2:])}"
        else:
            summary = "No significant events recorded yet."
        
        blackboard["context_summary"] = summary
        blackboard["last_aggregation"] = summary
        
        new_messages = messages + [f"{self.name}: {summary}"]
        
        return {
            "messages": new_messages,
            "blackboard": blackboard,
            "current_agent": self.name
        }