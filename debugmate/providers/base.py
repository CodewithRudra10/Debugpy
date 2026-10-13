
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AnalysisResult:
    error_type: str
    cause: str
    suggested_fix: str
    explanation: str


class AIProvider(ABC):
    @abstractmethod
    def analyze(
        self,
        error_type: str,
        error_message: str,
        source_code: str,
        instructions: str,
    ) -> AnalysisResult:
        """Analyze an error and return a structured diagnosis."""
        pass
