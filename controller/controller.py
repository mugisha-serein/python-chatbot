import sys
from pathlib import Path
from typing import List, Optional

sys.path.append(str(Path(__file__).resolve().parents[1]))

from data import DataLayer
from service import ChatService


class ChatController:
    def __init__(self, data_layer: Optional[DataLayer] = None, service: Optional[ChatService] = None):
        self.data_layer = data_layer or DataLayer()
        self.service = service or ChatService(data_layer=self.data_layer)

    def send_user_message(self, message: str, session_id: Optional[str] = None) -> Optional[str]:
        cleaned = message.strip()
        if not cleaned:
            return None

        bot_response = self.service.process_message(cleaned, session_id=session_id)
        return bot_response

    def load_history(self, limit: Optional[int] = None) -> List[dict]:
        return self.data_layer.load_history(limit=limit)


# export
default_controller = ChatController()
