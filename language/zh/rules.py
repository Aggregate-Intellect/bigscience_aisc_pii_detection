# Refer to Big Science code: https://github.com/bigscience-workshop/data_tooling/blob/master/pii_processing/regex/hhn_en.py

import regex # Mandarin regex pattern would need the regex module

rulebase = [([
    ("AGE", regex.compile(), None, None, None),
    ("STREET_ADDRESS", regex.compile(), None, None, None),
    ("GOVT_ID", regex.compile(), None, None, None), 
    ("PHONE", regex.compile(), None, None, None), 
    ("LICENSE_PLATE", regex.compile(), None, None, None)
    ("USER_ID", regex.compile(), None, None, None),
    ("DISEASE", regex.compile("diabetes|cancer|HIV|AIDS|Alzheimer's|Alzheimer|heart disease", re.IGNORECASE), None, None, None)
],1)]