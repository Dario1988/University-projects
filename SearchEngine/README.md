Building a Search Engine up!

Many techniques have been used for this project, but before getting inside the core of this work, I'm gonna explain a bit what kind of data I worked with and how I proceeded.


A precisation:
I didn't work alone. All the code you'll see has been developped by me in collaboration with other two collegues.

Let's start.


We grabbed the data (87000 songs) from the AZLyrics website, making the web scraping. Once made this, we cleaned up the data through tokenization and stamming and we allocated them into MongoDB.


Then, we focused on some statistics before starting to create our search engine.


To create the S.E. we used the *INVERTED INDEX* technique in addition to *COSINE SIMILARITY* and *TF-IDF*.

Eventually, once our query has been forwarded, we built clusters in according to the results obtained from the S.E.
