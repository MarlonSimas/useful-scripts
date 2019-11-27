import os
from datetime import datetime, timedelta

endpoint = 's3://platform-dumps-virginia/users/'
date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
print("APIKEY:") 
apiKey = input() + '-r'

#Grabing file name from AWS bucket and downloading 
get_file_name = os.popen("s3cmd ls "+ endpoint + date + "/" + apiKey + "| grep -oP 's3://.*.gz'").read()
os.system("s3cmd get " + get_file_name)

#Spliting files by slash and dot
split_file_by_slash = get_file_name.split('/') 
split_file_by_slash_final = split_file_by_slash[len(split_file_by_slash)-1]

split_file_by_dot = split_file_by_slash_final.split('.')
split_file_by_dot_final = split_file_by_dot[0]

#unziping the .gz downloaded file
os.system("gunzip " + split_file_by_slash_final)

#Parsing file, returning only e-mails from optOut == true accounts 
os.system("jq 'select(.optOutChaordic == true) | .email' " +
split_file_by_dot_final+" > " + apiKey + "-OptOut")

#Removing unecessary file 
os.system("rm " + split_file_by_dot_final)
