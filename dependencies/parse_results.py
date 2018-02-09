import json
import numpy

data = json.load(open('dependencies/data30.json'))
servers = []

with open('dependencies/traceroute_results.txt', 'r') as traceroute_results_file:
	servers = traceroute_results_file.read()

servers = servers.split('server end')[:-1]	# Remove the empty line from the end

results = []
for server in servers:
	round_trip_times = [] 	
	trials = server.split('traceroute end')[:-1]	# Remove the blank line from the end
	
	for trial in trials:
		hops = trial.split('\n')[1:-1]				# Remove the blank lines from the beginning and end
		good_hops = [hop for hop in hops if hop.split(' ')[-3:] != ['*', '*', '*']]
		if good_hops != []:
			last_hop_results = good_hops[-1].split(' ')
			for x in last_hop_results[3:]:		# Ensure to trim the hop count from the front
				try:
					time = float(x)
					round_trip_times.append(time)
				except ValueError:
					pass
	results.append(round_trip_times)

for i, server_result in enumerate(results):
	x = numpy.array(server_result)
	average = x.mean()
	standard_deviation = x.std()
	average_plus_4std = average + (4 * standard_deviation)
	data[i]['avg_rt_time'] = average
	data[i]['std_rt_time'] = standard_deviation
	data[i]['avg_plus_4std'] = average_plus_4std	

# Get the top 5 slowest servers by average roundtrip time on the last hop
top_5_avg = []
for _ in range(5):
	max_val = 0
	for server in data:
		x = server['avg_rt_time'] 
		if x > max_val and x not in top_5_avg:
			max_val = x
	top_5_avg.append(max_val)

slowest_5_by_avg = []
for x in top_5_avg:
	for server in data:
		if server['avg_rt_time'] == x:
			slowest_5_by_avg.append(server)
			break

# Get the top 5 slowest servers by the average + (4 * std) of the 
#roundtrip time on the last hop
top_5_avg_plus_4std = []
for _ in range(5):
	max_val = 0
	for server in data:
		x = server['avg_plus_4std'] 
		if x > max_val and x not in top_5_avg_plus_4std:
			max_val = x
	top_5_avg_plus_4std.append(max_val)

slowest_5_by_avg_plus_4std = []
for x in top_5_avg_plus_4std:
	for server in data:
		if server['avg_plus_4std'] == x:
			slowest_5_by_avg_plus_4std.append(server)
			break

def print_result(heading, lst):
	"""Prints formatted results"""
	print('\t\t\t' + heading.upper() + '\n')
	for server in lst:
		print('Name:', server['name'])
		print('Server:', server['web_pages'][0][:-1].split('//')[-1])
		print('Country:', server['country'])
		print('Roundtrip time of Traceroute:')
		print('\tAverage:\t\t', str(round(server['avg_rt_time'], 2)), 'ms')
		print('\tStandard Deviation:\t', str(round(server['std_rt_time'], 2)), 'ms')
		print('\tAvg + (4 * Std):\t', str(round(server['avg_plus_4std'], 2)), 'ms')
		print('-' * 100)
	print('\n')

print_result('top 5 slowest servers by average roundtrip time', slowest_5_by_avg)
print_result('top 5 slowest servers by Avg + 4 * Std roundtrip time', slowest_5_by_avg_plus_4std)

