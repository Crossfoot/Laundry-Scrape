import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sched, time
import requests, bs4


scope = ['https://spreadsheets.google.com/feeds', 
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', 
                                                          scope)
gc = gspread.authorize(creds)
sheet = gc.open('Laundry Scrape Data')

def main():
  row = 2
  print(len(sheet.worksheet("Data").col_values(1)))
  while True:
    data = scrape_site()
    add_datapoint(data, row)
    row += 1
    time.sleep(300)# Insert a wait for 3-5 minutes


def scrape_site(): #scrapes site for availability of washers, and 
  site = requests.get('http://washalert.washlaundry.com/washalertweb/calpoly/WASHALERtweb.aspx?location=950de8d6-9345-4a4f-9f64-f3a1daa6b865')
  site_data = bs4.BeautifulSoup(site.text, 'html.parser') 
  data = [time.strftime('%a', time.localtime())]
  for i in range(7, 11):
    if site_data.find_all('tr')[i].find_all('td')[2].string == 'Available':
      data.append('1')
    else:
      data.append('0')
  data.append(time.strftime('%H', time.localtime()))
  return data


def add_datapoint(data, row): #This function just adds a new row
  day = time.strftime('%a', time.localtime())
  for x in range(len(data)):
    sheet.worksheet("Data").update_cell(row , 1 + x, data[x])

if __name__ == '__main__':
  main()
