# LangGraph Swarm Experiment - With Persistence + Mesh Simulator

from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# Agents
from agents.network_monitor import NetworkMonitor
from agents.optimizer import Optimizer
from agents.security_agent import SecurityAgent
from agents.context_aggregator import ContextAggregator

# Simulator
from simulation.mesh_simulator import MeshSimulator


class SwarmState(TypedDict):
    messages: Annotated[list[str], lambda x, y: x + y]
    blackboard: dict
    current_agent: str
    mesh_conditions: dict
    task_context: dict
    handoff_history: list[str]
    thread_id: str   # For persistence


def create_swarm_graph(checkpointer=None):
    workflow = StateGraph(SwarmState)

    monitor = NetworkMonitor()
    optimizer = Optimizer()
    security = SecurityAgent()
    aggregator = ContextAggregator()

    workflow.add_node("network_monitor", monitor.run)
    workflow.add_node("optimizer", optimizer.run)
    workflow.add_node("security_agent", security.run)
    workflow.add_node("context_aggregator", aggregator.run)

    def decide_next_agent(state: SwarmState) -> str:
        conditions = state.get("mesh_conditions", {})
        blackboard = state.get("blackboard", {})

        if conditions.get("security_alert", False):
            return "security_agent"
        
        if (conditions.get("latency", 0) > 80 or 
            conditions.get("packet_loss", 0) > 5 or
            blackboard.get("optimization_needed", False)):
            return "optimizer"
        
        # Occasionally aggregate context
        if len(blackboard.get("recent_events", [])) >= 3:
            return "context_aggregator"
        
        return "end"

    workflow.add_conditional_edges(
        "network_monitor",
        decide_next_agent,
        {
            "optimizer": "optimizer",
            "security_agent": "security_agent",
            "context_aggregator": "context_aggregator",
            "end": END
        }
    )

    workflow.add_edge("optimizer", END)
    workflow.add_edge("security_agent", END)
    workflow.add_edge("context_aggregator", END)

    workflow.set_entry_point("network_monitor")
    
    if checkpointer:
        return workflow.compile(checkpointer=checkpointer)
    return workflow.compile()


def run_with_persistence():
    print("=== LangGraph Swarm with Persistence & Simulator ===\n")
    
    # Create checkpointer for persistence
    checkpointer = MemorySaver()
    
    app = create_swarm_graph(checkpointer=checkpointer)
    
    # Use thread_id for conversation/session persistence
    config = {"configurable": {"thread_id": "mesh-swarm-001"}}
    
    simulator = MeshSimulator()
    
    initial_state: SwarmState = {
        "messages": [],
        "blackboard": {
            "optimization_needed": False,
            "recent_events": []
        },
        "current_agent": "",
        "mesh_conditions": simulator.get_current_conditions(),
        "task_context": {"task": "maintain_mesh_health"},
        "handoff_history": [],
        "thread_id": "mesh-swarm-001"
    }
    
    result = app.invoke(initial_state, config=config)
    
    print("\n=== Run Complete ===")
    print(f"Messages: {len(result.get('messages', []))}")
    print(f"Blackboard keys: {list(result.get('blackboard', {}).keys())}")
    
    # Demonstrate persistence - get state from checkpointer
    print("\n--- Persistence Check ---")
    saved_state = app.get_state(config)
    print(f"State can be resumed from thread_id: mesh-swarm-001")
    
    return result


if __name__ == "__main__":
    run_with_persistence()