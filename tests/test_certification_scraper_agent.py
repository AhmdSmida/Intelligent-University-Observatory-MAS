from mesa import Model
from agents.certification_scraper_agent import CertificationScraperAgent

class DummyModel(Model):
    def __init__(self):
        super().__init__()

def test_certification_scraper_agent_init():
    model = DummyModel()
    agent = CertificationScraperAgent(model)
    assert agent.model == model
