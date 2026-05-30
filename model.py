import logging
from typing import Dict, Any

from mesa import Model, Agent
from mesa.datacollection import DataCollector
import random

# 1. Agent Imports
from agents.internship_scraper import InternshipScraper
from agents.scholarship_scraper import ScholarshipScraper
from agents.certification_scraper import CertificationScraper
from agents.project_scraper import ProjectScraper
from agents.classifier import AgentClassifier as Classifier
from agents.cluster_agent import AgentCluster as Cluster
from agents.relevance_matcher import AgentRelevanceMatcher as RelevanceMatcher
from agents.advisor import AgentAdvisor as Advisor
from agents.notification import AgentNotification as Notification

# Coordinator was not explicitly built yet, so we leave a stub for the architecture.
class Coordinator(Agent):
    def __init__(self, model):
        super().__init__(model)
    def step(self):
        pass



class ObservatoryModel(Model):
    """
    Intelligent University Observatory MAS Model
    Manages the lifecycle, scheduling, and data collection of all agents.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the ObservatoryModel.
        
        Design Decision (Config Dict): Passing a config dictionary allows us to decouple 
        the environment settings (like database paths, API keys, intervals) from the model logic.
        This makes the model highly reusable across different environments (testing, production).
        """
        super().__init__()
        self.config = config
        
        # Setup logging to fulfill the requirement of tracking which agents run
        self.logger = logging.getLogger("ObservatoryModel")
        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO)
            
        # Initialize tracked variables for DataCollector
        # Design Decision: We track these directly on the model instance so agents can 
        # easily increment them (e.g., self.model.opportunities_collected += 1)
        self.opportunities_collected = 0
        self.clusters_formed = 0
        self.recommendations_made = 0
        
        # Design Decision (Scheduler): We use a custom randomized list.
        # In Mesa 3.0+ RandomActivation was removed/refactored. By maintaining our own shuffled
        # list, we ensure fairness so no single agent always gets to write to the database first.
        self.my_agents = []
        self.steps = 0
        
        # Design Decision (Agent Registration): 
        # We instantiate exactly one of each structural agent because this MAS represents 
        # a pipeline of diverse, specialized microservices rather than a population of identical entities.
        agents_to_add = [
            InternshipScraper(self),
            ScholarshipScraper(self),
            CertificationScraper(self),
            ProjectScraper(self),
            Classifier(self),
            Cluster(self),
            RelevanceMatcher(self),
            Advisor(self),
            Notification(self),
            Coordinator(self)
        ]
        
        for agent in agents_to_add:
            self.my_agents.append(agent)
            
        # Design Decision (DataCollector): 
        # The DataCollector samples the model state at every step. This provides a time-series
        # history of the MAS performance which can be directly fed into the Streamlit dashboard 
        # to plot line charts of system activity over time.
        self.datacollector = DataCollector(
            model_reporters={
                "opportunities_collected": lambda m: m.opportunities_collected,
                "clusters_formed": lambda m: m.clusters_formed,
                "recommendations_made": lambda m: m.recommendations_made
            }
        )

    def step(self):
        """
        Advance the model by one step.
        """
        self.steps += 1
        step_num = self.steps
        self.logger.info(f"--- Starting Step {step_num} ---")
        
        # Design Decision (Logging agents): 
        # We log the agents present in the schedule before execution.
        agent_names = [agent.__class__.__name__ for agent in self.my_agents]
        self.logger.info(f"Agents running this step: {', '.join(agent_names)}")
        
        # Execute all scheduled agents in random order
        random.shuffle(self.my_agents)
        for agent in self.my_agents:
            agent.step()
        
        # Collect system metrics for this step
        self.datacollector.collect(self)
        
        self.logger.info(f"--- Completed Step {step_num} ---")
