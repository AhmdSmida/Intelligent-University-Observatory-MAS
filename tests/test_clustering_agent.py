from mesa import Model
from agents.clustering_agent import ClusteringAgent

class DummyModel(Model):
    def __init__(self):
        super().__init__()

def test_clustering_agent_init():
    model = DummyModel()
    agent = ClusteringAgent(model)
    assert agent.model == model
