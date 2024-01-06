# Comprehensive News Synthesis

## Background
This project was conceived as a personal project to help me grow and demonstrate my 
development skills. The basic idea is to create a web application that allows users to get a
comprehensive view of current events and topics through the aggregation and synthesis of multiple
sources.

## Purpose

The philosophy behind the project is that if people can see information from sources across the 
political spectrum, it will help them cut through what is noise and fluff and parse out what the relevant 
information is. Current news content at some level eventually appeals to authority, or relies on trust in a specific 
source. This site would relax the need for trust in specific sources, and instead of appealing to one authority, rely 
on the collective knowledge of them all.

Several news sources today often employ specific rhetoric to force a specific point of view, or prescribe how 
consumers should feel about information. This often happens immediately, with headlines attempting to stir a specific 
emotion in the reader. Unfortunately, this makes sense from a content perspective. Getting readers to emotionally 
connect with content is a great way to get them, and keep them, engaged. This strategy has proven effective. A 
consequence of this strategy, is that people are not given the space to form their own opinions, instead absorbing the
viewpoint of the source.

The responsibility placed on individuals to be good consumers of information is greater than ever before in human 
history. We are awash in so much information, so many opinions, that it is difficult to apply the diligence and 
skepticism this information ecosystem requires. I believe that people need tools to help them be responsible consumers 
of information. This site will attempt to be just that. If we can reduce the cognitive burden required to consume 
information responsibly, we can help them take a step in the right direction. For example, instead of needing to seek 
out multiple sources, and then determine what through-lines they all share, they can go to one source that already does 
this. This reduces the number of actions consumers need to take to reach the same outcome.

The purpose of the site is to provide a place for people to see news that has been aggregated, determine their own
aggregation strategies, and offer them opportunities to view opinions that differ from their own. The overall goal
is to leverage the law of averages to provide news content that contains only the connective tissue between sources.
This new synthesized information should contain the truth of the matter, with the spin of specific sources being washed
away by the aggregation.

Ideally the site can serve as a starting point for people who are interested in keeping up with current events, 
providing a comprehensive view of things, and serve as a launching point for more detailed exploration from specific 
sources.

## Target Audience

The target audience for this site is people interested in staying informed on current events, without the spin or 
prescriptive opinions that specific sources often apply. The user this site is most likely to connect with, is one that 
recognizes the need for responsible information consumption, and wants a way more easily bear that responsibility. The 
users the site would be most beneficial for, but may be harder to penetrate, are those that don't yet understand that 
by only consuming one or two sources, they are at risk of being lead in a specific direction.

## Value Proposition

### consensus 

Navigating the massive information ecosystem we live in now is a daunting task. Consuming news from only one source 
can leave you missing a critical piece of information or perspective. We need to be able to see the whole picture to 
inform our opinions. Consensus helps as do just that by drawing in information from varied sources, distilling the 
critical information from each, synthesizing that information, and offering a comprehensive view of the matter.

### logos

News, like most content driven industries, often relies on pathos, or emotional appeals to engage users. Content 
algorithms have learned that making users feel certain emotions increases the engagement on their platforms. Logos sets out 
to protect you from these emotionally appealing arguments, by distilling the actual information out of content, and 
presenting you with only that.

## Metrics

### Conversion

Conversion for the site will be measured by the number of users that sign up for the membership experience. These users 
will be offered unlimited access to site content, and offered a newsletter. Unsubscribed members will be offered only a 
few articles a month, similar to how other news sources operate.

## Features

### Data Source Selection

I want to allow users to select the sources that their synthesized news comes from. 

### Synthesizing Model Selection

I want to offer users the ability to select which model actually consumes their sources and produces the synthesized 
output.

### Bias and Reliability Scoring

The site should provide both a simple-to-understand score for bias and reliability based on source selection, and a 
comprehensive breakdown if they wish.

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

