from mesa import Model
from agents.recommendation_agent import RecommendationAgent

class DummyModel(Model):
    def __init__(self):
        super().__init__()

def test_recommendation_agent_init():
    model = DummyModel()
    agent = RecommendationAgent(model)
    assert agent.model == model
