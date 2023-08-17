# try to get the needed data here before translating to rust

import requests, json, time
from datetime import datetime, timedelta
from tqdm import tqdm

from ValeraLib.utils.DuckTypes import Timestamp
from ValeraLib import dbg, tg_msg, shutdown

def get1000points(t_iso):
	params = {
		"symbol": ".BVOL24H",
		"count": 1000,
		"reverse": "true",
		"endTime": t_iso
	}
	r = requests.get("https://www.bitmex.com/api/v1/trade", params=params)
	data = {
		"quotes": r.json(),
		"rate-limit": {
			"remaining": r.headers.get(('x-ratelimit-remaining')),
			"reset-unix-s": r.headers.get(('x-ratelimit-reset'))
		}
	}
	return data

def main():
	dict_buffer = {}
	t_iso = Timestamp(time.time()).Isoformat
	# t_iso = "2014-11-07T20:55:00.000Z"
	
	try:
		for i in tqdm(range(10_000)):
			data = get1000points(t_iso)
			for entry in data['quotes']:
				dict_buffer[entry['timestamp']] = entry['price']
			t_iso = data['quotes'][-1]['timestamp']
			assert len(data['quotes']) > 100, "Seems like we're finished"
   
			if int(data['rate-limit']['remaining']) < 2:
				sleep_duration = int(data['rate-limit']['reset-unix-s']) - time.time()
				time.sleep(max(1, sleep_duration))
	except:
		try:saved = json.load(open('dict_buffer.json', 'r'))
		except:saved = {}
		saved.update(dict_buffer)
		json.dump(saved, open('dict_buffer.json', 'w'), indent=4)
		tg_msg()
		# shutdown()
	
	# buffer = []

if __name__=='__main__':
	try:
		main()
	except Exception as e:
		import traceback
		traceback.print_exc()
	finally:
		from ValeraLib import alert
		alert()