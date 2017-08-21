from bs4 import BeautifulSoup
import requests
import argparse

class TrafficStats:
    """

    """

    def __init__(self, args_websites, args_vs, args_country):
        """

        """
        self.args_websites = args_websites
        self.args_vs = args_vs
        self.args_country = args_country


    def get_top_sites(self, limit=100, country='US'):
        """
        it returns traffic of top ranking sites in a particular country

        :param limit: total number of sites in integer
        :param country: country in ISO Code in string
        :return a list containing info about top sites
        """
        pages = int(limit / 100)
        if pages < 1:
            pages = 1
        top_sites = {}
        for page in range(1,pages+1):
            url = 'https://www.quantcast.com/top-sites/' + country + '/' + str(page)
            soup = BeautifulSoup(requests.get(url).text, 'lxml')
            left_half_div_tag = soup.findAll('div', {'class': 'left-half'})
            right_half_div_tag = soup.findAll('div', {'class': 'right-half'})

            for tag in left_half_div_tag:
                column_1 = tag.find_all('td', {'class': 'rank'})
                column_2 = tag.find_all('td', {'class': 'link'})
                column_3 = tag.find_all('td', {'class': 'digit'})

                for i in range(0, len(column_1)):
                    rank = int(column_1[i].text.strip())
                    site = column_2[i].text.strip()
                    try:
                        traffic = int(column_3[i].text.strip().replace(',',''))
                    except:
                        traffic = 0
                    top_sites[rank] = {
                        'site': site,
                        'traffic': traffic,
                    }

            for tag in right_half_div_tag:
                column_1 = tag.find_all('td', {'class': 'rank'})
                column_2 = tag.find_all('td', {'class': 'link'})
                column_3 = tag.find_all('td', {'class': 'digit'})

                for i in range(0, len(column_1)):
                    rank = int(column_1[i].text.strip())
                    site = column_2[i].text.strip()
                    try:
                        traffic = int(column_3[i].text.strip().replace(',',''))
                    except:
                        traffic = 0
                    top_sites[rank] = {
                        'site': site,
                        'traffic': traffic,
                    }
        temp_list = []
        for i in range (1,limit+1):
            try:
                temp = top_sites[i]
                temp_list.append(temp)
            except:
                pass

        return temp_list


    def get_site_traffic(self, site, country = 'US'):
        """
        it return s traffic of a particular site in particular country

        :param site: string containing domain name of website eg. google.com
        :param country: string containing ISO Code of country; default US
        :return traffic of site in integer
        """
        url = 'https://www.quantcast.com/' + site + '?country=' + country
        cookies = requests.get(url).cookies
        rev_site = '.'.join(site.split('.')[::-1])
        url = 'https://www.quantcast.com/api/profile/traffic?country=' + country + '&period=DAY30&wUnit=wd:' + rev_site
        r = requests.get(url, cookies = cookies)
        if r.status_code == requests.codes.ok:
            r = r.json()
            return int(r[0]['summaries'][country]['PEOPLE']['WEB']['reach'])
        else:
            print 'Cannot locate ' + site + ' in ' + country
            return 0


    def get_traffic_data(self):
        traffic_arg1 = 0
        traffic_arg2 = 0
        print 'Country = ' + self.args_country
        countries = self.args_country.split(',')
        if self.args_websites[:3] == 'top' and ',' not in self.args_websites:
            limit_args_websites = int(self.args_websites.replace('top',''))
            data1 = []
            for i in range (0,len(countries)):
                data1.append(self.get_top_sites(limit = limit_args_websites, country = countries[i]))

            sum_args_websites = 0
            for j in data1:
                for data in j:
                    if data['site'] in self.args_vs:
                        pass
                    else:
                        sum_args_websites += data['traffic']

            print self.args_websites + ' = ' + str(sum_args_websites)
            traffic_arg1 = sum_args_websites
        else:
            data1 = []
            websites = self.args_websites.split(',')
            for website in websites:
                for i in range (0,len(countries)):
                    data1.append(self.get_site_traffic(website, country = countries[i]))

            sum_args_websites = 0
            for data in data1:
                sum_args_websites += data
            print self.args_websites + ' = ' + str(sum_args_websites)


        if self.args_vs[:3] == 'top' and ',' not in self.args_vs:
            limit_args_vs = int(self.args_vs.replace('top',''))
            data1 = []
            for i in range (0,len(countries)):
                data1.append(self.get_top_sites(limit = limit_args_vs, country = countries[i]))

            sum_args_vs = 0
            for j in data1:
                for data in j:
                    if data['site'] in self.args_websites:
                        pass
                    else:
                        sum_args_vs += data['traffic']
            if traffic_arg1 > 0:
                sum_args_vs -= traffic_arg1
            #print self.args_vs + ' = ' + str(sum_args_vs)
            print self.args_vs + '(except ' + self.args_websites + ') = ' + str(sum_args_vs)
        else:
            data2 = []
            vss = self.args_vs.split(',')
            for vs in vss:
               for i in range (0,len(countries)):
                   data2.append(self.get_site_traffic(vs, country = countries[i]))
            sum_args_vs = 0
            for data in data2:
                sum_args_vs += data
            traffic_arg2 = sum_args_vs
            #print self.args_vs + ' = ' + str(sum_args_vs)
            print self.args_vs + '(except ' + self.args_websites + ') = ' + str(sum_args_vs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--websites', help='add either google.com,buzzfeed.com,... or top5/top10/...')
    parser.add_argument('--vs', help='add either google.com,buzzfeed.com,... or top5/top10/...')
    parser.add_argument('--country', help='add two digit ISO Code of countries (separate multiple countries with , ) eg: US,IN,AU,GLOBAL')

    args = parser.parse_args()

    if not args.country:
        args.country = 'US'

    if 'top' in args.websites and 'top' in args.vs:
        top_args_websites = int(args.websites.replace('top',''))
        top_args_vs = int(args.vs.replace('top',''))
        if top_args_vs < top_args_websites:
            temp = args.websites
            args.websites = args.vs
            args.vs = temp
    traffic_stats = TrafficStats(args.websites, args.vs, args.country)
    traffic_stats.get_traffic_data()
