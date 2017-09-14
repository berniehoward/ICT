from simpleai.search import SearchProblem
import random

# Aid class for hill_climbing created by the 'simpleai' algorithm demands


class ParametersTuningLocalSearch(SearchProblem):
    def __init__(self, ranges, f, X, c, hops, function):
        # State is ([n_est, max_features, max_depth, min_samples_leaf], score)
        self.f = f
        self.X = X
        self.c = c
        self.ranges = ranges
        self.hops = hops
        self.function = function
        params = []
        for i in range(0, len(self.ranges)):
            params.append(random.choice(self.ranges[i]))
        r_forest, score = self.function(self.f, self.X, self.c, params)
        self.initial_state = params, score

    def initial_state(self):
        return self.initial_state

    def actions(self, state):
        actions = []
        for i in range(0, len(state)):
            new_action, score = state
            if (new_action[i] + self.hops[i]) in self.ranges[i]:
                new_action[i] += self.hops[i]
                actions.append(new_action)
                new_action[i] -= self.hops[i]
            if (new_action[i] - self.hops[i]) in self.ranges[i]:
                new_action[i] -= self.hops[i]
                actions.append(new_action)
        return actions

    def result(self, state, action):
        r_forest, score = self.function(self.f, self.X, self.c, action)
        return action, score

    def value(self, state):
        x = 5
        action, score = state
        # The algorithm return the state with the higher score but we want the minimum.
        return score * -1