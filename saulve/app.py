import sys

from .challenges.base import Challenge, ChallengeLoader
from .errors import ChallengeNotFound, SaulveError
from .import_module import append_module_path, import_instance

__all__ = ['App', 'import_app']


class App:
    def __init__(self) -> None:
        self.loaders: dict[str, ChallengeLoader] = {}

    def register_challenge(
        self,
        challenge_id: str,
        loader: ChallengeLoader,
    ) -> None:
        """
        Raises:
            SaulveError: If a challenge is already registered with the given
                id.
        """
        if challenge_id in self.loaders:
            raise SaulveError(
                f"A challenge with id '{challenge_id} is already registered."
            )

        self.loaders[challenge_id] = loader

    def get_challenge(self, challenge_id: str) -> Challenge:
        """
        Raises:
            ChallengeNotFound: If no challenge with this id exist.
        """
        try:
            challenge = self.loaders[challenge_id]
        except KeyError as e:
            raise ChallengeNotFound(
                f"No challenge exists with id {challenge_id}"
            ) from e

        return challenge.load()


def import_app(app_module_name: str) -> App:
    """
    Raises:
        SaulveError: If the module has no 'app' attribute or the 'app'
            attribute is not an instance of the App class.
    """
    append_module_path(app_module_name, sys.path)
    return import_instance(app_module_name, 'app', App)
