from mesa import Agent

class InternshipScraperAgent(Agent):
    """Agent responsible for scraping internship opportunities."""
    def __init__(self, model):
        super().__init__(model)
        
    def step(self):
        # TODO: Implement scraping logic for internships
        # 1. Fetch data from source
        # 2. Parse data
        # 3. Save to data/ directory as JSON
        # 4. Insert into database
        pass
