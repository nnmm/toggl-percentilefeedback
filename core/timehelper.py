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


	def which_day_is(self, day):
		"""Finds out which date the given datetime belongs to"""
		if day.time() > self.waketime:
			return day.date()
		else:
			# if it’s before wake time, it belongs to the previous day
			return (day - datetime.timedelta(days=1)).date()