def read_variables():
    states = input("Введите множество состояний: ").split()
    alphabet = input("Введите алфавит ввода: ").split()
    transitions = {}
    print("Введите функцию переходов (текущее состояние, входной символ, следующее состояние): ")
    transitions_input = input()
    while transitions_input != "":
        current_state, input_char, next_state = transitions_input.split()
        if transitions.get((current_state, input_char)) is not None:
            transitions[(current_state, input_char)] += next_state
        else:
            transitions[(current_state, input_char)] = next_state
        transitions_input = input()
    for key in transitions.keys():
        transitions[key] = "".join(sorted(transitions[key]))
    transitions = dict(sorted(transitions.items()))
    initial_states = input("Введите множество начальных состояний: ").split()
    final_states = input("Введите множество конечных состояний: ").split()

    return states, alphabet, transitions, initial_states, final_states


def nfa_to_dfa(alphabet, transitions, initial_states, final_states):
    new_transitions = {}
    new_initial_state = "".join(initial_states)

    for initial in new_initial_state:
        for symb in alphabet:
            if new_transitions.get((new_initial_state, symb)) is not None:
                new_transitions[(new_initial_state, symb)] += transitions[(initial, symb)]
            else:
                if transitions.get((initial, symb)) is not None:
                    new_transitions[(new_initial_state, symb)] = transitions[(initial, symb)]

    for key in new_transitions.keys():
        new_transitions[key] = "".join(sorted(new_transitions[key]))
    new_transitions = dict(sorted(new_transitions.items()))
    list_transitions = list(new_transitions.values())

    while list_transitions:
        item = list_transitions.pop()
        for state in item:
            for symb in alphabet:
                if new_transitions.get((item, symb)) is not None:
                    new_transitions[(item, symb)] += transitions[(state, symb)]
                else:
                    if transitions.get((state, symb)) is not None:
                        new_transitions[(item, symb)] = transitions[(state, symb)]
        for key in new_transitions.keys():
            new_transitions[key] = "".join(sorted(set(new_transitions[key])))
        new_transitions = dict(sorted(new_transitions.items()))
        keys = list(zip(*new_transitions))[0]
        for val in new_transitions.values():
            if val not in keys:
                list_transitions.append(val)

    new_states = sorted(set(new_transitions.values()))
    if new_initial_state not in new_states:
        new_states.append(new_initial_state)
        new_states.sort()
    new_final_states = []
    for final in final_states:
        for val in set(new_transitions.values()):
            if final in val:
                new_final_states.append(val)

    return new_states, alphabet, new_transitions, new_initial_state, new_final_states


def print_transitions(transitions):
    for key, val in transitions.items():
        print(f"D("".join(key[0])}, {"".join(key[1])}) = {val}")


states, alphabet, transitions, initial_states, final_states = read_variables()
print("\nНКА")
print("Множество состояний:", ", ".join(states))
print("Алфавит ввода:", ", ".join(alphabet))
print("Функции переходов:")
print(transitions)
print_transitions(transitions)
print("Начальные состояния:", ", ".join(initial_states))
print("Конечные состояния:", ", ".join(final_states))
states, alphabet, transitions, initial_states, final_states = nfa_to_dfa(alphabet, transitions, initial_states,
                                                                         final_states)
print("\nДКА")
print("Множество состояний:", ", ".join(states))
print("Алфавит ввода:", ", ".join(alphabet))
print("Функции переходов:")
print_transitions(transitions)
print("Начальные состояния:", ", ".join(initial_states))
print("Конечные состояния:", ", ".join(final_states))
