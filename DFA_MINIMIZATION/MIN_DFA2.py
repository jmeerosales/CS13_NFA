class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states, name="DFA", language=""):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.name = name
        self.language = language

    def process_string(self, input_string):
        """Traces an input string through the DFA and returns (is_accepted, final_state)."""
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False, "Invalid Symbol"
            current_state = self.transitions[current_state][symbol]
        return (current_state in self.accept_states), current_state

    def minimize(self):
        """Minimizes the DFA using Moore's Partition Refinement Algorithm."""
        # Step 1: Remove unreachable states
        reachable = set()
        queue = [self.start_state]
        while queue:
            s = queue.pop(0)
            if s not in reachable:
                reachable.add(s)
                for sym in self.alphabet:
                    if sym in self.transitions[s]:
                        queue.append(self.transitions[s][sym])
        
        valid_states = self.states & reachable
        valid_accept = self.accept_states & reachable

        # Step 2: Partition refinement
        partitions = [valid_accept.copy(), (valid_states - valid_accept).copy()]
        partitions = [group for group in partitions if len(group) > 0]

        while True:
            new_partitions = []
            changed = False

            for group in partitions:
                if len(group) <= 1:
                    new_partitions.append(group)
                    continue

                subgroups = {}
                for state in group:
                    signature = []
                    for sym in sorted(self.alphabet):
                        target = self.transitions[state][sym]
                        for idx, part in enumerate(partitions):
                            if target in part:
                                signature.append(idx)
                                break
                    signature_key = tuple(signature)
                    subgroups.setdefault(signature_key, set()).add(state)

                splits = list(subgroups.values())
                if len(splits) > 1:
                    changed = True
                new_partitions.extend(splits)

            partitions = new_partitions
            if not changed:
                break

        # Step 3: Reconstruct Minimized DFA
        state_map = {}
        min_states = set()
        for group in partitions:
            label = "".join(sorted(group))
            min_states.add(label)
            for state in group:
                state_map[state] = label

        min_start = state_map[self.start_state]
        min_accept = {state_map[s] for s in valid_accept}
        min_transitions = {}

        for group in partitions:
            group_label = state_map[next(iter(group))]
            rep_state = next(iter(group))
            min_transitions[group_label] = {}
            for sym in self.alphabet:
                target = self.transitions[rep_state][sym]
                min_transitions[group_label][sym] = state_map[target]

        return DFA(
            states=min_states,
            alphabet=self.alphabet,
            transitions=min_transitions,
            start_state=min_start,
            accept_states=min_accept,
            name=f"{self.name} (Minimized)",
            language=self.language
        )


# Definition for Whiteboard Example 2
p4_transitions = {
    'A': {'0': 'B', '1': 'C'},
    'B': {'0': 'A', '1': 'D'},
    'C': {'0': 'E', '1': 'F'},
    'D': {'0': 'E', '1': 'F'},
    'E': {'0': 'E', '1': 'F'},
    'F': {'0': 'F', '1': 'F'}
}

dfa4 = DFA(
    states={'A', 'B', 'C', 'D', 'E', 'F'},
    alphabet={'0', '1'},
    transitions=p4_transitions,
    start_state='A',
    accept_states={'C', 'D', 'E'},
    name="Whiteboard DFA Example 2",
    language="L = { w ∈ {0, 1}* | w contains exactly one '1' }"
)

if __name__ == "__main__":
    min_dfa4 = dfa4.minimize()

    print("=" * 70)
    print(f"RUNNING: {dfa4.name}")
    print(f"Language: {dfa4.language}")
    print("=" * 70)
    print(f"Original States  : {dfa4.states}")
    print(f"Minimized States : {min_dfa4.states}")

    # --- SECTION 1: PRESET TEST CASES TABLE ---
    accepted_tests = ['1', '01']
    rejected_tests = ['0', '11']
    all_tests = [(s, "Accepted") for s in accepted_tests] + [(s, "Rejected") for s in rejected_tests]

    print("\n--- TEST CASES TABLE ---")
    print(f"{'Input String':<15} | {'Type':<10} | {'Original Result':<20} | {'Minimized Result':<20}")
    print("-" * 70)

    for input_str, expected_type in all_tests:
        orig_acc, orig_st = dfa4.process_string(input_str)
        min_acc, min_st = min_dfa4.process_string(input_str)

        orig_res = f"{'ACCEPT' if orig_acc else 'REJECT'} (State: {orig_st})"
        min_res = f"{'ACCEPT' if min_acc else 'REJECT'} (State: {min_st})"

        print(f"{input_str:<15} | {expected_type:<10} | {orig_res:<20} | {min_res:<20}")

    print("\n" + "=" * 70)
    print("INPUT CHECKER")
    print("=" * 70)

    while True:
        user_input = input("\nEnter binary string (or type 'X' to quit): ").strip()

        if user_input.lower() in ('x', 'exit'):
            print("Exiting interactive mode.")
            break

        orig_accepted, orig_end = dfa4.process_string(user_input)
        min_accepted, min_end = min_dfa4.process_string(user_input)

        if orig_end == "Invalid Symbol":
            print("Error: Input contains invalid characters. Use 0 or 1 only.")
            continue

        print("\n--- Original Graph ---")
        print(f"  Start State : {dfa4.start_state}")
        print(f"  End State   : {orig_end}")
        print(f"  Status      : {'ACCEPTED' if orig_accepted else 'REJECTED'}")

        print("--- Minimized Graph ---")
        print(f"  Start State : {min_dfa4.start_state}")
        print(f"  End State   : {min_end}")
        print(f"  Status      : {'ACCEPTED' if min_accepted else 'REJECTED'}")