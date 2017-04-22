#!/usr/bin/env python

import logging
import os
import subprocess
import tempfile
import re
import task_config as configs
import pymonad.extractors as extractors


def main():
    global logger

    #set logging
    logging.basicConfig(format='%(levelname)-7s : %(name)s -  %(message)s', level=logging.INFO)
    logging.getLogger('pymonad.extractors').setLevel(logging.DEBUG)
    logger = logging.getLogger(configs.TASK_NAME)
    logger.setLevel(logging.DEBUG)

    #connect to rabbitmq
    extractors.connect_message_bus(
        extractorName=configs.TASK_NAME,
        messageType=configs.ROUTING_KEY,
        processFileFunction=process_file,
        rabbitmqExchange=configs.RABBITMQ_EXCHANGE,
        rabbitmqURL=configs.RABBITMQ_URL)


# ----------------------------------------------------------------------
# Process the file and upload the results
def process_file(parameters):

    print(parameters['inputfile'])

    if configs.IMG_BINARY:
        execute_command(parameters, configs.IMG_BINARY, configs.IMG_THUMBNAIL, configs.IMG_TYPE, True)
        execute_command(parameters, configs.IMG_BINARY, configs.IMG_PREVIEW, configs.IMG_TYPE, False)
    if configs.PREVIEW_BIN:
        execute_command(parameters, configs.PREVIEW_BIN, configs.PREVIEW_CMD, configs.PREVIEW_TYPE, False)

def execute_command(parameters, binary, commandline, ext, thumbnail=False):
    global logger

    (fd, tmpfile)=tempfile.mkstemp(suffix='.' + ext)
    try:
        # close tempfile
        os.close(fd)
        file_name = None
        try:
            file_name = parameters['filename']
        except:
            file_name = parameters['inputfile']

        # replace some special tokens
        commandline = commandline.replace('@BINARY@', binary)
        commandline = commandline.replace('@INPUT@', parameters['inputfile'])
        commandline = commandline.replace('@OUTPUT@', tmpfile)

        # split command line
        p = re.compile(r'''((?:[^ "']|"[^"]*"|'[^']*')+)''')
        commandline = p.split(commandline)[1::2]


        # execute command
        x = subprocess.check_output(commandline, stderr=subprocess.STDOUT)
        if x:
            logger.debug(binary + " : " + x)

        if(os.path.getsize(tmpfile) != 0):
            # upload result
            if thumbnail:
                extractors.upload_thumbnail(thumbnail=tmpfile, parameters=parameters)
                extractors.upload_preview(previewfile=tmpfile,parameters=parameters)
            else:
                extractors.upload_preview(previewfile=tmpfile, parameters=parameters)
    except subprocess.CalledProcessError as e:
        logger.error(binary + " : " + str(e.output))
        raise
    finally:
      try:
        os.remove(tmpfile)
      except:
        pass

if __name__ == "__main__":
    main()
