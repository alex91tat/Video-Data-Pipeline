from services.base_service import BaseService
import random

class AnalysisService(BaseService):
    def run(self, file_path: str, duration: float) -> dict:
        print("[AnalysisService] Starting analysis...")
        return {
            "intro_end": self._detect_intro(duration),
            "credits_start": self._detect_credits(duration),
            "scenes": self._index_scenes(duration),
        }


    def _detect_intro(self, duration: float) -> float:
        timestamp = round(min(random.uniform(60, 90), duration * 0.1), 2)
        print(f"[AnalysisService] Intro ends at: {timestamp}s")
        return timestamp


    def _detect_credits(self, duration: float) -> float:
        timestamp = round(duration * random.uniform(0.85, 0.95), 2)
        print(f"[AnalysisService] Credits start at: {timestamp}s")
        return timestamp


    def _index_scenes(self, duration: float) -> list:
        segment = duration / 3
        scenes = [
            {"start": round(0.0, 2), "end": round(segment, 2), "type": "establishing_shot"},
            {"start": round(segment, 2), "end": round(segment * 2, 2), "type": "dialogue"},
            {"start": round(segment * 2, 2), "end": round(duration, 2), "type": "action"},
        ]
        print(f"[AnalysisService] Indexed {len(scenes)} scenes")
        return scenes