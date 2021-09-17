Turkish Newspaper Parsers
===

Although there are wonderful libraries to collect and parse newspaper articles, such as https://github.com/fhamborg/news-please and https://github.com/codelucas/newspaper, I realized that parsing certain Turkish newspapers can be problematic. In particular, extracting dates is most of the time problematic. Even when the dates are extracted, there were issues whenever the newspaper publishes date in `dd/mm/yyyy` format. I also realized that extracting main text when it was short can also be problematic.

That is why, I wrote custom parsers to fix specific problems whenever these libraries do not work. 

