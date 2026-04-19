from services.base_service import BaseService
import subprocess
import json
import os

class ComplexityAnalysisService(BaseService):
    def run(self, file_path: str) -> dict:
        print("[ComplexityAnalysisService] Analysing scene complexity...")
        result = self._run_ffprobe(file_path)
        print("[ComplexityAnalysisService] Complexity analysis done.")
        return result


    def _run_ffprobe(self, file_path: str) -> dict:
        command = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            "-show_format",
            file_path
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"[ComplexityAnalysisService] ffprobe failed: {result.stderr}")
        data = json.loads(result.stdout)
        return self._extract_complexity(data)


    def _extract_complexity(self, data: dict) -> dict:
        video_stream = next(
            (s for s in data["streams"] if s["codec_type"] == "video"), None
        )

        if video_stream is None:
            raise RuntimeError("[ComplexityAnalysisService] No video stream found")
        
        return {
            "codec": video_stream.get("codec_name", "unknown"),
            "width": video_stream.get("width", 0),
            "height": video_stream.get("height", 0),
            "duration": float(data["format"].get("duration", 0)),
            "bit_rate": int(data["format"].get("bit_rate", 0)),
        }


    def _save_scene_analysis(self, result: dict, output_path: str) -> None:
        scene_analysis_path = os.path.join(output_path, "metadata", "scene_analysis.json")
        with open(scene_analysis_path, "w") as f:
            json.dump(result, f, indent=4)
        print(f"[ComplexityAnalysisService] Scene analysis saved: {scene_analysis_path}")