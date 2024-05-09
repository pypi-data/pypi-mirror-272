from importlib.metadata import version, PackageNotFoundError

version = "0.0.1"

class VersionUtil:
    def get_version():
        try:
            return version('lib_version_remla')
        except PackageNotFoundError:
            return version