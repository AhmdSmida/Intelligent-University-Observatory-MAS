from mesa import Model
from agents.scholarship_scraper_agent import ScholarshipScraperAgent

class DummyModel(Model):
    def __init__(self):
        super().__init__()

def test_scholarship_scraper_agent_init():
    model = DummyModel()
    agent = ScholarshipScraperAgent(model)
    assert agent.model == model
