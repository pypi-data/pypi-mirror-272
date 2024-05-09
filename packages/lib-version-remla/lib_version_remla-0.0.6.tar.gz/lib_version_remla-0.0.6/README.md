# lib-version
This is a package that returns the version of itself. 

### Building the package locally
1. ```poetry install```
2. ```poetry shell```
3. ```poetry build```
<!-- 3. ```python3 -m build```
To upload to PyPi you need to have access to the API key, which is stored in the team channel -->
<!-- 4. ```python3 -m twine upload --repository pypi dist/*```  -->

### Importing the package
1. Install with: ```pip install --index-url https://pypi.org/project/ --no-deps lib-version-remla```