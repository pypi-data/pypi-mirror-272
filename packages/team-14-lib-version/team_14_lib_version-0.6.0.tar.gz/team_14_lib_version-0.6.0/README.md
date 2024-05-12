# lib-version
A version-aware library consumed by the URL fishing detection application service
The library parses the version from the metadata in the package.

Uses semantic versioning `vMAJOR.MINOR.PATCH`

Automatic Bumping on Github: If no #major, #minor or #patch tag is contained in the merge commit message, 
it will bump whichever DEFAULT_BUMP is set to (which is minor by default). Right now it increments the minor version with each PR.

# usage

In the file you want to use this in, do `from libversion import VersionUtil`.
Then you can call `VersionUtil.VersionUtil.get_version()` to get the library version.