# Improved Mesh Simulator with Events and Failures

import random


class MeshSimulator:
    def __init__(self):
        self.base_latency = 45
        self.base_packet_loss = 1.5
        self.node_count = 12
        self.failed_nodes = set()
        
    def get_current_conditions(self) -> dict:
        """Return current simulated mesh conditions."""
        latency = self.base_latency + random.randint(-8, 40)
        packet_loss = max(0, self.base_packet_loss + random.uniform(-0.3, 3.0))
        
        # Account for failed nodes
        effective_nodes = self.node_count - len(self.failed_nodes)
        
        return {
            "latency": round(latency),
            "packet_loss": round(packet_loss, 1),
            "security_alert": random.random() < 0.12,
            "node_count": effective_nodes,
            "failed_nodes": len(self.failed_nodes),
            "timestamp": "simulated"
        }
    
    def simulate_event(self) -> dict:
        """Simulate network events including failures."""
        roll = random.random()
        
        if roll < 0.15:  # Node failure
            if self.node_count - len(self.failed_nodes) > 3:
                node_id = f"node-{random.randint(1, self.node_count):02d}"
                self.failed_nodes.add(node_id)
                return {
                    "type": "node_failure",
                    "node": node_id,
                    "description": f"Node {node_id} became unreachable"
                }
        elif roll < 0.35:  # Congestion
            return {
                "type": "congestion",
                "latency_increase": random.randint(15, 45),
                "description": "Sudden congestion detected"
            }
        else:
            return {
                "type": "normal",
                "description": "Network conditions stable"
            }
    
    def recover_node(self):
        """Simulate node recovery."""
        if self.failed_nodes:
            recovered = self.failed_nodes.pop()
            return {"type": "recovery", "node": recovered}
        return None