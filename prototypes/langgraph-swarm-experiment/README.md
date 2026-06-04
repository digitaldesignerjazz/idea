# LangGraph Swarm Experiment (Phase 1)

**Goal**: Prototype a minimal 3-5 agent swarm using LangGraph that can operate in a simulated mesh environment, with dynamic handoffs and a shared blackboard.

## Experiment Objectives

- Implement basic agent roles (Network Monitor, Optimizer, Security Agent)
- Demonstrate dynamic task handoff between agents
- Implement a simple shared blackboard for collective awareness
- Test behavior under normal conditions and simulated network partitions
- Measure basic metrics (coordination success, latency, token usage)

## Architecture Overview

- Use **LangGraph** for stateful multi-agent orchestration
- Agents communicate via structured messages + shared state
- Simulated mesh environment (can start with simple in-memory simulation, later Docker + Yggdrasil)
- Focus on emergence of coordination rather than full LLM intelligence initially

## Project Structure

```
langgraph-swarm-experiment/
├── README.md
├── main.py                 # Entry point and graph compilation
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── network_monitor.py
│   ├── optimizer.py
│   ├── security_agent.py
├── state/
│   ├── shared_blackboard.py
│   ├── mesh_state.py
├── tools/
│   ├── mesh_tools.py
├── utils/
│   ├── simulation.py
└── requirements.txt
```

## Getting Started (Planned)

```bash
git clone ...
cd langgraph-swarm-experiment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Next Milestones

1. Define agent roles and tools
2. Build the LangGraph state graph with handoff logic
3. Implement shared blackboard
4. Add basic mesh simulation
5. Run first successful multi-agent coordination
6. Add partition/failure scenarios

**Status**: Scaffolding created — ready for implementation.