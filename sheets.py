import gspread

gc = gspread.service_account("credentials.json")

sh = gc.open("FKER RSVP")
worksheet = sh.get_worksheet(0)
value = worksheet.acell('A1').value

print(value)