import util, random
import numpy as np

class Agent:

  def getAction(self, state):
    """
    For the given state, get the agent's chosen
    action.  The agent knows the legal actions
    """
    abstract

  def getValue(self, state):
    """
    Get the value of the state.
    """
    abstract

  def getQValue(self, state, action):
    """
    Get the q-value of the state action pair.
    """
    abstract

  def getPolicy(self, state):
    """
    Get the policy recommendation for the state.

    May or may not be the same as "getAction".
    """
    abstract

  def update(self, state, action, nextState, reward):
    """
    Update the internal state of a learning agent
    according to the (state, action, nextState)
    transistion and the given reward.
    """
    abstract


class RandomAgent(Agent):
  """
  Clueless random agent, used only for testing.
  """

  def __init__(self, actionFunction):
    self.actionFunction = actionFunction

  def getAction(self, state):
    return random.choice(self.actionFunction(state))

  def getValue(self, state):
    return 0.0

  def getQValue(self, state, action):
    return 0.0

  def getPolicy(self, state):
    return 'random'

  def update(self, state, action, nextState, reward):
    pass


################################################################################
# Exercise B - complete the ValueIterationAgent.

class ValueIterationAgent(Agent):

  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
    Your value iteration agent should take an mdp on
    construction, run the indicated number of iterations
    and then act according to the resulting policy.
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations

    # Exercise B: program value iteration here.
    raise ValueError("Exercise B code should replace this message.")

  def getValue(self, state):
    """
    Look up the value of the state (after the indicated
    number of value iteration passes).
    """
    # Exercise B: return the determined value for state
    raise ValueError("Exercise B code should replace this message.")

  def getQValue(self, state, action):
    """
    Look up the q-value of the state action pair
    (after the indicated number of value iteration
    passes).  Note that value iteration does not
    necessarily create this quantity and you may have
    to derive it on the fly.
    """
    # Exercise B: return the determined Q value state here (or compute it right here)
    raise ValueError("Exercise B code should replace this message.")

  def getPolicy(self, state):
    """
    Look up the policy's recommendation for the state
    using the mdp and the computed state values or Q values.
    """
    # Exercise B: return the best action here according to the Q or V values available
    raise ValueError("Exercise B code should replace this message.")

  def getAction(self, state):
    """
    Return the action recommended by the policy.
    """
    return self.getPolicy(state)


  def update(self, state, action, nextState, reward):
    """
    Not used for value iteration agents!
    """
    pass

################################################################################
# Policy iteration
# Exercise C - implement a policy iteration class here (similar to Value iteration)
