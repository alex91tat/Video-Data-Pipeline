from enum import Enum

class PipelineState(Enum):
    IDLE = "idle"
    INGESTING = "ingesting"
    ANALYSING = "analysing"
    PROCESSING = "processing"
    PACKAGING = "packaging"
    DONE = "done"
    FAILED = "failed"


VALID_TRANSITIONS = {
    PipelineState.IDLE: [PipelineState.INGESTING],
    PipelineState.INGESTING: [PipelineState.ANALYSING, PipelineState.FAILED],
    PipelineState.ANALYSING: [PipelineState.PROCESSING, PipelineState.FAILED],
    PipelineState.PROCESSING: [PipelineState.PACKAGING, PipelineState.FAILED],
    PipelineState.PACKAGING: [PipelineState.DONE, PipelineState.FAILED],
    PipelineState.DONE: [],
    PipelineState.FAILED: [],
}