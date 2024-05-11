from abc import ABC, abstractmethod


class Context(ABC):
    """
    Base class for a resource Context. Allows describing the resource's identifier for logging purposes.
    """

    @abstractmethod
    def get_context(self) -> dict:
        """
        Returns a dictionary containing the resource's identifier for logging purposes.
        """
