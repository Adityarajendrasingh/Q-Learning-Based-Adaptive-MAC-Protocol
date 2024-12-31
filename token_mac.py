import simpy

class Token:
    """Represents a token used for granting access to nodes."""
    def __init__(self, env, initial_value, total_nodes):
        self.env = env
        self.value = initial_value
        self.total_nodes = total_nodes
        self.current_holder = 0  # Tracks which node holds the token

    def pass_token(self):
        """Rotate the token to the next node."""
        self.current_holder = (self.current_holder + 1) % self.total_nodes


class TokenNode:
    """Represents a node in the token-based MAC simulation."""
    def __init__(self, env, node_id, token, slot_duration, window_size):
        self.env = env
        self.node_id = node_id
        self.token = token
        self.slot_duration = slot_duration
        self.window_size = window_size
        self.sent_packets = 0
        self.failed_packets = 0
        self.total_delay = 0
        self.packet_count = 0

    def operate(self):
        """Simulate the node's operation."""
        while True:
            if self.token.current_holder == self.node_id:
                if self.packet_count > 0:  # If packets are available to send
                    self.sent_packets += 1
                    self.total_delay += self.slot_duration * self.packet_count
                    self.packet_count -= 1
                self.token.pass_token()
            yield self.env.timeout(self.slot_duration)


def run_token_simulation(sim_time, num_nodes, slot_duration, window_size):
    """Run the token-based MAC simulation for a given window size."""
    env = simpy.Environment()
    token = Token(env, initial_value=0, total_nodes=num_nodes)
    nodes = [TokenNode(env, node_id, token, slot_duration, window_size) for node_id in range(num_nodes)]

    # Start node operations
    for node in nodes:
        env.process(node.operate())

    # Run the simulation
    env.run(until=sim_time)

    # Collect metrics
    total_sent = sum(node.sent_packets for node in nodes)
    total_failed = sum(node.failed_packets for node in nodes)
    avg_delay = sum(node.total_delay / max(1, node.packet_count) for node in nodes) / len(nodes)

    return total_sent, total_failed, avg_delay