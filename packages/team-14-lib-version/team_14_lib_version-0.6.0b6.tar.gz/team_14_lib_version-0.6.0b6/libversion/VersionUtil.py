import importlib.metadata


class VersionUtil:
    @staticmethod
    def get_version(package_name="team_14_lib_version"):
        try:
            dist = importlib.metadata.distribution(package_name)
            return dist.version
        except importlib.metadata.PackageNotFoundError:
            return f"No package named '{package_name}' found."
