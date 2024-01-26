import argparse
from itertools import combinations

class Automaton:
    def __init__(self, states, symbols, start_state, accept_states, transitions):
        self.states = states
        self.symbols = symbols
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

def read_nfa(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()

    states = []
    for state in lines[0].strip().split('\t'):
        states.append(state.strip('{}'))

    symbols = lines[1].strip().split('\t')

    start_state = lines[2].strip('{}')

    accept_states = []
    for state in lines[3].strip().split('/t'):
        accept_states.append(state.strip('{}'))

    transitions = {}
    for line in lines[5:-1]:
        initial_state = tuple(line.strip('{}').split(', ')[0].split())
        print(initial_state)
        next_state = line.strip().split(' = ')[1].split(', ')
        transitions[initial_state] = next_state

    return Automaton(states, symbols, start_state, accept_states, transitions)

def convert_nfa_to_dfa(nfa):
    dfa_states = []
    for i in range(len(nfa.states) + 1):
        for states in combinations(nfa.states, i):
            # if the state is reachable
                dfa_states.append(list(states))

    dfa_transitions = {}
    
    for dfa_state in dfa_states:
        for symbol in nfa.symbols:
            new_dfa_state = dict()
            for state in dfa_state:
                new_dfa_state.update(nfa.transitions.get((state, symbol), []))
                # print(nfa.transitions.get(state, symbol))

            dfa_transitions[(tuple(dfa_state), symbol)] = list(new_dfa_state)
    # print(dfa_transitions)
    dfa_start_state = tuple(epsilon_closure(nfa, nfa.start_state))

    dfa_accept_states = [tuple(state) for state in dfa_states if any(s in state for s in nfa.accept_states)]

    dfa = Automaton(dfa_states, nfa.symbols, dfa_start_state, dfa_accept_states, dfa_transitions)

    return dfa

def epsilon_closure(nfa, state):
    closure = set([state])
    stack = [state]

    while stack:
        current_state = stack.pop()
        epsilon_transitions = nfa.transitions.get((current_state, 'EPS'), [])
        for next_state in epsilon_transitions:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)

    return list(closure)

def write_dfa(automaton, file_name):
    file = open(file_name, 'w')
    for state in automaton.states:
        if len(state) == 0:
            file.write('{EM}\t')
        else:
            file.write('{' + ', '.join(map(str, state)) + '}\t')
    file.write('\n')

    file.write('\t'.join(automaton.symbols) + '\n')
    file.write('{' + ', '.join(automaton.start_state))
    for acceptState in automaton.accept_states:
        file.write('{' + (', '.join(map(str, acceptState))) + '}\t')
    file.write('\n')

    file.write('BEGIN\n')
    for (state, symbol), transitions in automaton.transitions.items():
        if len(state) == 0 and len(transitions) == 0:
            file.write('{EM}, ' + symbol + ' = ' + '{EM}\n')
        elif len(state) == 0:
            file.write('{EM}, ' + symbol + ' = ' + '{' + ', '.join(transitions) + '}\n')
        elif len(transitions) == 0:
            file.write('{' + ', '.join(map(str, state)) + '}, ' + symbol + ' = ' + '{EM}\n')
        else:
            file.write('{' + ', '.join(map(str, state)) + '}, ' + symbol + ' = ' + '{' + ', '.join(transitions) + '}\n')
    file.write('END\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    args = parser.parse_args()
    nfa = read_nfa(args.input_file)
    dfa = convert_nfa_to_dfa(nfa)
    # CHANGE TO OUTPUT.DFA
    output_file = 'input.DFA'
    write_dfa(dfa, output_file)

if __name__ == '__main__':
    main()
