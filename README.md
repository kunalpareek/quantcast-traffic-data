# quantcast-traffic-data
gives traffic data of websites as mentioned in quantcast.com


Requirements:

1. python 2.7
2. python packages mentioned in requirements.txt


How to run:

1. to get data of top sites vs top sites

python traffic_stats.py --websites top5 --vs top100 --country US

2. to get data of specific sites vs top sites

python traffic_stats.py --websites google.com,amazon.com --vs top100 --country US

3. to get data of specific sites vs specific sites

python traffic_stats.py --websites google.com,amazon.com --vs buzzfeed.com --country US

