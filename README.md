# DancingLines
A scheme that captures and quantitatively analyzes event popularities between pairwise text media.

Weiming Bao, Boyuan Kong, Tianxiang Gao, Xiaofeng Gao, Yan Tang, Xuan Li and Guihai Chen. *DancingLines: An Analytical Scheme to Depict Cross-Platform
Event Popularity*. (under review)

## Summary
Nowadays, online events usually burst and are propagated through multiple modern media like social networks and search engines.
While there exist various researches discussing the event dissemination trends on individual platforms, few studies focus on event popularity analysis from a cross-platform perspective. 
Challenges come from the vast diversity of events and media platforms, especially the structurally, syntactically and semantically different user generated data.

In this paper, we design DancingLines, a novel and universal scheme that captures and quantitatively analyzes event popularities between pairwise text media. 
It contains two models: 
TF-SW, a semantic-aware popularity quantification model based on an integrated weight coefficient leveraging Word2Vec and TextRank with an embedded contributiveword selection process; 
and wDTW-CD, a paired time series alignment model matching different event phases adapted from Dynamic Time Warping, with four metrics proposed to provide insights on interpreting event popularity trends.

Experimental results on eighteen real-world event datasets from an influential social network and a popular search engine validate the effectiveness and applicability of our scheme. 
DancingLines is demonstrated to possess broad application potentials for discovering knowledge of various aspects related to events and platforms.