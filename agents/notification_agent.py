from mesa import Agent

class NotificationAgent(Agent):
    """Agent responsible for generating notifications for users when relevant opportunities are found."""
    def __init__(self, model):
        super().__init__(model)
        
    def step(self):
        # TODO: Implement notification logic
        pass
