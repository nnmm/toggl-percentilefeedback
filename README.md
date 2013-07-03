toggl-percentilefeedback
========================

This is an implementation of percentile feedback (described here: http://blog.sethroberts.net/2011/05/01/percentile-feedback-and-productivity/). It’s far from polished.

## How does it work? ##
If you don’t know what percentile feedback means, take a look at the blog post linked above.

The **basic idea** is this: You log your time in [toggl](https://www.toggl.com), and tag those entries you consider work with "work" or something else. My application looks at the things you logged and calculates a **percentile score** for you. So, what does "percentile score" mean? Let’s say it’s Thursday and you’ve been tracking your time since Monday. At 2pm, you’ve been working for 5 hours, Monday-you had been working for 4.5 hours at that time, and Tuesday-you 4 hours, but Wednesday-you has managed 6 hours. Since you’re better than two out of three past-yous, that would get you a percentile score of 66 %. Also, you can plot your **efficiency** – that is, the % of time you have spent working in relation to the time you had available – for every day. Hopefully, looking at the graph and the percentile score motivates you to **work more**. Hooray!

Details:
At the moment, "the time you have available" simply means the time since 8am (or 7am or 10am, it’s configurable). So if it’s 11am and you’ve worked two hours, your efficiency is 66 %. The graph doesn’t take into account what time it is.

## How can I use toggl-percentilefeedback? ##
I’m running Python 2.7.3 32 bit on Windows, but I think it should work with other versions, too. You need to have the `requests` library installed. If you have pip, it should be `pip install requests`, otherwise download and unpack the source from [here](https://pypi.python.org/pypi/requests). In the directory, run `setup.py build` and `setup.py install`. At least that’s how I think I did it. Now for the easy part:
* Download and unpack toggl-percentilefeedback
* Rename config.py-example to config.py and replace the dummy API token with yours (you can find it in your [toggl profile](https://www.toggl.com/user/edit))
* Run main.py

## Issues ##
There are still a few things to do:
* Time zones are not fully implemented yet (see line 36 in timehelper.py)
* X and y axes need to be labeled with day and efficiency, respectively
* It might be good to seperate the time at which you wake up and the time at which a new day begins
* Better handling of time entries in the past that start before and end after the current time (see line 99 in model.py)

## Questions and comments ##
I appreciate any comments, including comments on my English here and suggestions for improving the structure of the program. Contact me for any questions you might have.

Thanks to [Mosab Ahmad](https://github.com/mos3abof) for his api.py file.
