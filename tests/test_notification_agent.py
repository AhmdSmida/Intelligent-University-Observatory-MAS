from mesa import Model
from agents.notification_agent import NotificationAgent

class DummyModel(Model):
    def __init__(self):
        super().__init__()

def test_notification_agent_init():
    model = DummyModel()
    agent = NotificationAgent(model)
    assert agent.model == model
