from models.pipeline_state import PipelineState, VALID_TRANSITIONS
from services.ingest import IngestService
from services.analysis import AnalysisService
from services.complexity_analysis import ComplexityAnalysisService
from services.video_ecoding import VideoEncodingService
from services.timed_text import TimedTextService
from services.compliance import ComplianceService
from services.packaging import PackagingService
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

class Orchestrator:
    def __init__(self, file_path: str, output_path: str):
        self.file_path = file_path
        self.output_path = output_path
        self.state = PipelineState.IDLE

    def _transition(self, new_state: PipelineState) -> None:
        if new_state not in VALID_TRANSITIONS[self.state]:
            raise RuntimeError(f"Invalid transition: {self.state} -> {new_state}")
        print(f"[Orchestrator] State: {self.state.value} -> {new_state.value}")
        self.state = new_state
        

    def _create_output_folders(self) -> None:
        folders = [
            os.path.join(self.output_path, "video", "h264"),
            os.path.join(self.output_path, "video", "vp9"),
            os.path.join(self.output_path, "video", "hevc"),
            os.path.join(self.output_path, "images", "thumbnails"),
            os.path.join(self.output_path, "text"),
            os.path.join(self.output_path, "audio"),
            os.path.join(self.output_path, "metadata"),
        ]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
        print("[Orchestrator] Output folders created.")


    def run(self) -> None:
        try:
            # phase 1 - ingest
            self._transition(PipelineState.INGESTING)
            IngestService().run(self.file_path)

            # phase 2 - analysis
            self._transition(PipelineState.ANALYSING)
            self._create_output_folders()
            complexity = ComplexityAnalysisService().run(self.file_path)
            analysis = AnalysisService().run(self.file_path, complexity["duration"])

            # phase 3 - parallel processing
            self._transition(PipelineState.PROCESSING)
            flagged_scenes = self._run_parallel(analysis)

            # phase 4 - packaging
            self._transition(PipelineState.PACKAGING)
            PackagingService().run(self.output_path, analysis, complexity, flagged_scenes)

            self._transition(PipelineState.DONE)
            print("[Orchestrator] Pipeline completed successfully.")

        except Exception as e:
            self._transition(PipelineState.FAILED)
            print(f"[Orchestrator] Pipeline failed: {e}")


    def _run_parallel(self, analysis: dict) -> dict:
        flagged_scenes = {}
        scenes = analysis.get("scenes", [])

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(VideoEncodingService().run, self.file_path, self.output_path): "video",
                executor.submit(TimedTextService().run, self.output_path): "timed_text",
                executor.submit(ComplianceService().run, scenes): "compliance",
            }
            for future in as_completed(futures):
                service = futures[future]
                result = future.result()
                if service == "compliance":
                    flagged_scenes = result
                print(f"[Orchestrator] {service} completed.")

        return flagged_scenes