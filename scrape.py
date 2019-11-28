import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sched, time
import requests, bs4


scope = ['https://spreadsheets.google.com/feeds', 
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', 
                                                          scope)
gc = gspread.authorize(creds)


def main():
  row = 2
  while True:
    data = scrape_site()
    add_datapoint(data, row)
    row += 1
    time.sleep(300)# Insert a wait for 3-5 minutes


def scrape_site(): #scrapes site for availability of washers, and 
  site = requests.get('http://washalert.washlaundry.com/washalertweb/calpoly/WASHALERtweb.aspx?location=950de8d6-9345-4a4f-9f64-f3a1daa6b865')
  site_data = bs4.BeautifulSoup(site.text, 'html.parser') 
  data = [time.strftime('%a %d %b %Y, %I:%M%p', time.localtime())]
  if site_data.find_all('tr')[7].find_all('td')[2].string == 'Available':
    data.append('1')
  else:
    data.append('0')
  if site_data.find_all('tr')[8].find_all('td')[2].string == 'Available':
    data.append('1')
  else:
    data.append('0')
  if site_data.find_all('tr')[9].find_all('td')[2].string == 'Available':
    data.append('1')
  else:
    data.append('0')
  if site_data.find_all('tr')[10].find_all('td')[2].string == 'Available':
    data.append('1')
  else:
    data.append('0')
  return data


def add_datapoint(data, row): #This function just adds a new row
  sheet = gc.open('Laundry Scrape Data').sheet1
  for x in range(len(data)):
    sheet.update_cell(row, 1 + x, data[x])


if __name__ == '__main__':
  main()
