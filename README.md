Turkish Newspaper Parsers
===

Although there are wonderful libraries to collect and parse newspaper articles, such as https://github.com/fhamborg/news-please and https://github.com/codelucas/newspaper, I realized that parsing certain Turkish newspapers can be problematic. In particular, extracting dates is most of the time problematic. Even when the dates were extracted, there were issues whenever the newspaper published dates in dd/mm/yyyy format. I also realized that parsing the main text when it was short can also be problematic.


That is why I wrote custom parsers to fix specific problems whenever these libraries do not work. Each script deals with a particular newspaper: it collects URLs either using the newspaper's daily archive or search function, parses them, and saves them in a spreadsheet. 

