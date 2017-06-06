# webstatus-update
Provide status updates to the web site by uploading a JSON file over scp.

## Usage
uploadJsonStatusFile.py _configuration file_

If no configuration file is given, the configuration file defaults to
'config.yaml'. 

The configuration file lets you configure multiple settings. You can specify
 the filenames for each of the three yaml files that the json file
 will the produced from, the filename of the json file to be
 produced, the json schema file to validate it against, the scp command to upload it with, the host to upload it to, the path to the file on the remote server, and the filename to use for the file on the remote server.
 
 See the config.yaml file for an example of what the setttings should look like.

