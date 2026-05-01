# quick_fix.py - Automatically fix the data files

import csv

print("Applying quick fixes...")

# Fix 1: Update timeslots.csv
timeslots_data = [
    ["MWF-8","Monday/Wednesday/Friday","08:00","50"],
    ["MWF-9","Monday/Wednesday/Friday","09:00","50"],
    ["MWF-10","Monday/Wednesday/Friday","10:00","50"],
    ["MWF-11","Monday/Wednesday/Friday","11:00","50"],
    ["MWF-12","Monday/Wednesday/Friday","12:00","50"],
    ["MWF-1","Monday/Wednesday/Friday","13:00","50"],
    ["MWF-2","Monday/Wednesday/Friday","14:00","50"],
    ["TTh-8","Tuesday/Thursday","08:00","75"],
    ["TTh-930","Tuesday/Thursday","09:30","75"],
    ["TTh-11","Tuesday/Thursday","11:00","75"],
    ["TTh-1","Tuesday/Thursday","13:00","75"],
    ["TTh-230","Tuesday/Thursday","14:30","75"],
]

with open("timeslots.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["SlotID","Days","StartTime","Duration"])
    writer.writerows(timeslots_data)
print("✓ Updated timeslots.csv")

# Fix 2: Add more rooms
rooms_data = [
    ["R101","CS Building","50","Lab;Projector;Whiteboard"],
    ["R102","CS Building","40","Projector;Whiteboard"],
    ["R103","CS Building","60","Projector;Whiteboard"],
    ["R201","CS Building","45","Projector;Whiteboard"],
    ["R202","CS Building","55","Projector;Whiteboard"],
    ["L301","Lab Building","35","Lab;Projector"],
    ["L302","Lab Building","50","Lab;Projector"],
    ["M101","Main Building","80","Projector;Whiteboard"],
    ["M102","Main Building","70","Projector;Whiteboard"],
    ["M201","Main Building","100","Projector;Whiteboard"],
]

with open("rooms.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["RoomID","Building","Capacity","Features"])
    writer.writerows(rooms_data)
print("✓ Updated rooms.csv")

# Fix 3: Update instructor availability
instructor_data = [
    ["Mr Aamir Gulzar","MWF-8;MWF-9;MWF-10;TTh-8;TTh-930","MWF-9;MWF-10"],
    ["Mr Arshad Islam","MWF-8;MWF-9;MWF-10;TTh-8;TTh-930;TTh-11","TTh-930"],
    ["Maam Marium Hida","MWF-8;MWF-9;MWF-10;MWF-11;MWF-12;TTh-8;TTh-930","MWF-9;MWF-10"],
    ["Mr Anas Bin Rashid","MWF-8;MWF-9;MWF-10;TTh-8;TTh-930;TTh-11","TTh-930"],
    ["Mr Hasnain Akhtar","MWF-8;MWF-9;MWF-10;TTh-8;TTh-11","TTh-11"],
    ["Mr Hasan Mujtaba","MWF-8;MWF-9;MWF-10;MWF-11;MWF-12;TTh-8;TTh-930;TTh-11","MWF-11"],
    ["Maam Bushra Kanwal","MWF-8;MWF-9;MWF-10;MWF-11;TTh-8;TTh-930","MWF-9"],
]

with open("instructor_availability.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Instructor","AvailableSlots","PreferredSlots"])
    writer.writerows(instructor_data)
print("✓ Updated instructor_availability.csv")

print("\n" + "="*50)
print("Fixes applied! Now run:")
print("python debug.py")
print("="*50)