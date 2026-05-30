from mesa import Model
from agents.internship_scraper_agent import InternshipScraperAgent

class DummyModel(Model):
    def __init__(self):
        super().__init__()

def test_internship_scraper_agent_init():
    model = DummyModel()
    agent = InternshipScraperAgent(model)
    assert agent.model == model
