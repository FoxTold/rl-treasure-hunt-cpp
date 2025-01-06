import random


def deterministic_policy_eval_in_place(mdp, policy, gamma, theta):
    """
    This function uses the in-place approach to evaluate the specified deterministic policy for the specified MDP:

        'mdp' - model of the environment, use following functions:
        get_all_states - return list of all states available in the environment
        get_possible_actions - return list of possible actions for the given state
        get_next_states - return list of possible next states with a probability for transition from state by taking
                          action into next_state
        get_reward - return the reward after taking action in state and landing on next_state


        'policy' - the deterministic policy (action probability for each state), for the given mdp, too evaluate
        'gamma' - discount factor for MDP
        'theta' - algorithm should stop when minimal difference between previous evaluation of policy and current is
                  smaller than theta
    """
    def hash_state(state):
        return tuple(map(tuple, state))

    V = dict()

    for s in mdp.get_all_states():
        hashed_state = hash_state(s)
        V[hashed_state] = 0

    states = mdp.get_all_states()

    for s in states:
        has_player = False
        for x in range(len(s)):
            for y in range(x):
                if s[x][y] == 1:
                    has_player = True
        if not has_player:
            states.remove(s)

    while True:
        delta = 0
        for state in states:
            hashed_state = hash_state(state)
            old_value = V[hashed_state]

            action = policy[hashed_state]

            next_states = mdp.get_next_states(state, action)
            new_value = 0.0
            if not next_states:
                continue
            for next_state, prob in next_states.items():
                reward = mdp.get_reward(state, action, next_state)
                hashed_next_state = hash_state(next_state)
                new_value += prob * (reward + gamma * V[hashed_next_state])

            V[hashed_state] = new_value
            delta = max(delta, abs(old_value - V[hashed_state]))

        if delta < theta:
            break

    return V


def policy_improvement(mdp, policy, value_function, gamma):
    """
     This function improves specified deterministic policy for the specified MDP using value_function:

    'mdp' - model of the environment, use following functions:
         get_all_states - return list of all states available in the environment
         get_possible_actions - return list of possible actions for the given state
         get_next_states - return list of possible next states with a probability for transition from state by taking
                           action into next_state

         get_reward - return the reward after taking action in state and landing on next_state


    'policy' - the deterministic policy (action for each state), for the given mdp, too improve.
    'value_function' - the value function, for the given policy.
     'gamma' - discount factor for MDP

    Function returns False if policy was improved or True otherwise
    """

    policy_stable = True
    #
    # INSERT CODE HERE to evaluate the improved policy
    #
    for s in mdp.get_all_states():
        action = mdp.get_possible_actions(s)
        a_result = {}
        for a in action:
            temp = 0
            next_states = mdp.get_next_states(s, a)
            if not next_states:
                continue
            for s_next in next_states:
                temp += next_states[s_next] * (
                    mdp.get_reward(s, a, s_next) + gamma * value_function[s_next]
                )

            a_result[a] = temp
        try:
            max_value = max(a_result, key=a_result.get)
        except ValueError:
            continue

        if max_value != policy[s]:
            policy[s] = max_value
            policy_stable = False

    return policy_stable

def policy_iteration(mdp, gamma, theta):
    """
     This function calculate optimal policy for the specified MDP:

    'mdp' - model of the environment, use following functions:
         get_all_states - return list of all states available in the environment
         get_possible_actions - return list of possible actions for the given state
         get_next_states - return list of possible next states with a probability for transition from state by taking
                           action into next_state

         get_reward - return the reward after taking action in state and landing on next_state


    'gamma' - discount factor for MDP
    'theta' - algorithm should stop when minimal difference between previous evaluation of policy and current is smaller
               than theta
    Function returns optimal policy and value function for the policy
    """

    policy = dict()
    states = mdp.get_all_states()
    for s in states:
        actions = mdp.get_possible_actions(s)
        policy[s] = actions[0]

    V = deterministic_policy_eval_in_place(mdp, policy, gamma, theta)

    policy_stable = False

    while not policy_stable:
        policy_stable = policy_improvement(mdp, policy, V, gamma)
        V = deterministic_policy_eval_in_place(mdp, policy, gamma, theta)

    return policy, V

def hash_state(state):
    return tuple(map(tuple, state))

def value_iteration(mdp, gamma, theta):
    """
    This function calculate optimal policy for the specified MDP using Value Iteration approach:

    'mdp' - model of the environment, use following functions:
        get_all_states - return list of all states available in the environment
        get_possible_actions - return list of possible actions for the given state
        get_next_states - return list of possible next states with a probability for transition from state by taking
                          action into next_state
        get_reward - return the reward after taking action in state and landing on next_state


    'gamma' - discount factor for MDP
    'theta' - algorithm should stop when minimal difference between previous evaluation of policy and current is
              smaller than theta
    Function returns optimal policy and value function for the policy
    """

    V = dict()
    policy = dict()

    for current_state in mdp.get_all_states():
        V[current_state] = 0
        for action in mdp.get_possible_actions(current_state):
            policy[current_state] = action

    while True:
        delta = 0
        for state in mdp.get_all_states():
            if not mdp.get_possible_actions(state):
                continue

            action_values = {}
            for action in mdp.get_possible_actions(state):
                action_value = 0.0
                transitions = mdp.get_next_states(state, action)
                if not transitions:
                    continue
                for next_state, prob in transitions.items():
                    reward = mdp.get_reward(state, action, next_state)
                    action_value += prob * (reward + gamma * V[next_state])
                action_values[action] = action_value

            if not len(action_values):
                continue
            max_action_value = max(action_values.values())

            delta = max(delta, abs(max_action_value - V[state]))

            V[state] = max_action_value

        if delta < theta:
            break

    for state in mdp.get_all_states():
        if not mdp.get_possible_actions(state):
            policy[state] = None
            continue
        action_values = {}

        for action in mdp.get_possible_actions(state):
            action_value = 3
            transitions = mdp.get_next_states(state, action)
            if not transitions:
                continue
            for next_state, prob in transitions.items():
                reward = mdp.get_reward(state, action, next_state)
                action_value += prob * (reward + gamma * V[next_state])
            action_values[action] = action_value

        if not len(action_values):
            action_values[3]=3
        best_action = max(action_values, key=action_values.get)
        policy[state] = 3

    primt(policy)
    return policy, V


from Environment import *
if __name__ == "__main__":
    env = TreasureHuntEnv(render_mode="none")

    import time
    start = time.time()
    optimal_policy, optimal_value = value_iteration(env, 0.9, 0.001)
    print("Took %.2f seconds." % (time.time() - start))
    env.render_mode = "pygame"
    state = env.reset()
    done = False
    steps = 0

    while not done:

        hashed_state = hash_state(state)
        action = optimal_policy[hashed_state]  # Access optimal action for the current state
        state, reward, done, _ = env.step(action)
        print(state)
        steps += 1
        env.render()


