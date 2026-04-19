from services.base_service import BaseService
import json
import os

class PackagingService(BaseService):
    def run(self, output_path: str, analysis: dict, complexity: dict, flagged_scenes: dict) -> None:
        print("[PackagingService] Starting packaging...")
        self._drm_wrap(output_path)
        self._build_manifest(output_path, analysis, complexity, flagged_scenes)
        print("[PackagingService] Packaging done.")

    def _drm_wrap(self, output_path: str) -> None:
        print("[PackagingService] DRM encryption applied (stub).")

    def _build_manifest(self, output_path: str, analysis: dict, complexity: dict, flagged_scenes: dict) -> None:
        scene_analysis = {
        "complexity": complexity,
        "scenes": analysis.get("scenes", []),
        }

        scene_analysis_path = os.path.join(output_path, "metadata", "scene_analysis.json")
        with open(scene_analysis_path, "w") as f:
            json.dump(scene_analysis, f, indent=4)
        print(f"[PackagingService] Scene analysis saved: {scene_analysis_path}")
        
        manifest = {
            "version": "1.0",
            "analysis": analysis,
            "complexity": complexity,
            "flagged_scenes": flagged_scenes,
            "assets": {
                "video": {
                    "h264": [
                        "video/h264/4k_h264.mp4",
                        "video/h264/1080p_h264.mp4",
                        "video/h264/720p_h264.mp4",
                    ],
                    "vp9": [
                        "video/vp9/4k_vp9.webm",
                        "video/vp9/1080p_vp9.webm",
                        "video/vp9/720p_vp9.webm",
                    ],
                    "hevc": [
                        "video/hevc/4k_hevc.mkv",
                        "video/hevc/1080p_hevc.mkv",
                        "video/hevc/720p_hevc.mkv",
                    ],
                },
                "images": {
                    "sprite_map": "images/sprite_map.jpg",
                    "thumbnails": "images/thumbnails/",
                },
                "text": {
                    "source_transcript": "text/source_transcript.txt",
                    "ro_translation": "text/ro_translation.txt",
                },
                "audio": {
                    "ro_dub": "audio/ro_dub_synthetic.aac",
                },
                "metadata": {
                    "scene_analysis": "metadata/scene_analysis.json",
                },
            },
        }
        
        manifest_path = os.path.join(output_path, "metadata", "manifest.json")
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=4)
        print(f"[PackagingService] Manifest saved: {manifest_path}")