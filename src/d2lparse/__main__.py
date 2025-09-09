import csv
import argparse
from enum import Enum

class Format(Enum):
   Email = {
      "name": "email",
      "fields": ["Email"]
   }
   Hostbin = {
      "name": "hostbin",
      "fields": ["Last Name", "First Name", "OrgDefinedId"]
   }
   Names = {
      "name": "names",
      "fields": ["Last Name", "First Name"]
   }

parser = argparse.ArgumentParser(description="Parse a CSV exported from D2L into various useful formats")
formats = parser.add_mutually_exclusive_group(required=True)

parser.add_argument("path", help="path to csv file", type=open)
parser.add_argument("-o", "--output", help="name of output file", type=str)

formats.add_argument("-b", "--hostbin", action="store_true", help="output in the format requested for hostbin users")
formats.add_argument("-n", "--names", action="store_true", help="output first and last names")
formats.add_argument("-e", "--email", action="store_true", help="output a list of emails seperated by semi-colon")
formats.add_argument("--format", choices=[x.value["name"] for x in Format], help="specify the desired output format")

def check_csv(csv_fields, required_fields):
   missing = [x for x in required_fields if x not in csv_fields]
   if missing:
      print("Missing fields in csv:", missing)
      exit()

def main():
   args = parser.parse_args()
   csvfile = csv.DictReader(args.path)

   format = (
      Format.Email if args.email or args.format == "email"
      else Format.Hostbin if args.hostbin or args.format == "hostbin" 
      else Format.Names
   )

   check_csv(csvfile.fieldnames, format.value["fields"])

   lines = []

   if format == Format.Email:    
      for row in csvfile:
         lines.append(row["Email"])
   elif format == Format.Names: 
      for row in csvfile:
        lines.append(f"{row['First Name']} {row['Last Name']}")
   else:
      for row in csvfile:
         lines.append(f"{row["First Name"]} {row["Last Name"]},{row["OrgDefinedId"]}")
      
   output = "\n".join(lines)

   if args.output:
      file = open(args.output, "w")
      file.write(output)
   else:
      print(output)


if __name__ == "__main__":
   main()



   