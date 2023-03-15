# DSC 180B [WI 23] Project 2:<br> Community Detection of Music Genres
*** Classifying Spotify Artists through Community Detection and Clustering ***

<!--This site was built using [GitHub Pages](https://pages.github.com/).-->
This data 
## Data Background
<!-- TODO -->
Our primary source of data is a dataset of Spotify playlists collected by Andrew Maranhão, which is freely available on Kaggle \href{https://www.kaggle.com/datasets/andrewmvd/spotify-playlists}{(link)}. This dataset was collected using a subset of users who published their #nowplaying tweets via Spotify. This tabular dataset lists a row for each song that was tweeted out, containing the name of the song, the artist of the song, and the playlist that song was playing from. While the data also contained the user IDs of each person who tweeted the track they were listening to, our model does not take personal information as input.

## Deployment

Clone the project

```bash
  git clone https://github.com/darehunt/DSC180B-Project2
```

After running Docker and logging into your account, pull and launch the docker image: (note that this requires more RAM than the usual to run)
```bash
  launch.sh -i anmokhta/DSC180B-proj2:latest -m 32
```

From there, copy in the directory, change directories into the project and run commands from bash using run.py:

```bash
  cp DSC180B-Project2 .
  cd DSC180B-Project2
  python run.py all
```
## Commands

The build script can be run directly from bash `python run.py`

| Command | Description |
| --- | --- |
| `clean`  | Clears reminents of previous networks or community detection  |
| `data`  | Downloads, extracts, and prepares data network from Kaggle dataset  |
| `model`  | Runs community detection to attempt to group artists by genre |
| `all`  | equivalent of running `data model`  |

## Authors

- [@darehunt](https://www.github.com/darehunt)
- [@anmokhta](https://www.github.com/anmokhta)
- [@Btran206](https://www.github.com/Btran206)
- [@jul016](https://www.github.com/jul016)

