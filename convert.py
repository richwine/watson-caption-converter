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

# function to format time for SRT file
def srt_time(self):
    ms = (str(self).split("."))[1]
    sec = self
    min = sec / 60
    hr = min / 60
    time = "%02d:%02d:%02d,%s" % (hr, min % 60, sec % 60, ms.ljust(3,'0'))
    return time

# function to format time for VTT file
def vtt_time(self):
    ms = (str(self).split("."))[1]
    sec = self
    min = sec / 60
    hr = min / 60
    time = "%02d:%02d:%02d.%s" % (hr, min % 60, sec % 60, ms.ljust(3,'0'))
    return time

# function to format time for VTT file
def stl_time(self):
    ms = (str(self).split("."))[1]
    sec = self
    min = sec / 60
    hr = min / 60
    time = "%02d:%02d:%02d.%s" % (hr, min % 60, sec % 60, ms.ljust(2,'0'))
    return time

# Load JSON from Watson (replace watson.json with path to JSON file)
str_data = open('watson.json').read()
try:
    json_data = json.loads(str_data)
except:
    print "ERROR: The JSON is not formatted properly."
    quit()

# open subtitle files in write mode (overwrites if it already exists)
f_srt = open('subtitles.srt','w')
f_vtt = open('subtitles.vtt','w')
f_stl = open('subtitles.txt','w')
f_scc = open('subtitles.scc','w')

# starts subtitle id counter for SRT file
sub_id = 0

# writes headers for VTT file and set VTT display format
f_vtt.write("WEBVTT\n\n")
display_vtt = "align:middle line:84%"

# writes header for STL .txt file
stl_header = """{QTtext}{timescale:100}{textBox: 0, 0, 45, 0}{font:Arial}{size:16}{backColor:0,0,0}
{textColor:65535,65535,65535}{width:640}{height:40}{justify:Center}\n\n\n"""
f_stl.write(stl_header)

# writes header for SCC .scc file
scc_header = "Scenarist_SCC V1.0\n\n"
f_scc.write(scc_header)

# iterate through JSON array
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
            try:
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
            except:
                print 'ERROR: Cannot find timestamps in JSON. Please ensure word timestamps are enabled in Watson.'
                quit()


        for x in tran_list:

            # formats time for SRT format
            st_time = srt_time(x[2])
            en_time = srt_time(x[3])

            # generates and writes block to SRT file, loops until all entries complete
            block = "%s\n%s --> %s\n%s\n\n" % (x[0],st_time,en_time,x[1])
            f_srt.write(block)

            # formats time for VTT format
            st_time = vtt_time(x[2])
            en_time = vtt_time(x[3])

            # generates and writes block to VTT file, loops until all entries complete
            block = "%s\n%s --> %s %s\n%s\n\n" % (x[0],st_time,en_time,display_vtt,x[1])
            f_vtt.write(block)

            # formats time for STL format
            st_time = stl_time(x[2])
            block = "[%s]\n%s\n\n" % (st_time,x[1])
            f_stl.write(block)



f_srt.close()
f_vtt.close()
f_stl.close()
f_scc.close()
