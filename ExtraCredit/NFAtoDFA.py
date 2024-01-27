import argparse
from itertools import combinations

# Defining class that can be used for both nfas and dfas
class Automaton:
    def __init__(self, states, symbols, start_state, accept_states, transitions):
        self.states = states
        self.symbols = symbols
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

# Reading through the input file to get data about nfa
def read_nfa(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()

    states = []
    for state in lines[0].strip().split('\t'):
        states.append(state.strip('{}')) # Ignoring brackets to make storing easier

    symbols = lines[1].strip().split('\t')

    start_state = lines[2].split()[0][1]

    accept_states = []
    for state in lines[3].strip().split('\t'):
        accept_states.append(state.strip('{}'))

    # Where I made a mistake of using a dictionary to store transitions. I am not sure what structure I could have used instead of a dictionary
    # but I thought it would work.
    transitions = {}
    for line in lines[5:-1]:
        line_half1 = line.split(' = ')[0]
        line_half2 = line.split(' = ')[1]
        initial_state = line_half1.split(', ')[0].strip('{}')
        symbol = line_half1.split(', ')[1]
        next_state = line_half2.split()[0].strip('{}')
        
        transitions[initial_state + symbol] = next_state

    return Automaton(states, symbols, start_state, accept_states, transitions)

# Code to perform conversion
def convert_nfa_to_dfa(nfa):
    # power set of all states
    dfa_states = []
    for i in range(len(nfa.states) + 1):
        for states in combinations(nfa.states, i):
            dfa_states.append(list(states))

    # Epsilon transition on start state if applicable
    dfa_start_state = []
    dfa_start_state.append(nfa.start_state)
    eps_transition = epsilon_transition(nfa, nfa.start_state)
    for eps in eps_transition:
        dfa_start_state.append(eps)

    # Transitions of dfa
    dfa_transitions = {}
    curr_state = nfa.start_state
    temp_transitions = nfa.transitions.copy() # Wanted to have transitions removed after each use for each symbol iteration
    for state in nfa.states: # Going through the possible states from nfa
        temp_transitions = nfa.transitions.copy() # Resetting transition pool
        for symbol in nfa.symbols: # Going through each symbol
            new_dfa_state = [] # Initializing next state
            for s in curr_state: # Going through the current states to check for each new possible transition
                # Checking if the current state has an available transition and does not overlap with previously made transitions
                if ((nfa.transitions.get(s + symbol) != None) and (nfa.transitions.get(s + symbol) not in new_dfa_state)): 
                    new_dfa_state.append(nfa.transitions.get(s + symbol))
                    temp_transitions.pop(s+symbol)
                # Performing an epsilon transition if applicable
                elif (epsilon_transition(nfa, s) != []):
                    new_dfa_state.append(s)
                    new_dfa_state.append(nfa.transitions.get(s + "EPS"))
                    temp_transitions.pop(s+"EPS")
                
            new_dfa_state.sort()
            # To make sure output file has accurate start state in transitions
            if(curr_state == nfa.start_state):
                dfa_transitions[(tuple(dfa_start_state), symbol)] = new_dfa_state
            else:
                dfa_transitions[(tuple(curr_state), symbol)] = new_dfa_state
        curr_state = new_dfa_state # Updating current state with each pass, would also need to fix this

    # Accept states are wrong but I would implement the transitions to get them if I had accurate transitions
    dfa_accept_states = []
    for state in dfa_states:
        for s in nfa.accept_states:
            if (s in state and s in dfa_start_state):
                dfa_accept_states.append(tuple(state))

    dfa = Automaton(dfa_states, nfa.symbols, dfa_start_state, dfa_accept_states, dfa_transitions)

    return dfa

# Method to see if there is a epsilon transition and if so perform it
def epsilon_transition(nfa, state):
    transition = [] # Stores all previous transitions
    stack = [state] # Stack of the current state

    while len(stack) > 0: # Looping until the stack is empty
        current_state = stack.pop()
        
        epsilon_transitions = nfa.transitions.get((current_state + 'EPS'), []) # Gets the corresponding value with the state and EPS, i.e. '1EPS'
        for next_state in epsilon_transitions: 
            if next_state not in transition: # Continuing epsilon transition possibilities
                transition.append(next_state)
                stack.append(next_state)

    return transition # Returning list of possible transitions

# Writing to output file
def write_dfa(automaton, file_name):
    file = open(file_name, 'w')
    for state in automaton.states:
        # Formatting for {EM}
        if len(state) == 0:
            file.write('{EM}\t')
        else:
            file.write('{' + ', '.join(map(str, state)) + '}\t')
    file.write('\n')

    file.write('\t'.join(automaton.symbols) + '\n')
    file.write('{' + ', '.join(automaton.start_state) + '}\n')
    for acceptState in automaton.accept_states:
        file.write('{' + (', '.join(map(str, acceptState))) + '}\t')
    file.write('\n')

    file.write('BEGIN\n')
    for (state, symbol), transitions in automaton.transitions.items():
        # All if statements below to check if there is an empty array and inputting {EM} for correct formatting
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
    # parser to allow for CLI
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file') # Input file on line
    args = parser.parse_args() # Args to read input file
    nfa = read_nfa(args.input_file)
    dfa = convert_nfa_to_dfa(nfa)
    output_file = 'output.DFA' # Choosing output file name
    write_dfa(dfa, output_file)

if __name__ == '__main__':
    main()
