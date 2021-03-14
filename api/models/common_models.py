from dataclasses import dataclass


@dataclass
class FileWithPath:
    fileName: str
    filePath: str


@dataclass
class AuthResponse:
    message: str
