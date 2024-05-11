# Manual process to update project

1. Update software, test
2. update version in pyproject.toml
3. build software: "python3 -m build"
4. upload new version: "python3 -m twine upload --repository pypi dist/*"

