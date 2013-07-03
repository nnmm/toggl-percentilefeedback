#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time

class TimeHelper(object):
	"""Time helper functions"""
	def __init__(self, config):
		self.timezone = config.TIMEZONE
		self.waketime = datetime.datetime.strptime(config.WAKE_TIME, "%H:%M:%S").time()
		self.bedtime = datetime.datetime.strptime(config.BED_TIME, "%H:%M:%S").time()

	@property
	def secs_since_epoch(self):
		return int(time.time())


	@property
	def now(self):
		return datetime.datetime.now()


	@property
	def this_morning(self):
		morning = datetime.datetime.combine(datetime.date.today(), self.waketime)
		if self.now < morning:
			morning = morning - datetime.timedelta(days=1)
		return morning


	def to_datetime(self, time_string):
		"""Converts a string containing a date and a time into a datetime object"""
		dtime = datetime.datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S+00:00")
		# TEMPORARY HACK
		return dtime + datetime.timedelta(hours=2)


	def last_n_days(self, num_days):
		oneday = datetime.timedelta(days=1)
		thismorning = datetime.datetime.combine(datetime.date.today(), self.waketime)
		if thismorning > self.now:
			thismorning = thismorning - datetime.timedelta(days=1)
		# if num_days is 2 and today is wednesday, this returns monday, tuesday and wednesday morning
		return [thismorning + datetime.timedelta(days=n) for n in range(-num_days, 2)]


	def days_since(self):
		"""Creates a list of dates since the START_DATA date"""
		days = []
		begin = datetime.datetime.strptime('2013-06-19T08:00:00+00:00', "%Y-%m-%dT%H:%M:%S+00:00")
		thismorning = self.this_morning
		if thismorning > self.now:
			thismorning = thismorning - datetime.timedelta(days=1)
		while begin <= thismorning:
			days.append(begin)
			begin = begin + datetime.timedelta(days=1)
		return days


	def secs_to_fraction(self, secs):
		"""Converts a number of seconds into a fraction of the time since WAKE_TIME"""
		now = self.now
		begin = datetime.datetime.combine(datetime.date.today(), self.waketime)

		if now < begin:
			begin = begin - datetime.timedelta(days=1)
		awake_time = (now-begin).total_seconds()
		return secs/awake_time


	def which_day_is(self, day):
		"""Finds out which date the given datetime belongs to"""
		if day.time() > self.waketime:
			return day.date()
		else:
			# if it’s before wake time, it belongs to the previous day
			return (day - datetime.timedelta(days=1)).date()