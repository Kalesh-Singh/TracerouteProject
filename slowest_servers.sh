if [ ! -e dependencies/server_list.txt ]; then
	echo "Server list not found!"
	echo "Getting server list ..."
	python3 dependencies/get_server_list.py
	echo "Retrieved server list ..."
	echo "Performing traceroute tests ... (This will take a few hours)"
	dependencies/traceroute.sh > dependencies/traceroute_results.txt
	echo "Completed traceroute tests"
else
	echo "Sever list found ..."
fi

echo "Performing analysis of data ..."
python3 dependencies/parse_results.py > output.txt
echo "Generated output.txt file ..."
more output.txt



