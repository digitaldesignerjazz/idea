# LangGraph Swarm Experiment - Phase 1 (Enhanced)
# Features: Dynamic handoff, shared blackboard, basic mesh simulation

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
    workflow = StateGraph(SwarmState)

    monitor = NetworkMonitor()
    optimizer = Optimizer()
    security = SecurityAgent()

    workflow.add_node("network_monitor", monitor.run)
    workflow.add_node("optimizer", optimizer.run)
    workflow.add_node("security_agent", security.run)

    def decide_next_agent(state: SwarmState) -> Literal["optimizer", "security_agent", "end"]:
        conditions = state.get("mesh_conditions", {})
        blackboard = state.get("blackboard", {})

        # Expanded handoff logic with multiple conditions
        if conditions.get("security_alert", False):
            return "security_agent"
        
        # High latency or packet loss triggers optimizer
        if (conditions.get("latency", 0) > 80 or 
            conditions.get("packet_loss", 0) > 5 or
            blackboard.get("optimization_needed", False)):
            return "optimizer"
        
        # If recent security issue was found
        if blackboard.get("last_security_check") and "anomaly" in str(blackboard.get("last_security_check", "")).lower():
            return "security_agent"
        
        return "end"

    workflow.add_conditional_edges(
        "network_monitor",
        decide_next_agent,
        {
            "optimizer": "optimizer",
            "security_agent": "security_agent",
            "end": END
        }
    )

    workflow.add_edge("optimizer", END)
    workflow.add_edge("security_agent", END)

    workflow.set_entry_point("network_monitor")
    return workflow.compile()


def run_enhanced_example():
    print("=== Enhanced LangGraph Swarm Experiment ===\n")
    
    app = create_swarm_graph()
    
    # More realistic initial conditions
    initial_state: SwarmState = {
        "messages": [],
        "blackboard": {
            "optimization_needed": False,
            "recent_events": []
        },
        "current_agent": "",
        "mesh_conditions": {
            "latency": 95,           # High -> should trigger optimizer
            "packet_loss": 3,
            "security_alert": False,
            "node_count": 12
        },
        "task_context": {"task": "maintain_mesh_health"},
        "handoff_history": []
    }
    
    result = app.invoke(initial_state)
    
    print("\n=== Execution Complete ===")
    print(f"Total messages: {len(result.get('messages', []))}")
    print(f"Final blackboard: {result.get('blackboard')}")
    print(f"Handoff history: {result.get('handoff_history', [])}")
    
    return result


if __name__ == "__main__":
    run_enhanced_example()