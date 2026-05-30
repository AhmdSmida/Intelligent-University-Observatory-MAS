import sqlite3
import logging
from typing import List, Dict, Any

from mesa import Agent

# Machine Learning & NLP Imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
import spacy

class AgentClassifier(Agent):
    """
    AgentClassifier uses NLP and Machine Learning to automatically categorize
    opportunities and extract relevant keyword tags from their descriptions.
    """

    def __init__(self, model):
        super().__init__(model)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # We use a scikit-learn Pipeline which chains the Vectorizer and the Classifier.
        #
        # === What is TF-IDF and why do we use it? ===
        # TF-IDF stands for Term Frequency-Inverse Document Frequency.
        # It converts raw text descriptions into numerical vectors that our ML model can understand.
        #
        # - Term Frequency (TF): Counts how often a word appears in a specific description.
        # - Inverse Document Frequency (IDF): Penalizes common words (like "the", "and", "is") 
        #   that appear across ALL descriptions, while boosting rare, domain-specific words 
        #   (like "quantum", "scholarship", "postdoc").
        #
        # By using TF-IDF, the ML model ignores generic fluff and focuses only on the most 
        # distinguishing vocabulary to make highly accurate classification decisions.
        # ============================================
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english')),
            ('clf', MultinomialNB())
        ])
        
        # Try loading spaCy model for Named Entity Recognition and POS Tagging
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            self.logger.warning("spaCy 'en_core_web_sm' model not loaded. Run 'python -m spacy download en_core_web_sm'.")
            self.nlp = None

        self.is_trained = False

    def train(self):
        """
        Trains the TF-IDF Vectorizer and Naive Bayes classifier on 30 mock samples.
        Prints a confusion matrix after training.
        """
        # 30 Mock Samples covering 6 categories
        samples = [
            # Internship (5)
            ("Summer software engineering intern required. Must know Python.", "internship"),
            ("Marketing internship for a fast-growing tech startup. Paid position.", "internship"),
            ("Data science intern to work on predictive models.", "internship"),
            ("Looking for a product design intern with UI/UX portfolio.", "internship"),
            ("Hardware engineering internship focusing on microcontrollers.", "internship"),
            
            # Scholarship (5)
            ("Full-tuition scholarship for international students in STEM.", "scholarship"),
            ("Merit-based scholarship for undergraduate minority students.", "scholarship"),
            ("Funding grant and scholarship for climate change research.", "scholarship"),
            ("Financial aid scholarship for developing nations.", "scholarship"),
            ("Excellence scholarship covering living expenses and tuition.", "scholarship"),
            
            # Certification (5)
            ("Free machine learning certification course by top university.", "certification"),
            ("Cloud architecture professional certificate. Learn AWS.", "certification"),
            ("Agile project management certification. Scrum master prep.", "certification"),
            ("Data analytics certificate focusing on SQL and Tableau.", "certification"),
            ("Cybersecurity basics certification. No prior experience needed.", "certification"),
            
            # Research Project (5)
            ("PhD position for research project in quantum computing.", "research_project"),
            ("Research assistant needed for bioinformatics sequence analysis.", "research_project"),
            ("Horizon Europe funded research project on green energy grids.", "research_project"),
            ("Seeking researchers for deep learning applications in healthcare.", "research_project"),
            ("Marie Curie fellowship research project on smart materials.", "research_project"),
            
            # Postdoc (5)
            ("Postdoc fellowship in theoretical physics and string theory.", "postdoc"),
            ("Postdoctoral researcher position in neuroscience lab.", "postdoc"),
            ("Funded postdoc role investigating AI ethics.", "postdoc"),
            ("Postdoctoral scholar needed for materials science department.", "postdoc"),
            ("Postdoc opportunity in robotics and computer vision.", "postdoc"),
            
            # Webinar (5)
            ("Join our free webinar on the future of AI in education.", "webinar"),
            ("Online webinar discussing scholarship application strategies.", "webinar"),
            ("Interactive webinar on cracking the software engineering interview.", "webinar"),
            ("Webinar: How to transition from academia to industry.", "webinar"),
            ("Live webinar Q&A with top tier tech recruiters.", "webinar"),
        ]
        
        X_train = [text for text, label in samples]
        y_train = [label for text, label in samples]
        
        self.logger.info("Training text classification pipeline on 30 labeled samples...")
        self.pipeline.fit(X_train, y_train)
        self.is_trained = True
        
        # Generate Confusion Matrix on the training data
        y_pred = self.pipeline.predict(X_train)
        cm = confusion_matrix(y_train, y_pred, labels=self.pipeline.classes_)
        
        print("\n=== Confusion Matrix (Training Data) ===")
        # Format the header
        header = f"{'':>18}" + "".join([f"{c[:5]:>8}" for c in self.pipeline.classes_])
        print(header)
        # Format the rows
        for i, row in enumerate(cm):
            row_str = "".join([f"{val:>8}" for val in row])
            print(f"{self.pipeline.classes_[i]:>18}{row_str}")
        print("========================================\n")

    def extract_tags(self, text: str) -> str:
        """
        Uses spaCy NER and POS tagging to extract useful keywords (nouns/entities).
        """
        if not self.nlp:
            return ""
            
        doc = self.nlp(text)
        tags = set()
        
        # Extract named entities (like organizations, products, geographics)
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT", "GPE", "NORP", "FAC"]:
                tags.add(ent.text.lower())
                
        # Extract important nouns
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and len(token.text) > 2:
                tags.add(token.text.lower())
                
        # Return top 10 unique tags as a comma separated string
        return ", ".join(list(tags)[:10])

    def step(self):
        """
        1. Load unclassified opportunities.
        2. Classify them.
        3. Extract tags.
        4. Save back to DB.
        """
        if not self.is_trained:
            self.train()
            
        # Dynamically fetch DB path from the global config
        db_path = self.model.config.get("DB_PATH", "db/observatory.db")
        
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # 1. Load all unclassified opportunities
                cursor.execute("SELECT id, description FROM Opportunities WHERE classified = 0 OR classified IS NULL")
                rows = cursor.fetchall()
                
                if not rows:
                    self.logger.info("No unclassified opportunities found.")
                    return
                    
                updates = []
                for opp_id, description in rows:
                    # Provide a fallback for empty descriptions
                    safe_desc = description if description else "Unknown Opportunity"
                        
                    # 2 & 3. Predict the category label using the trained ML Pipeline
                    category = self.pipeline.predict([safe_desc])[0]
                    
                    # 4. Extract keyword tags using spaCy
                    tags = self.extract_tags(safe_desc)
                    
                    updates.append((category, tags, 1, opp_id))
                    
                # 5. Save category + tags back to DB
                cursor.executemany('''
                    UPDATE Opportunities 
                    SET category = ?, tags = ?, classified = ?
                    WHERE id = ?
                ''', updates)
                
                conn.commit()
                self.logger.info(f"Successfully classified and tagged {len(updates)} opportunities.")
                
        except Exception as e:
            self.logger.error(f"Error during classification step: {e}")
