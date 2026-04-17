from services.base_service import BaseService
import random

class AnalysisService(BaseService):
    def run(self, file_path: str) -> dict:
        print("[AnalysisService] Starting analysis...")
        return {
            "intro_end": self._detect_intro(),
            "credits_start": self._detect_credits(),
            "scenes": self._index_scenes(),
        }


    def _detect_intro(self) -> float:
        timestamp = round(random.uniform(60, 90), 2)
        print(f"[AnalysisService] Intro ends at: {timestamp}s")
        return timestamp


    def _detect_credits(self) -> float:
        timestamp = round(random.uniform(5400, 6000), 2)
        print(f"[AnalysisService] Credits start at: {timestamp}s")
        return timestamp


    def _index_scenes(self) -> list:
        scenes = [
            {"start": 0.0, "end": 120.0, "type": "establishing_shot"},
            {"start": 120.0, "end": 400.0, "type": "dialogue"},
            {"start": 400.0, "end": 600.0, "type": "action"},
        ]
        print(f"[AnalysisService] Indexed {len(scenes)} scenes")
        return scenes