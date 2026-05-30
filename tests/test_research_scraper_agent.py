from mesa import Model
from agents.research_scraper_agent import ResearchScraperAgent

class DummyModel(Model):
    def __init__(self):
        super().__init__()

def test_research_scraper_agent_init():
    model = DummyModel()
    agent = ResearchScraperAgent(model)
    assert agent.model == model
