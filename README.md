# CS7319 Homework 2
_Architecture Comparisons_ - Homework #2 for CS 7319 Software Architecture
Author: Blaine Harris
SMU - Spring 2025

## TODOs
[ ] Brief description of your Part A architecture, language, and how to 
build/run.
[ ] Capture screenshots of Part A executing.
[ ] Brief description of your Part B architecture, explaining where Map, 
Shuffle, and Reduce occur.
[ ] Capture screenshots of Part B executing.
[ ] Compile responses into a word doc to submit
[ ] Review and revise homework questions below.
[ ] Work on HW 2 Bonus [Natural Lanuage Processing](instruction/CS_7319_HW2_Bonus.pdf)

## Part A: [Single-Program Architecture](src_single/sentiment_analysis.py)
I still used a "map" architecture where I attributed values to enums.  
This is "modular" but would need some refacotring to match the map reduce
architecture.

## Part B: [MapReduce-Style Architecture](src_mapreduce/sentiment_mapreduce_complete.ipynb)
Jupyter notebook created from `sentiment_mapreduce_starter.ipynb`, which 
completes all TODOs.  
[_Jupyter Notebook Reference_](instruction/Jupyter_Notebook_Setup_Guide.pdf)

# [Homework Questions:](instruction/CS_7319_HW2_Sentiment_Analysis_2_Arch.pdf)
_Keep responses within 0.5 to 1 page(s)._
1. Structure & responsibilities (mapper vs single pass)
    - Since I used enums for my "single pass" function I ended up using some
    similar traits to the mapper. However, my single pass is still structure
    around a single post file import and would require refactoring or potential
    external infrastucture to support multiple posts.  The architecture of my 
    implementation was primarily focused around my current expierence and how
    we structure python programs for use in automated testing infrastructure.
    - The way my single pass was authored should allow for a simple rework that
    would also include the "reduction" aspect of this pattern so that all data
    sets are immediately stored into a single dictionary to capture the rolling
    sum.
2. Complexity (which code is simpler? easier to evolve?) 
    - I tried to author my single use code to be maintainable and modular, and
    in small cases is easier to use. The map reduce may add some complexity, but
    is in trade off for scalability.
3. Scalability & performance (how would each handle 100,000 × data?)
    - The map reduce pattern allows for aspects of the operation (i.e. mapping, 
    evaluating the text, creating summing sentiment values, etc.) to be shared 
    across multiple processes. While not currently implemented here, these could
    be split into differnet applications that can run across multiple processes. 