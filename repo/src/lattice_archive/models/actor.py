from dataclasses import dataclass


@dataclass(frozen=True)
class Actor:
    user_id: str
    workspace_id: str
    role: str
    display_name: str
