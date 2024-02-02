from datetime import datetime

def today() :
    days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    months = [
        "January", "February", "March", 
        "April", "May", "June", 
        "July", "August", "September", 
        "October", "November", "December"
    ]
    now = datetime.now()
    day_week = days[int(now.strftime("%w"))]
    day_number = now.strftime("%d")
    month = months[int(now.strftime("%m"))-1]
    year = now.strftime("%Y")
    output = day_week[:3] + " " + day_number + " " + month[:3] + ", " + year
    return output
