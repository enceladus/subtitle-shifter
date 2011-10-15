import datetime, time, sys, re

def change_time(hour, minute, second, time_diff):
	""" Changes a time by the amount of seconds specified as time_diff
		Parameters:
			hour: hour value of the time
			minute: minute value
			second: second value
			time_diff: the distance (in seconds) by which to change the time
					   (this can be positive or negative)
	"""
	current_time = datetime.datetime(1, 1, 1, hour, minute, second)
	difference = datetime.timedelta(seconds=time_diff)
	
	try:
		return current_time + difference
	except OverflowError:
		print 'ERROR: Date value out of range.'
		sys.exit()
	except:
		print 'ERROR: Error changing time.'
		return None
		
def process_time_string(s, time_diff):
	""" Processes a .SRT subtitle time string. Ignores milliseconds.
		Parameters:
			s: the time string. Format: HH:MM:SS,MMS (milliseconds)
			time_diff: the time change to apply (in seconds)
	
	"""
	
	# Ignore milliseconds
	s = s.split(',')
	
	# Convert to time object
	dt = time.strptime(s[0], '%H:%M:%S')
	
	# Apply time difference
	dt = change_time(dt.tm_hour, dt.tm_min, dt.tm_sec, time_diff)
	
	# Fix formatting for the minutes
	minutes = str(dt.minute)
	seconds = str(dt.second)
	if len(minutes) == 1:
		minutes = '0%s' % (minutes,)
	if len(seconds) == 1:
		seconds = '0%s' % (seconds,)
	
	new_time_string = '0%s:%s:%s,%s' % (str(dt.hour), minutes, seconds, s[1])
	return new_time_string
	
def is_time_string(s):
	""" Determines if a string 's' is an SRT file time string
		Format: HH:MM:SS,MMS --> HH:MM:SS,MMS
	"""
	if re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', s):
		return True
	return False
	
def shift_subtitles(rfile, wfile, time_diff):
	""" Takes subtitles from rfile, alters them by time_diff, and writes to wfile.
		Parameters:
			rfile: The subtitle file to read
			wfile: The subtitle file to write
			time_diff: The time change to apply (in seconds)
			
		Important to note is that the subtitle times are indicated in SRT files by:
			01:12:05,328 --> 01:12:09,100
		The first time is when the subtitle appears, the second time is when it disappears
	"""
	
	# Open files for reading and writing
	try: 
		source_file = file(rfile, 'r')
	except IOError:
		print 'ERROR: No such file or directory:', rfile
		sys.exit()
	print 'Reading from file:', rfile
	
	try:
		new_file = file(wfile, 'w')
	except IOError:
		print 'ERROR: No such file or directory:', wfile
		sys.exit()
	print 'Writing to file:', wfile
	
	new_lines = []
	
	for line in source_file.readlines():
		line = line[:-2] 					# removes '\r\n' from line
		print 'Read line:', line
		if is_time_string(line):
			print 'Identified time string:', line
			times = line.split(' --> ')		# split up the two times
			new_times = []
			for t in times:
				new_times.append(process_time_string(t, time_diff))
			line = new_times[0] + ' --> ' + new_times[1]
			print 'Changed times:', line
		new_lines.append(line + '\r\n')		# adds back in '\r\n'
		print 'Line added:', new_lines[-1]
	
	for line in new_lines:
		new_file.write(line)
		print 'Wrote line:', line
	
# the script runs from here
shift_subtitles(sys.argv[1], sys.argv[2], int(sys.argv[3]))
			