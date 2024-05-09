# Zacks
An unofficial package that extracts portfolio information from Zacks. The only current implementation is `experts_view()`

## Installation
First, make sure to install [geckodriver](https://github.com/mozilla/geckodriver/releases/tag/v0.34.0) for your OS. The default place Zacks will look is `$USER_HOME/chromedriver` but you can change where it points using the -c flag.

If Firefox is installed through snap, you need to use firefox.geckodriver by running
```bash
ln -s $(whereis firefox.geckodriver | awk '{print $2}') geckodriver
```
## Usage
```python
from zacks import experts_view

experts_view()
```