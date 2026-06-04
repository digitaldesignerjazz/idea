# Simple Mesh Network Simulator

import random


class MeshSimulator:
    """Simple simulator for mesh network conditions."""
    
    def __init__(self):
        self.base_latency = 45
        self.base_packet_loss = 1.5
        self.node_count = 12
        
    def get_current_conditions(self) -> dict:
        """Return current simulated mesh conditions."""
        # Add some randomness to make it realistic
        latency = self.base_latency + random.randint(-10, 35)
        packet_loss = max(0, self.base_packet_loss + random.uniform(-0.5, 2.5))
        
        return {
            "latency": round(latency),
            "packet_loss": round(packet_loss, 1),
            "security_alert": random.random() < 0.15,  # 15% chance
            "node_count": self.node_count,
            "timestamp": "simulated"
        }
    
    def simulate_event(self) -> dict:
        """Simulate a network event (congestion, node failure, etc)."""
        event_type = random.choice(["congestion", "node_failure", "normal"])
        
        if event_type == "congestion":
            return {
                "type": "congestion",
                "latency_increase": random.randint(20, 50),
                "description": "Network congestion detected"
            }
        elif event_type == "node_failure":
            return {
                "type": "node_failure",
                "affected_nodes": random.randint(1, 3),
                "description": "Node(s) became unreachable"
            }
        else:
            return {
                "type": "normal",
                "description": "Network operating normally"
            }