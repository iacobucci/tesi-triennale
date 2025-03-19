#!/usr/bin/python3
import sys

class Time:
	def __init__(self):
		self.hours = 0
		self.minutes = 0
		self.seconds = 0
	def add(self,hours,minutes,seconds):
		self.hours += hours
		self.minutes += minutes
		self.seconds += seconds
		if self.seconds >= 60:
			self.seconds -= 60
			self.minutes += 1
		if self.minutes >= 60:
			self.minutes -= 60
			self.hours += 1
	def __repr__(self):
		secs = self.seconds
		if self.seconds < 10:
			secs = "0" + str(self.seconds)
		mins = self.minutes
		if self.minutes < 10 and self.hours != 0:
			mins = "0" + str(self.minutes)
		if self.hours == 0:
			return f"{mins}:{secs}"
		else:
			return f"{self.hours}:{mins}:{secs}"
	def __str__(self):
		return self.__repr__()

# read from stdin and write to stdout
def main():
	# Leggi l'input da stdin
	text = sys.stdin.read()

	output_lines = []

	total_time = Time()
	lines = text.split("\n")
	for line in lines:
		if line.startswith("#"):
			ts = line.split("#")
			time = ts[1].split(":")
			if len(time) == 3:
				hours = int(time[0])
				minutes = int(time[1])
				seconds = int(time[2])
				total_time.add(hours,minutes,seconds)
			if len(time) == 2:
				minutes = int(time[0])
				seconds = int(time[1])
				total_time.add(0,minutes,seconds)
			if len(time) == 1:
				seconds = int(time[0])
				total_time.add(0,0,seconds)
			output_lines.append("## " + str(total_time))
		else:
			output_lines.append(line)

	# Scrivi l'output su stdout
	print("# " + str(total_time))
	print("\n".join(output_lines))

if __name__ == '__main__':
	main()