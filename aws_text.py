def aws_rec(img_name):

	import os
	import boto3


	## aws 


	import io
	from io import BytesIO
	import sys

	import psutil
	import time

	import math
	from PIL import Image, ImageDraw, ImageFont

	""""""

	# Document
	documentName = str(img_name)

	# Read document content
	with open(documentName, 'rb') as document:
	    imageBytes = bytearray(document.read())

	# Amazon Textract client
	textract = boto3.client('textract')

	# Call Amazon Textract
	response = textract.detect_document_text(Document={'Bytes': imageBytes})

	#print(response)

	# Print detected text
	list_rec=[]
	for item in response["Blocks"]:
	    if item["BlockType"] == "LINE":
	        #print ('\033[94m' +  item["Text"] + '\033[0m')
	        list_rec.append(item["Text"])

	return list_rec
