#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details. http://www.gnu.org/licenses/

import json
import math

# Load JSON from Watson (replace watson.json with path to JSON file)
str_data = open('watson.json').read()
json_data = json.loads(str_data)

# open subtitle file in write mode
# this will create the file if it doesn't exist, or overwrite if it does
f = open('subtitles.srt','w')

# starts subtitle id counter for SRT file
sub_id = 0

for x in json_data["results"]:
    for y in x["alternatives"]:
        tran_start = 0
        tran_end = 0
        word_list = []
        tran_list = []
        custom_tran = ""

        # checks to see is transcript is long (over 60 chars)
        if len(y["transcript"]) > 60:
            long_tran = True
            # calculate how many characters allowed per subtitle
            max_chars = len(y["transcript"]) / math.ceil( len(y["transcript"]) / 60.0 )
        else:
            long_tran = False

        # iterates JSON and records transcript lines with start and end times
        # ignores entry if Watson confidence is 0.00
        if y["confidence"] == 0.00:
            break
        else:
            for z in y["timestamps"]:
                word = str(z[0])
                custom_tran = custom_tran + "%s " % word
                word_start = z[1]
                if tran_start == 0 or word_start < tran_start:
                    tran_start = word_start
                word_end = z[2]
                if word_end > tran_end:
                    tran_end = word_end
                if long_tran is True :
                    if len(custom_tran) > max_chars :
                        sub_id += 1
                        tran_list.append([sub_id,custom_tran,tran_start,tran_end])
                        custom_tran = ""
                        tran_start = 0
                        tran_end = 0
            sub_id += 1
            tran_list.append([sub_id,custom_tran,tran_start,tran_end])


        for x in tran_list:

            # reformatting the time for SRT format (convert to function later)
            st_ms = (str(x[2]).split("."))[1]
            st_sec = x[2]
            st_min = st_sec // 60
            st_hr = st_min // 60
            st_time = "%02d:%02d:%02d,%s" % (st_hr, st_min % 60, st_sec % 60, st_ms)
            en_ms = (str(x[3]).split("."))[1]
            en_sec = x[3]
            en_min = en_sec // 60
            en_hr = en_min // 60
            en_time = "%02d:%02d:%02d,%s" % (en_hr, en_min % 60, en_sec % 60, en_ms)

            #
            sub_block = "%s\n%s --> %s\n%s\n\n" % (x[0],st_time,en_time,x[1])
            #
            f.write(sub_block)

print "Conversion to SRT successful!"

f.close()
