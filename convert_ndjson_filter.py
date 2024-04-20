import json
from sys import argv
from textblob import TextBlob
import datetime
import re

fndJson = open(argv[1], "r")
outCSV = open(argv[2], "w")

outCSV.write("Subreddit,Score,Timestamp,Body,LinkID,ParentID,Polarity,Subjectivity\r\n")


for line in fndJson:
    jsonObj = json.loads(line)
    for j in range(2, len(argv)):
        match = True
        if len(argv[j].split("+")) == 1:
            match = re.search(r"\b" + re.escape(argv[j]) + r"\b", jsonObj['body'].lower())
        else:
            for i in argv[j].split("+"):
                if not re.search(r"\b" + re.escape(i) + r"\b", jsonObj['body'].lower()):
                    match = False
        if match:
            strippedBody = jsonObj['body'].strip().replace("\n"," ").replace("\r", " ").replace(",", " ")
            print(jsonObj)
            txtBlbAnalysis = TextBlob(strippedBody)
            tsString = datetime.datetime.fromtimestamp(int(jsonObj['created_utc']))
            outString = "%s,%s,%s,%s,%s,%s,%s,%s\r\n" % (jsonObj['subreddit'], jsonObj['score'],
                                                         tsString, strippedBody, jsonObj['link_id'],
                                                         jsonObj['parent_id'], txtBlbAnalysis.sentiment.polarity,
                                                         txtBlbAnalysis.sentiment.subjectivity)
            outCSV.write(outString)
            break
fndJson.close()
outCSV.close()
