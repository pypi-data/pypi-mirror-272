from importlib.metadata import version, PackageNotFoundError
import lib_version_remla

class VersionUtil:
    @staticmethod
    def get_version():
        try:
            return version('lib_version_remla')
        except PackageNotFoundError:
            print('Package not found')