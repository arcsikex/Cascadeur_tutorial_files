## Full video about the workflow:
[![Watch the video](https://img.youtube.com/vi/*VIDEO-ID*/default.jpg)](https://youtu.be/*VIDEO-ID*)

## Setup Instructions

1. **Install Face_Landmark_Link**  
   Download it from the official repository: [Face_Landmark_Link v0.2](https://github.com/Qaanaaq/Face_Landmark_Link/releases/tag/v0.2).  
   _(I am not affiliated with this project.)_

2. **Install Python**  
   Get the latest version from the [official Python website](https://www.python.org/downloads/).

3. **Install the `scipy` module for Cascadeur**  
   Run the following command in your terminal (as admin):

   ```bash
   pip install --target="C:\Program Files\Cascadeur\python\Lib\site-packages" --python-version=3.11.0 --only-binary=:all: scipy
   ```

- Replace --target with your actual installation path if Cascadeur is installed elsewhere.
- (After this, you won't need Python anymore, so feel free to uninstall it.)
4. Download the import_facial_mocap.py file
Copy it from this repository to your ```Cascadeur\resources\scripts\python\commands``` folder.

