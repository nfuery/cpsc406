import argparse
import re
from itertools import combinations

# Removed unused State class

class Automaton:
    """
    A class to represent a generic automaton (NFA or DFA).
    """
    def __init__(self, states, symbols, start_state, accept_states, transitions):
        self.states = states
        self.symbols = symbols
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

def read_automaton(file_name: str) -> Automaton:
    """
    Reads an automaton (NFA or DFA) from a file.
    """
    with open(file_name, 'r') as file:
        lines = file.readlines()
        states = lines[0].strip().split('\t')
        symbols = lines[1].strip().split('\t')
        start_state = lines[2].strip()
        accept_states = lines[3].strip().split('\t')
        transitions = {line.strip().split(', ')[0]: line.strip().split(' = ')[1] for line in lines[5:-1]}
        return Automaton(states, symbols, start_state, accept_states, transitions)

def convert_nfa_to_dfa(nfa: Automaton) -> Automaton:
    """
    Converts a given NFA to a DFA.
    """
    # Create a list of all possible states (subsets of the NFA states)
    dfa_states = [set(states) for i in range(len(nfa.states) + 1) for states in combinations(nfa.states, i)]
    
    # Initialize the DFA transitions as an empty dictionary
    dfa_transitions = {}

    # For each DFA state (which is a subset of NFA states)
    for dfa_state in dfa_states:
        # For each symbol in the alphabet
        for symbol in nfa.symbols:
            # The new DFA state is the union of the NFA transitions for each state in the subset
            new_dfa_state = set().union(*[nfa.transitions.get((state, symbol), set()) for state in dfa_state])
            # Add the transition to the DFA transitions
            dfa_transitions[(frozenset(dfa_state), symbol)] = new_dfa_state

    # The start state of the DFA is the same as the NFA
    dfa_start_state = nfa.start_state

    # The accept states of the DFA are those that contain at least one NFA accept state
    dfa_accept_states = [dfa_state for dfa_state in dfa_states if any(state in dfa_state for state in nfa.accept_states)]

    # Create the DFA
    dfa = Automaton(dfa_states, nfa.symbols, dfa_start_state, dfa_accept_states, dfa_transitions)

    return dfa

def write_automaton(automaton: Automaton, file_name: str) -> None:
    """
    Writes a given automaton (NFA or DFA) to a file.
    """
    with open(file_name, 'w') as file:
        file.write('\t'.join(['{' + ', '.join(state) + '}' for state in automaton.states]) + '\n')
        file.write('\t'.join(automaton.symbols) + '\n')
        file.write('{' + ', '.join(automaton.start_state) + '}' + '\n')
        file.write('\t'.join(['{' + ', '.join(state) + '}' for state in automaton.accept_states]) + '\n')
        file.write('BEGIN\n')
        for (state, symbol), transitions in automaton.transitions.items():
            file.write('{' + ', '.join(state) + '}, ' + symbol + ' = {' + ', '.join(transitions) + '}' if transitions else '{EM}' + '\n')
        file.write('END\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='The input file containing the NFA specification')
    args = parser.parse_args()

    nfa = read_automaton(args.input_file)
    dfa = convert_nfa_to_dfa(nfa)
    write_automaton(dfa, args.input_file.replace('.nfa', '.DFA'))

if __name__ == '__main__':
    main()
