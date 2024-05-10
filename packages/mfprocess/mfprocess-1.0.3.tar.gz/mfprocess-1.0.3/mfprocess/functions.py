def input_path(message=""):  #translate copy path of windows
  
  raw_s=input(message) if message=="" else message
  raw_s=raw_s.replace(r'"','')
  return "/content/drive/Shareddrives/"+'/'.join(raw_s.split("\\")[2:])



