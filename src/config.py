from dataclasses import dataclass

@dataclass
class JobConfig:
    input_path: str
    output_path: str
    keyword_param: str = "q"
    coalesce_files: int = 1
