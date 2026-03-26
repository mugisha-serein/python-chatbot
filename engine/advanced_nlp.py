import logging
import os
from typing import Dict, List, Optional

try:
    from transformers import pipeline
except ImportError:  # pragma: no cover
    pipeline = None

import knowledge

logger = logging.getLogger(__name__)


class AdvancedNLPEngine:
    def __init__(self, model_name: Optional[str] = None, threshold: float = 0.55):
        self.model_name = model_name or os.environ.get("CHATBOT_NLP_MODEL", "typeform/distilbert-base-uncased-mnli")
        self.threshold = threshold
        self.labels = list(knowledge.INTENTS.keys())
        self.pipeline = self._build_pipeline()

    def _build_pipeline(self):
        if pipeline is None:
            logger.info("Transformers not available; skipping advanced NLP.")
            return None
        try:
            return pipeline("zero-shot-classification", model=self.model_name)
        except Exception as exc:
            logger.warning("Couldn't initialize advanced NLP pipeline (%s).", exc)
            return None

    def classify_intent(self, message: str) -> Optional[Dict[str, float]]:
        if self.pipeline is None:
            return None
        try:
            result = self.pipeline(message, candidate_labels=self.labels)
            top_label = result["labels"][0]
            score = result["scores"][0]
            return {"intent": top_label, "score": score}
        except Exception as exc:
            logger.debug("Advanced NLP classification failed: %s", exc)
            return None
