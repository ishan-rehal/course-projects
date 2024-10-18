class Circuit:
    def __init__(self):
        self.gates = {}
        self.nets = []
        self.pin_lookup = {}  # Dictionary to map pin names to pins
        self.connected_components = None
        self.a_to_bs = {}  # Dictionary to map each "a" to its "b"s
        self.made_to_list = False
    
    def add_gate(self, gate):
        self.gates[gate.name] = gate
        for pin in gate.pins:
            pin_name = f"{gate.name}.p{pin.pin_index}"
            self.pin_lookup[pin_name] = pin

    def add_net(self, net):
        self.nets.append(net)
        # Ensure "a" to "b" mapping for wire cost function
        a_pin_name = f"{net.pin1.gate_name}.p{net.pin1.pin_index}"
        b_pin_name = f"{net.pin2.gate_name}.p{net.pin2.pin_index}"
        if a_pin_name not in self.a_to_bs:
            self.a_to_bs[a_pin_name] = {a_pin_name}
        self.a_to_bs[a_pin_name].add(b_pin_name)

    def bounding_box(self, component):
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        for pin, gate in component:
            absolute_x = gate.x + pin.x
            absolute_y = gate.y + pin.y
            min_x = min(min_x, absolute_x)
            min_y = min(min_y, absolute_y)
            max_x = max(max_x, absolute_x)
            max_y = max(max_y, absolute_y)
        return min_x, min_y, max_x, max_y

    def semi_perimeter(self, bounding_box):
        min_x, min_y, max_x, max_y = bounding_box
        width = max_x - min_x
        height = max_y - min_y
        return width + height

    def total_wire_cost(self):
        total_cost = 0
        if not self.made_to_list:
            for a_pin, b_pins in self.a_to_bs.items():
                # Calculate bounding box of a and its corresponding b's
                self.a_to_bs[a_pin] = tuple(b_pins)
            self.made_to_list = True
            self.final_matrix = []
            for a_pins, b_pins in self.a_to_bs.items():
                temp = []
                for b_pin in b_pins:
                    b_pin_object = self.pin_lookup[b_pin]
                    gate_pin = self.gates[b_pin_object.gate_name]
                    temp.append((b_pin_object, gate_pin))
                self.final_matrix.append(temp)
            self.final_matrix = tuple([tuple(x) for x in self.final_matrix])

        for b_pins in self.final_matrix:
            # Calculate bounding box of a and its corresponding b's
            bounding_box = self.bounding_box(b_pins)
            total_cost += self.semi_perimeter(bounding_box)
        return total_cost