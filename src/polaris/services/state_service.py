from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class StateService:
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)

    def load(self, name: str) -> dict[str, Any]:
        """
        Load persisted plugin state.

        Returns an empty dictionary if no state exists.
        """

        file_path = self._get_path(name)

        if not file_path.exists():
            return {}

        try:
            with open(file_path, "r") as file:
                return json.load(file)

        except (json.JSONDecodeError, OSError):
            return {}

    def save(
        self,
        name: str,
        state: dict[str, Any],
    ) -> None:
        """
        Persist plugin state.
        """

        self.base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = self._get_path(name)

        with open(file_path, "w") as file:
            json.dump(
                state,
                file,
                indent=2,
            )

    def _get_path(self, name: str) -> Path:
        return self.base_path / f"{name}.json"
