toggl-percentilefeedback
========================

This is an implementation of percentile feedback (described here: http://blog.sethroberts.net/2011/05/01/percentile-feedback-and-productivity/). It’s not really finished yet.

### How does it work? ###
If you don’t know what percentile feedback means, take a look at the blog post linked above.

The basic idea is this: You log your time in toggl, and tag those entries you consider work with "work" or something else. My application looks at the things you logged and calculates a percentile score for you. So, what does "percentile score" mean? Let’s say it’s Thursday and you’ve been tracking your time since Monday. At 2pm, you’ve been working for 5 hours, Monday-you had been working for 4.5 hours at that time, and Tuesday-you 4 hours, but Wednesday-you has managed 6 hours. Since you’re better than two out of three past-yous, that would get you a percentile score of 66 %. Also, you can plot your efficiency – that is, the % of time you have spent working in relation to the time you had available – for every day. Hopefully, looking at the graph and the percentile score motivates you to work more. Hooray!

Details:
At the moment, "the time you have available" simply means the time since 8am (or 7am or 10am, it’s configurable). So if it’s 11am and you’ve worked two hours, your efficiency is 66 %. The graph doesn’t take into account what time it is.

### Requirements ###
You need to have the requests library installed.

Thanks to [Mosab Ahmad](https://github.com/mos3abof) for his api.py file.
