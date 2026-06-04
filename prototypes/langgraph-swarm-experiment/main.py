# Advanced LangGraph Swarm with SQLite Persistence + Emotional Agent

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

# Agents
from agents.network_monitor import NetworkMonitor
from agents.optimizer import Optimizer
from agents.security_agent import SecurityAgent
from agents.context_aggregator import ContextAggregator
from agents.emotional_alignment import EmotionalAlignmentAgent

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


def create_swarm_graph(checkpointer=None):
    workflow = StateGraph(SwarmState)

    monitor = NetworkMonitor()
    optimizer = Optimizer()
    security = SecurityAgent()
    aggregator = ContextAggregator()
    emotional = EmotionalAlignmentAgent()

    workflow.add_node("network_monitor", monitor.run)
    workflow.add_node("optimizer", optimizer.run)
    workflow.add_node("security_agent", security.run)
    workflow.add_node("context_aggregator", aggregator.run)
    workflow.add_node("emotional_alignment", emotional.run)

    def decide_next_agent(state: dict) -> str:
        conditions = state.get("mesh_conditions", {})
        blackboard = state.get("blackboard", {})
        iteration = state.get("iteration_count", 0)

        if iteration >= 8:
            return "end"

        if conditions.get("security_alert", False):
            return "security_agent"
        
        if (conditions.get("latency", 0) > 75 or 
            conditions.get("packet_loss", 0) > 4 or
            blackboard.get("optimization_needed", False)):
            return "optimizer"
        
        if len(blackboard.get("recent_events", [])) >= 2 and iteration % 2 == 0:
            return "context_aggregator"
        
        # Occasionally involve emotional alignment
        if iteration > 2 and iteration % 3 == 0:
            return "emotional_alignment"
        
        if iteration > 0 and iteration % 4 == 0:
            return "network_monitor"
        
        return "end"

    workflow.add_conditional_edges(
        "network_monitor",
        decide_next_agent,
        {
            "optimizer": "optimizer",
            "security_agent": "security_agent",
            "context_aggregator": "context_aggregator",
            "emotional_alignment": "emotional_alignment",
            "end": END
        }
    )

    # Cyclic edges for multi-round behavior
    workflow.add_edge("optimizer", "network_monitor")
    workflow.add_edge("context_aggregator", "network_monitor")
    workflow.add_edge("emotional_alignment", "network_monitor")

    workflow.add_edge("security_agent", END)
    workflow.set_entry_point("network_monitor")
    
    if checkpointer:
        return workflow.compile(checkpointer=checkpointer)
    return workflow.compile()


def run_with_sqlite_persistence():
    print("=== LangGraph Swarm with SQLite Persistence ===\n")
    
    # Real persistence using SQLite
    db_path = "swarm_state.db"
    checkpointer = SqliteSaver.from_conn_string(f"sqlite:///{db_path}")
    
    app = create_swarm_graph(checkpointer=checkpointer)
    
    config = {"configurable": {"thread_id": "persistent-swarm-001"}}
    simulator = MeshSimulator()
    
    initial_state = {
        "messages": [],
        "blackboard": {
            "optimization_needed": False,
            "recent_events": []
        },
        "current_agent": "",
        "mesh_conditions": simulator.get_current_conditions(),
        "task_context": {"task": "long_running_mesh_optimization"},
        "handoff_history": [],
        "iteration_count": 0,
        "thread_id": "persistent-swarm-001"
    }
    
    result = app.invoke(initial_state, config=config)
    
    print("\n=== Run Complete ===")
    print(f"Messages generated: {len(result.get('messages', []))}")
    print(f"State persisted to: {db_path}")
    print("You can resume this thread later using the same thread_id.")
    
    return result


if __name__ == "__main__":
    run_with_sqlite_persistence()