import argparse

parser = argparse.ArgumentParser(description = 'Commands for this Program')
parser.add_argument('--location', help = 'Enter the location')
args = parser.parse_args()
Loc_String = args.location

List = Loc_String.split(":")
print(List)
print("Longi :", List[0], end="\n")
print("Lati :", List[1], end='\n')
