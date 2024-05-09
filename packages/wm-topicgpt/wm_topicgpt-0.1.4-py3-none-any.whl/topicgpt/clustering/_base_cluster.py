import pandas as pd
from typing import List, Any
from dataclasses import dataclass, field


@dataclass
class Cluster:
    id: str = None
    parent_id: str = None
    children_id: str = field(default_factory=list)

    data: pd.DataFrame = None
    topic: str = None
    description: str = None
    summary: str = None
    keywords: str = None

    size: int = None
    percentage: float = None

    ranked_idx: List[int] = None