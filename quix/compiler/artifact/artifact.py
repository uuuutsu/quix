from dataclasses import dataclass

from .code import ArtifactCode
from .header import ArtifactHeader


@dataclass
class Artifact:
    header: ArtifactHeader
    code: ArtifactCode
