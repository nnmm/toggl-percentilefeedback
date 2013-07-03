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

        # calculate the seconds worked today
        start_date = self.t.this_morning
        end_date = self.t.now
        entries = self.a.get_time_entries(start_date.isoformat(), end_date.isoformat())
        secs = self._count_seconds(entries)

        # calculate percentile
        print('Past durations:')
        print(durations)
        print('Duration today:')
        print(secs)
        num_total = len(durations)
        num_lower = len([d for d in durations if d < secs])
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

        # calculate the seconds worked today
        start_date = self.t.this_morning
        end_date = self.t.now
        entries = self.a.get_time_entries(start_date.isoformat(), end_date.isoformat())
        secs = self._count_seconds(entries)

        durations.append(secs)
        self.plot_data.set(durations)


    def refresh_full_data(self):
        """This is called to make sure full_data contains the toggl data"""
        if self.full_data.get() == None:
            self.full_data.set(self.a.get_time_entries(start_date=self.config.START_DATA, end_date=self.t.now.isoformat()))


    def _count_seconds(self, time_entries):
        """Calculates the total duration in seconds of all time entries with the correct tag"""
        # the negative durations are running time entries
        if time_entries == None:
            return 0
        seconds_tracked = [entry['duration'] for entry in time_entries if self.config.FILTER_TAG in entry['tags']]
        total_seconds_tracked = sum(x if x > 0 else x + self.t.secs_since_epoch for x in seconds_tracked)

        return total_seconds_tracked


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
                # in the future, maybe also count non-finished tasks
                if full_day or self._starts_before(entry, time_right_now, self.t.this_morning.time()):
                    secs = secs + entry['duration']
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


    def _extract_relevant_data(self, time_entries):
        """From the raw time entries, returns a new list with start, stop, duration and day in a different format"""
        
        # Weed out time entries without the relevant tag and converts time strings to datetime objects
        processed_entries = []
        for entry in time_entries:
            if self.config.FILTER_TAG in entry['tags']:
                # create datetime objects from the start and stop keys in the dict
                # important: time_entries must contain no running time entries, or there is no 'stop' key!
                start = self.t.to_datetime(entry['start'])
                stop = self.t.to_datetime(entry['stop'])
                duration = entry['duration']
                day = self.t.which_day_is(start)
                new_entry = {'dtstart' : start, 'dtstop' : stop, 'duration' : duration, 'day' : day}
                processed_entries.append(new_entry)
        return processed_entries