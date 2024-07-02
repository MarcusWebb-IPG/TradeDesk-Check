# TradeDesk-Check
Couple of routines for checking TradeDesk Integrations

## Reminder
Dont' forget to create your virtual environment first, then run
  pip install -r requirements.txt
to ensure you're properly configured before running these scripts

### check_TRADS_credentials.py and check_sandbox_TRAS.py
These both need the following on hand:
  - email address
  - associated Password

You will be prompted for these items - the Password request operates as per a standard Password field (i.e. it replaces typed characters with asterisks (*) when being filled)
The resultant output shows you what is configured for the above combination

### td_rnb_check.py
This script needs the following on hand:
  
  - Password for api@cadreon.com

Optionally required:
  - partner ID

You will be prompted for these items - the Password request operates as per a standard Password field (i.e. it replaces typed characters with asterisks (*) when being filled)
This routine tries to guess the partner ID but prompts you to confirm that it is correct, and optionally if incorrect, offers you the chance to supply your own Partner ID
The resultant output shows you what is configured for the above combination



### batch-csv-check.py
You need to save a local copy of the TradeDesk credentials into a csv file called known-good.csv in the same folder as these routines.
You can then run this script.
It will cycle through the credentials presented and attempt to log in with each one. 

- If successful:
  - The credentials are displayed on screen
  - If there are no campaigns running
    -  A warning is displayed on screen stating that although the credentials appear valid we can't be 100% certain
  - The credentials are then written to a file called OK-<<timestamp>>.csv
- else if Not successful:
  - A warning is displayed on screen showing the error that was received.
  - The credentials are written to BadCredentials.csv
