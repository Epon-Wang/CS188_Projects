# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(
            self, 
            mdp:        mdp.MarkovDecisionProcess, 
            discount:   float = 0.9, 
            iterations: int = 100
        ) -> None:
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()


    def runValueIteration(self):
        """ 
          Run Value Iteration for a specified number of iterations.
        """
        for _ in range(self.iterations):

            # init new V-table for each iter
            v_table = util.Counter()

            # get max q for all a of each s
            for s in self.mdp.getStates():
                if self.mdp.isTerminal(s):
                    continue
                
                actions = self.mdp.getPossibleActions(s)
                v_table[s] = max(
                    self.getQValue(s, a) for a in actions
                ) if actions else 0
            
            # update V-table
            self.values = v_table


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        q = 0

        for s_next, P in self.mdp.getTransitionStatesAndProbs(state, action):
            v_next = self.getValue(s_next)
            r_next = self.mdp.getReward(state, action, s_next)
            q += P * (r_next + self.discount * v_next)

        return q


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        actions = self.mdp.getPossibleActions(state)

        return max(
            actions, 
            key=lambda a: self.getQValue(state, a)
        ) if actions else None


    def getPolicy(self, state):
        return self.computeActionFromValues(state)


    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)


    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)



class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(
            self, 
            mdp:        mdp.MarkovDecisionProcess, 
            discount:   float = 0.9, 
            iterations: int = 100, 
            theta:      float = 1e-5
        ) -> None:
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)


    def runValueIteration(self):
        """
          Run the Prioritized Sweeping Value Iteration for a specified number of iterations.
        """
        # compute predecessors of all s
        predecessors = {s: set() for s in self.mdp.getStates()}
        for s in self.mdp.getStates():
            for a in self.mdp.getPossibleActions(s):
                for s_next, P in self.mdp.getTransitionStatesAndProbs(s, a):
                    if P > 0:
                        predecessors[s_next].add(s)
        
        pq = util.PriorityQueue()

        # compute priorities of all s
        for s in self.mdp.getStates():
            if self.mdp.isTerminal(s):
                continue

            # get max q for all a of an s
            actions = self.mdp.getPossibleActions(s)
            max_q = max(
                self.getQValue(s, a) for a in actions
            ) if actions else 0
            
            # push s into priority queue with priority=-diff
            diff = abs(self.getValue(s) - max_q)
            pq.push(s, -diff)
        
        for _ in range(self.iterations):
            if pq.isEmpty():
                break

            s = pq.pop()
            if self.mdp.isTerminal(s):
                continue

            # update V-table
            actions = self.mdp.getPossibleActions(s)
            self.values[s] = max(
                self.getQValue(s, a) for a in actions
            ) if actions else 0

            # compute priorities of all predecessors of s
            for ps in predecessors[s]:
                if self.mdp.isTerminal(ps):
                    continue

                actions = self.mdp.getPossibleActions(ps)
                max_q = max(
                    self.getQValue(ps, a) for a in actions
                ) if actions else 0

                # push ps into priority queue with priority=-diff
                diff = abs(self.getValue(ps) - max_q)
                if diff > self.theta:
                    pq.update(ps, -diff)