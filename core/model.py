#!/usr/bin/python
# -*- coding: utf-8 -*-

import observable as obs
import timehelper
import togglapi.api as togglapi
import itertools

class PercentileFeedback(object):
    def __init__(self, config):
        self.percentage = obs.Observable('0.00 %')
        # full data is the raw toggl data since START_DATA
        self.full_data = obs.Observable(None)
        # plot data is the seconds worked each day
        self.plot_data = obs.Observable(None)
        # not sure if passing the config like this is ideal. If you read this and have wisdom to share, I’d be glad.
        self.t = timehelper.TimeHelper(config)
        self.a = togglapi.TogglAPI(config.API_TOKEN, config.TIMEZONE);
        self.config = config


    # this is triggered by the Refresh button
    def refresh_percentile(self):
        """Recalculate the percentile with respect to your efficiency on past days"""
        # extract the relevant data (if it’s 10AM, the time spent working before 10AM) from the toggl data
        self.refresh_full_data()
        full_data = self.full_data.get()
        processed_entries = self._extract_relevant_data(full_data)
        durations = self._secs_each_day(processed_entries)

        # the last entry of durations is the seconds worked today
        duration_today = durations.pop()

        # calculate percentile
        print('Past durations:')
        print(durations)
        print('Duration today:')
        print(duration_today)
        num_total = len(durations)
        num_lower = len([d for d in durations if d < duration_today])
        percentile = float(num_lower)/num_total*100
        # percentage has a callback which updates the tkEntry widget
    	self.percentage.set('{0:.2f} %'.format(percentile))


    # this is triggered by the Plot button
    def refresh_plot_data(self):
        """Returns the seconds worked for each day in the past, including today"""
        # extract the relevant data (if it’s 10AM, the time spent working before 10AM) from the toggl data
        self.refresh_full_data()
        full_data = self.full_data.get()
        processed_entries = self._extract_relevant_data(full_data)
        durations = self._secs_each_day(processed_entries, full_day=True)

        self.plot_data.set(durations)


    def refresh_full_data(self):
        """This is called to make sure full_data contains the toggl data"""
        self.full_data.set(self.a.get_time_entries(start_date=self.config.START_DATA, end_date=self.t.now.isoformat()))


    def _extract_relevant_data(self, time_entries):
        """From the raw time entries, returns a new list with description, start, stop, duration and day in a different format"""
        
        # Weed out time entries without the relevant tag and converts time strings to datetime objects
        processed_entries = []
        for entry in time_entries:
            if self.config.FILTER_TAG in entry['tags']:
                # create datetime objects from the start and stop keys in the dict
                start = self.t.to_datetime(entry['start'])
                stop = self.t.to_datetime(entry['stop'])
                duration = entry['duration']
                day = self.t.which_day_is(start)
                desc = entry['description']
                new_entry = {'description' : desc, 'dtstart' : start, 'dtstop' : stop, 'duration' : duration, 'day' : day}
                processed_entries.append(new_entry)
        return processed_entries


    def _secs_each_day(self, entries, full_day=False):
        """Calculates how many seconds you’ve worked each day, from the preprocessed toggl data"""
        # group all the entries on the same day
        groups = []
        for k, g in itertools.groupby(entries, lambda entry : entry['day']):
            groups.append(list(g))    # Store group iterator as a list

        # we only want the time we’ve worked in the time before
        # now for each day, add up all the entries for which end < now
        time_right_now = self.t.now.time()
        # durations contains the total seconds worked until the current time for each day
        durations = []
        for entry_list in groups:
            secs = 0
            for entry in entry_list:
                # in the future, also include tasks from past days that were still running at the time
                # with the correct duration (currently they’re counted full if they started before time_right_now)
                if full_day or self._starts_before(entry, time_right_now, self.t.this_morning.time()):
                    # if there is a time entry running right now (on the last day of groups)
                    # calculate its current duration
                    duration = entry['duration']
                    if duration < 0:
                        duration = duration + + self.t.secs_since_epoch
                    secs = secs + duration
            durations.append(secs)
        return durations


    def _starts_before(self, entry, time, rollover_time):
        """Checks if an entry stopped before a given time"""
        # we can’t simply do entry['dtstop'].time() < time_right_now
        # because that would also be true for tasks stopping at 1AM
        if time < rollover_time:
            # count all entries where entry.hour > 8 or entry.hour < time.hour
            if entry['dtstop'].time() > rollover_time or entry['dtstop'].time() < time:
                return True
        else:
            # count all entries between 8 and time.hour
            if rollover_time < entry['dtstart'].time() < time:
                return True
        return False