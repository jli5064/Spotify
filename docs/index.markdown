---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
title: Spotfy Genre Community Detection
---
Recent work introduced the vast unfolding of communities in large networks, in which a heuristic methodology not only identifies communities, but also measures the density between nodes in modules that highlight the strength of a subcommunity. It was shown that such methodology can facilitate community detection, and exceed similar community detection algorithms in time complexity. In this paper, we will focus on deploying an algorithm on a real world dataset, specially the _CESNA_ (Communities from Edge Structure and Node Attributes) algorithm proposed by Jaewon Yang, Julian McAuley, and Jure Leskovec. While our quarter one project focuses only on the node connections in a network, we will account for node features using the _CESNA_ model to improve our prediction accuracy. 


## Introduction

Technological innovations during the past few decades, including the rise of computers, the internet, and social media, have accelerated the size and strength of data networks. When analyzing the data behind various data networks, communities form naturally within them through connections between individual points of data, or nodes. These communities are typically defined by a common variable such as physical location, political alignment, or interest in a public figure. However, as more individual nodes of data are added to the data collection, the number of connections between nodes and the number of communities formed to represent these connections grows exponentially, creating difficult problems to overcome when analyzing the data in a timely manner.

## Methods

To implement the _CESNA_ to our dataset, we had to identify the nodes and attributes we’d be using, and the type communities we expected to detect.  Additionally, we wanted to find a way to validate the communities did indeed have features in common, even though there is no ground truth to this dataset.  We started by deciding we would set our nodes to be artists with edges being a common playlist, our expectation being that nodes would organize themselves into communities of genres.  We can retrieve associated genres through Spotify’s API as a metric of accuracy to compare our closely related nodes to the intersection of genres in the community. We already have all we need to create the edges, but we need the other half of the _CESNA_ algorithm: the node attributes.  Using Spotify’s API we could search on artist names and return a dictionary of attributes defined by Spotify.  However, we ran into a problem: this process took several minutes just to get through 1,000 artists, and our dataset has 290,002 artists.

<center> <img src="img1.png"  width="60%" height="60%"> </center>

<details>
    <summary> This is a test dropdown </summary>
    <br>
    Could be python code here!
</details>

## Results

Results, including a D3 graph from generated JSON file (networkx)

Also will include our concluding thoughts in same section.

* * *

##### Appendix

 __[Community Detection in Networks with Node Attributes](https://cs.stanford.edu/people/jure/pubs/cesna-icdm13.pdf)__


##### Contributions


* * *
* * *
* * *
* * *

### Header 3

```python
# Python code with syntax highlighting.
if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
```


#### Header 4

*   This is an unordered list following a header.
*   This is an unordered list following a header.
*   This is an unordered list following a header.

##### Header 5

1.  This is an ordered list following a header.
2.  This is an ordered list following a header.
3.  This is an ordered list following a header.


| head1        | head two          | three |
|:-------------|:------------------|:------|
| ok           | good swedish fish | nice  |
| out of stock | good and plenty   | nice  |
| ok           | good `oreos`      | hmm   |
| ok           | good `zoute` drop | yumm  |

* * *

### Here is an unordered list:

*   Item foo
*   Item bar

### And an ordered list:

1.  Item one
1.  Item two
1.  Item three
1.  Item four

### And a nested list:

- level 1 item
  - level 2 item
  - level 2 item
    - level 3 item
    - level 3 item

### Small image

![Octocat](https://github.githubassets.com/images/icons/emoji/octocat.png)



### Definition lists can be used with HTML syntax.

<dl>
<dt>Name</dt>
<dd>Godzilla</dd>
<dt>Born</dt>
<dd>1952</dd>
<dt>Birthplace</dt>
<dd>Japan</dd>
<dt>Color</dt>
<dd>Green</dd>
</dl>
