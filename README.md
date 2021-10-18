Turkish Newspaper Parsers
===

Although there are wonderful libraries to collect and parse newspaper articles, such as https://github.com/fhamborg/news-please and https://github.com/codelucas/newspaper, I realized that parsing certain Turkish newspapers can be problematic. In particular, extracting dates is most of the time problematic. Even when the dates are extracted, there are issues whenever the newspaper publishes dates in dd/mm/yyyy format. I also realized that parsing main texts could fail in `news-please` and `newspaper3k` whenever the articles are relatively short.


That is why I wrote custom parsers to fix specific problems whenever these libraries do not work. Each script deals with a particular newspaper: it collects URLs either using the newspaper's daily archive or search function, parses them, and saves them in a spreadsheet. 


Sometimes, it is also impossible to use either `news-please` or `newspaper3k` since newspapers remove old articles from their servers. In those cases, we can access URLs archived by Wayback. I use Wayback's [CDX server API](https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md) to search for URLs for a specific newspaper within a defined time range.

I will add more newspapers as I find time (they are ready, but I need to clean them, and I am trying to finish my dissertation at the same time!), but feel free to reach out to me if you need help with a particular newspaper.