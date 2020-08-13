def aws_api(filename):
  import requests
  import base64
  import json
  url = ""
  
  with open(filename, "rb") as img_file:
      my_string = base64.b64encode(img_file.read())
  #print(my_string)
  my_string=my_string.decode('utf-8')
  #print(my_string)
  #payload = "{\r\n  \"Image\":"+"\""+my_string+"\""+"\r\n}"
  payload = {'Image':my_string}
  headers = {
    'x-api-key': '',
    'Content-Type': 'application/json',
    'Connection':'keep-alive'
  }

  response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

  return response.json()


