# Advanced LangGraph Swarm Example with Cyclic Behavior
# Supports multiple handoff rounds and loops between agents

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
    iteration_count: int
    thread_id: str


def create_advanced_swarm_graph(checkpointer=None):
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
        iteration = state.get("iteration_count", 0)

        # Safety limit to prevent infinite loops
        if iteration >= 6:
            return "end"

        # Priority routing
        if conditions.get("security_alert", False):
            return "security_agent"
        
        if (conditions.get("latency", 0) > 75 or 
            conditions.get("packet_loss", 0) > 4 or
            blackboard.get("optimization_needed", False)):
            return "optimizer"
        
        # After several events, aggregate context
        if len(blackboard.get("recent_events", [])) >= 2 and iteration % 2 == 0:
            return "context_aggregator"
        
        # Occasionally re-monitor (creates loop potential)
        if iteration > 0 and iteration % 3 == 0:
            return "network_monitor"
        
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

    # Allow some agents to loop back to monitoring for multiple rounds
    workflow.add_edge("optimizer", "network_monitor")   # Optimizer -> Monitor (loop)
    workflow.add_edge("context_aggregator", "network_monitor")  # Aggregator -> Monitor

    workflow.add_edge("security_agent", END)

    workflow.set_entry_point("network_monitor")
    
    if checkpointer:
        return workflow.compile(checkpointer=checkpointer)
    return workflow.compile()


def run_advanced_example():
    print("=== Advanced Cyclic LangGraph Swarm ===\n")
    
    checkpointer = MemorySaver()
    app = create_advanced_swarm_graph(checkpointer=checkpointer)
    
    config = {"configurable": {"thread_id": "advanced-swarm-001"}}
    simulator = MeshSimulator()
    
    initial_state: SwarmState = {
        "messages": [],
        "blackboard": {
            "optimization_needed": False,
            "recent_events": []
        },
        "current_agent": "",
        "mesh_conditions": simulator.get_current_conditions(),
        "task_context": {"task": "continuous_mesh_maintenance"},
        "handoff_history": [],
        "iteration_count": 0,
        "thread_id": "advanced-swarm-001"
    }
    
    result = app.invoke(initial_state, config=config)
    
    print("\n=== Advanced Run Complete ===")
    print(f"Total messages: {len(result.get('messages', []))}")
    print(f"Iterations completed: {result.get('iteration_count', 0)}")
    print(f"Final blackboard keys: {list(result.get('blackboard', {}).keys())}")
    
    return result


if __name__ == "__main__":
    run_advanced_example()