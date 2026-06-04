# LangGraph Swarm Experiment - Phase 1
# Concrete starter implementation with dynamic handoffs and shared blackboard

from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END

from agents.network_monitor import NetworkMonitor
from agents.optimizer import Optimizer
from agents.security_agent import SecurityAgent
from state.shared_blackboard import SharedBlackboard


class SwarmState(TypedDict):
    messages: Annotated[list[str], lambda x, y: x + y]
    blackboard: dict
    current_agent: str
    mesh_conditions: dict
    task_context: dict
    handoff_history: list[str]


def create_swarm_graph():
    """Build the LangGraph for the agent swarm with conditional handoffs."""
    workflow = StateGraph(SwarmState)

    # Instantiate agents
    monitor = NetworkMonitor()
    optimizer = Optimizer()
    security = SecurityAgent()

    # Add nodes
    workflow.add_node("network_monitor", monitor.run)
    workflow.add_node("optimizer", optimizer.run)
    workflow.add_node("security_agent", security.run)

    # Conditional handoff logic
    def decide_next_agent(state: SwarmState) -> Literal["optimizer", "security_agent", "end"]:
        conditions = state.get("mesh_conditions", {})
        
        if conditions.get("needs_optimization", False):
            return "optimizer"
        elif conditions.get("security_alert", False):
            return "security_agent"
        else:
            return "end"

    # Add conditional edges from network_monitor
    workflow.add_conditional_edges(
        "network_monitor",
        decide_next_agent,
        {
            "optimizer": "optimizer",
            "security_agent": "security_agent",
            "end": END
        }
    )

    # Simple edges from other agents back to end for this minimal example
    workflow.add_edge("optimizer", END)
    workflow.add_edge("security_agent", END)

    # Set entry point
    workflow.set_entry_point("network_monitor")

    # Compile
    app = workflow.compile()
    return app


def run_example():
    """Run a simple example of the swarm."""
    print("=== LangGraph Swarm Experiment - Phase 1 ===\n")
    
    app = create_swarm_graph()
    
    # Initial state
    initial_state: SwarmState = {
        "messages": [],
        "blackboard": {},
        "current_agent": "",
        "mesh_conditions": {
            "needs_optimization": True,   # Trigger optimizer
            "security_alert": False,
            "latency": 45,
            "packet_loss": 2
        },
        "task_context": {"task": "optimize_mesh"},
        "handoff_history": []
    }
    
    # Run the graph
    result = app.invoke(initial_state)
    
    print("\n=== Final State ===")
    print(f"Messages: {result.get('messages', [])}")
    print(f"Final agent: {result.get('current_agent')}")
    print(f"Handoff history: {result.get('handoff_history', [])}")
    
    return result


if __name__ == "__main__":
    run_example()