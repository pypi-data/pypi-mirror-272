from __future__ import annotations

from dataclasses import dataclass

from model.Agent import Agent
from model.Auth import Auth


@dataclass(kw_only=True, eq=False)
class ClientConfig:
    agent: Agent
    # The authentication configuration.
    auth: Auth
