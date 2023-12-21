# Comprehensive News Synthesis

## Background
This project was conceived as a personal project to help me grow and demonstrate my 
development skills. The basic idea is to create a web application that allows users to get a
comprehensive view of current events and topics through the aggregation and synthesis of multiple
sources.

The philosophy behind the project is that if people can see information from sources across the 
political spectrum, it will help them cut through what is noise and fluff into what the relevant 
information is.

## Key Design Principles

### Transparency

I believe transparency to be the most important principle when creating this project. If I am going to 
ask people to step outside their information comfort zone, then I need to be very open about where I 
source my information, how I transform it, what models I am using, and how my algorithms work. I plan on 
creating documentation for each specific relevant piece, and of course you can see the source code here.

## Initial Project Scope
I plan on building this over about 6 months or so. I am without a doubt going to define a scope that
is far too large for that time-frame, but it will be fun to give it a shot.

Consider this readme as a work in progress, as I will use it for my notes.

Here is the user experience I am imagining. 

1) Users are presented a list of current events (topics).
    - This is a listing of aggregated and synthesized headlines.
2) They select a topic of interest and are presented with the sources that went into aggregation,
   and a synthesized article.

This seems like a good small first bite to take.

### Data Sources
I want to provide an exhaustive list that will allow people to see the different cross-sections of news
based on data like source, regional popularity, social media sentiment, demographic popularity, etc. I 
also want to provide users the ability to combine sources with different political alignments to help them
see the through-lines. I think for a first pass I will pick two sources; Fox News and CNN.

## Architecture
Right now I am thinking about creating a Flask microservice to handle web scraping, and another to handle
interaction with Weaviate.

