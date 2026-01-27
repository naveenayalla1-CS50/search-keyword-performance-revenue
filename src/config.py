# config.py
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)  # immutable → safer for configs
class JobConfig:
    """
    Configuration for the Search Keyword Performance Glue/PySpark job.
    
    Attributes:
        input_path: S3 path (or local file path) to the input TSV file
        output_path: S3 prefix or local directory where results will be written
        keyword_param: Default query parameter for keyword extraction (usually 'q')
        coalesce_files: Number of output files to write (1 = single file)
    """
    input_path: str
    output_path: str
    keyword_param: str = "q"           # default for Google/Bing
    coalesce_files: int = 1            # single file output (common for assessments)

    # Optional: 
    max_partitions: Optional[int] = None
    log_level: str = "INFO"

    def __post_init__(self):
        """Validate config after initialization."""
        if not self.input_path:
            raise ValueError("input_path is required")
        if not self.output_path:
            raise ValueError("output_path is required")
        if self.coalesce_files < 1:
            raise ValueError("coalesce_files must be >= 1")
        if self.keyword_param.strip() == "":
            raise ValueError("keyword_param cannot be empty")

    @classmethod
    def from_glue_args(cls, args: dict) -> "JobConfig":
        """
        Factory method: Create JobConfig from Glue job arguments (--key=value).
        """
        return cls(
            input_path=args.get("--INPUT_PATH", args.get("--input_path", "")),
            output_path=args.get("--OUTPUT_PATH", args.get("--output_path", "")),
            keyword_param=args.get("--KEYWORD_PARAM", args.get("--keyword_param", "q")),
            coalesce_files=int(args.get("--COALESCE_FILES", args.get("--coalesce_files", "1")))
        )

    def to_dict(self) -> dict:
        """Convert to dict for logging or debugging."""
        return {
            "input_path": self.input_path,
            "output_path": self.output_path,
            "keyword_param": self.keyword_param,
            "coalesce_files": self.coalesce_files,
        }
