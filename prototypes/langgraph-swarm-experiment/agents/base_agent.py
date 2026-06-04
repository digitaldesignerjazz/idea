# Base class for swarm agents

from typing import TypedDict


class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def run(self, state: dict) -> dict:
        """Process current state and return updates."""
        raise NotImplementedError("Subclasses must implement run()")

    def decide_handoff(self, state: dict) -> str:
        """Decide which agent to hand off to next (or END)."""
        raise NotImplementedError("Subclasses must implement decide_handoff()")