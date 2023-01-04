from importlib import import_module

from .challenges.base import Challenge, ChallengeLoader
from .errors import AOCError, ChallengeNotFound


__all__ = ['App', 'import_app']


class App:
    def __init__(self) -> None:
        self.loaders: dict[str, ChallengeLoader] = dict()

    def register_challenge(
        self,
        challenge_id: str,
        loader: ChallengeLoader,
    ) -> None:
        """
        Raises:
            AOCError: If a challenge is already registered with the given id.
        """
        if challenge_id in self.loaders:
            raise AOCError(
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
        except KeyError:
            raise ChallengeNotFound(
                f"No challenge exists with id {challenge_id}"
            )

        return challenge.load()


def import_app(app_module_name: str) -> App:
    """
    Raises:
        AOCError: If the module has no 'app' attribute or the 'app' attribute
            is not an instance of the App class.
    """
    app_module = import_module(app_module_name)

    if not hasattr(app_module, 'app'):
        raise AOCError(f"No 'app' found in {app_module_name}")

    app = app_module.app

    if not isinstance(app, App):
        raise AOCError(f"{app} is not an instance of {App.__class__}.")

    return app
