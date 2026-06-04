# Base Agent class with common functionality

from typing import Any


class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def run(self, state: dict) -> dict:
        """Main execution method. Should be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement run()")

    def decide_handoff(self, state: dict) -> str:
        """Return the name of the next agent or 'end'."""
        raise NotImplementedError("Subclasses must implement decide_handoff()")

    def log(self, message: str):
        print(f"[{self.name}] {message}")