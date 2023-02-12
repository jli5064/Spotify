# DSC 180B [WI 23] Project 2:<br> Finding Artist Genres Through Playlist Data
*** Classifying Spotify Artists through Community Detection and Clustering ***

<!--This site was built using [GitHub Pages](https://pages.github.com/).-->
This data 
## Data Background
<!-- TODO -->
WIP

## Deployment

Clone the project

```bash
  git clone https://github.com/darehunt/DSC180A-Project2
```

After running Docker and logging into your account, launch the docker image:
<!-- TODO -->
```bash
  launch.sh -i jul016/dsc180b-proj2
```

From there, copy in the directory, change directories into the project and run commands from bash using run.py:

```bash
  cp DSC180A-Project2 .
  cd DSC180A-Project2
  python run.py test
```
## Commands

The build script can be run directly from bash `python run.py`

| Command | Description |
| --- | --- |
| `clean`  | Clears remnents of previous networks or communitiy detection  |
| `test-data`  | Generates and loads data network from test data  |
| `data`  | Downloads, extracts, and prepares data network from Kaggle dataset  |
| `cesna`  | Runs cesna community detection |
| `test`  | equivilent of running `test-data cesna` |
| `all`  | equivilent of running `data cesna`  |
<!--| `aicrowd`  | Downloads, extracts, and prepares data network from aicrowd Spotify dataset  |-->

## Authors

- [@darehunt](https://www.github.com/darehunt)
- [@anmokhta](https://www.github.com/anmokhta)
- [@Btran206](https://www.github.com/Btran206)
- [@jul016](https://www.github.com/jul016)

