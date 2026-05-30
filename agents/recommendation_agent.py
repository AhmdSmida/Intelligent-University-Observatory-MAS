from mesa import Agent

class RecommendationAgent(Agent):
    """Agent responsible for recommending opportunities to users based on their skills and interests."""
    def __init__(self, model):
        super().__init__(model)
        
    def step(self):
        # TODO: Implement recommendation logic
        pass
