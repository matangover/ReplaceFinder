# ReplaceFinder
Open [fman](https://fman.io/) when clicking "Show in Finder". Works only on macOS, obviously. ;)

Instructions:
1. Install the plugin: in the fman Command Palette (Cmd+Shift+P) choose `Install plugin` and then `ReplaceFinder`.
2. Activate the plugin: in the fman Command Palette choose `Replace Finder`.
3. Any app that has a "Show in Terminal" button should now open fman instead. Tested on Google Chrome and VS Code -- your kilometrage may vary. If the app was already open, restart it for the changes to take effect.

To deactivate the plugin, run the following command in your Terminal:
```
defaults delete -g NSFileViewer
```
