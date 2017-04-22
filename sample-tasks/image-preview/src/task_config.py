#####################################
# Standard configurations
#####################################

# Task configurations
TASK_NAME = "IMAGE-PREVIEW"
ROUTING_KEY = "*.file.image.#"

# RabbitMQ configurations
RABBITMQ_URL = "amqp://guest:guest@localhost:5672/%2f"
RABBITMQ_EXCHANGE = "clowder"

# Curator configurations
CURATOR_KEY = "phuong-test"
USE_SSL = False
SSL_VERIFY = False

#####################################
# Other task specific configurations
#####################################

# image generating binary, or None if none is to be generated
IMG_BINARY = "/usr/local/bin/imagemagickconvert"

# image preview type
IMG_TYPE = "png"

# image thumbnail command line
IMG_THUMBNAIL = "@BINARY@ @INPUT@ -resize 225^ @OUTPUT@"

# image preview command line
IMG_PREVIEW = "@BINARY@ @INPUT@ -resize 800x600 @OUTPUT@"

# type specific preview, or None if none is to be generated
PREVIEW_BIN = None

# type preview type
PREVIEW_TYPE = None

# type preview command line
PREVIEW_CMD = None
