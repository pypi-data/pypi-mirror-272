import pycountry
import time
import openai
import urllib.parse
import json

def input_path(message=""):  #translate copy path of windows
  
  raw_s=input(message) if message=="" else message
  raw_s=raw_s.replace(r'"','')
  return "/content/drive/Shareddrives/"+'/'.join(raw_s.split("\\")[2:])



# Report issues
def raise_issue(e, model, prompt):
    issue_title = urllib.parse.quote("[bug] Hosted Gorilla: <Issue>")
    issue_body = urllib.parse.quote(f"Exception: {e}\nFailed model: {model}, for prompt: {prompt}")
    issue_url = f"https://github.com/ShishirPatil/gorilla/issues/new?assignees=&labels=hosted-gorilla&projects=&template=hosted-gorilla-.md&title={issue_title}&body={issue_body}"
    print(f"An exception has occurred: {e} \nPlease raise an issue here: {issue_url}")

# Query Gorilla server
def ask_gpt(prompt="Get the Alpha3 code of the country", model="gorilla-openfunctions-v0", functions=[]):
  openai.api_key = "EMPTY" # Hosted for free with ❤️ from UC Berkeley
  openai.api_base = "http://luigi.millennium.berkeley.edu:8000/v1"
  try:
    completion = openai.ChatCompletion.create(
      model="gorilla-openfunctions-v1",
      temperature=0.0,
      messages=[{"role": "user", "content": prompt}],
      functions=functions,
    )
    return completion.choices[0].message.function_call.arguments
  except Exception as e:
    print(e, model, prompt)

function_documentation = {
    "name" : "Alpha 3",
    "api_call": "country",
    "description": "Get alpha 3 code of country",
    "parameters": [
        {
            "name": "country",
            "description": "The chosen country alpha code 3, eg. if united states, then USA. it has to have 3 letters"
        }
    ]
}

def get_alpha_3(x):
  whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
  answer = ''.join(filter(whitelist.__contains__, x))
  try:
    return pycountry.countries.search_fuzzy(answer)[0].alpha_3
  except:
    got_it=True
    while got_it:
      try:
        other_fuzzy=ask_gpt(prompt=answer, functions=[function_documentation]).country
        got_it=False
        return pycountry.countries.search_fuzzy(other_fuzzy)[0].alpha_3
      except:
        time.sleep(5)
def get_data(path=False,sheet_name=0,usecols=None,header=0):  #easy get data from MES csv   ###############################################  path y sheet_name
    #import drive
    drive.mount("/content/drive")
    #transform str and get doc
    if path:
      newpath=path
    else:
      newpath=input_path('Input path:')
    
    if (newpath.split("/")[-1].split(".")[-1] == "xlsx") or (newpath.split("/")[-1].split(".")[-1] == "xls"):
        df=pd.read_excel(newpath,sheet_name=sheet_name,header=header)
    elif (newpath.split("/")[-1].split(".")[-1] == "csv"):
        df=pd.read_csv(newpath)
    elif (newpath.split("/")[-1].split(".")[-1] == "sav"):
        df=pd.read_spss(newpath,usecols=usecols)
        # try:
        #    df=df.rename(columns={"WEEK": "Weeks", "MKT": "Geographies"})
           
        # except:
        #    pass
    else:
        raise ValueError('Format Not Found')
    try:
      df=df.drop("Unnamed: 0",axis=1)
    except:
       pass
    try:
      df["Weeks"]=pd.to_datetime(df["Weeks"])
    except:
      pass
    
    return df

