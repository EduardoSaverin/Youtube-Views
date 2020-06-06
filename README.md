# Youtube View Increaser ;)

A python based program who's job is to increase provided youtube urls video views.

### Prerequisite
* `Python >= 3.1`
* `Tor (with Password)`
* `Firefox >= 60`
* `Selenium Gecko Driver PATH being set`

### Setup
I would suggest you to create `python virtual env` for this project. Next clone this repo, go inside downloaded repo and run :

```shell
pip install -r requirements.txt
```

This will install all libraries being used in this repo. Next setup is to set tor password as environment variable. You will need to set your tor password in __TOR_PASSWORD__ env variable so that it can read by this program.

### Running
Command to run this has following syntax
> python main.py *number_of_views* *youtube_url*

Example :
```shell
python main.py 1 https://www.youtube.com/watch?v=WNeLUngb-Xg
```