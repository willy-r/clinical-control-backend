from abc import ABC, abstractmethod
from typing import Any


class BaseUserRepository(ABC):  # pragma: no cover
    @abstractmethod
    def find_by_email(self, email: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def create_user(self, user: dict[str, Any]) -> dict[str, Any]:
        pass

    @abstractmethod
    def find_all(
        self, skip: int = 0, limit: int = 100
    ) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def find_by_id(user_id: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def update_user_by_id(
        self, user_id: str, user: dict[str, Any]
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    def delete_user_by_id(self, user_id: str) -> None:
        pass
