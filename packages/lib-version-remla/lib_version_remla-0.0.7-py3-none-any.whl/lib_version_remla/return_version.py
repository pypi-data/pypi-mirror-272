from importlib.metadata import version, PackageNotFoundError

class VersionUtil:
    @staticmethod
    def get_version():
        try:
            return version(__name__)
        except PackageNotFoundError:
            return version