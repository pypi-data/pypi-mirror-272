# lib-version
This is a package that returns the version of itself. 

### Building the package locally
You need to have poetry installed before running this: ```pip install poetry```.
1. ```poetry install```
2. ```poetry shell```
3. ```poetry build```

#### Uploading to PyPi manually
This can be done after building the package locally. Please don't upload manually if not necessary, the GitHub workflow will take care of this. But if you need to do it manually, input this command. The API key is shared in the team channel.
1. ```python3 -m twine upload --repository pypi dist/*```  

### Updating the package via workflow
After pushing an update you can tag it with the following command to trigger the workflow.
1. ```git tag 0.0.1```, where 0.0.1 can be any version. This tags the latest commit. 
2. ```git push origin --tags ```

### Importing the package from PyPi
To use the package in your project you can install it from PyPi. 
PyPi link is: https://pypi.org/project/lib-version-remla/
1. Install with: ```pip install lib-version-remla```

### Using the functionality
```
from lib_version_remla import return_version
version = return_version.VersionUtil.get_version()
```