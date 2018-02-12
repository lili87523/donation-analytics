import sys
import datetime
import bisect
import math

#Read In Percentile
with open(sys.argv[2], 'r') as inputPercentile:
    percentile = int(inputPercentile.readline())

#Consideration 6: invalid date
def invalid_date(str):
    try:
        datetime.datetime.strptime(str, "%m%d%Y")
        return False
    except ValueError:
        return True


#Read In Needed Fields
donors = set()
validRecords = {}

with open(sys.argv[3], 'w+') as output:
    with open(sys.argv[1], 'r') as inputItcont:
       for line in inputItcont.readlines():
            fields = line.split("|")
            #CMTE_ID = fields[0]; NAME = fields[7]; ZIP = fields[10]; DATE = fields[13]; AMOUNT = fields[14]; OTHER_ID = fields[15]
            if fields[0] == '' or fields[7] == '' or len(fields[10]) < 5 or invalid_date(fields[13]) or fields[14] == '' or fields[15] != '':
                continue
            else:
                cmte_id = fields[0]
                name = fields[7]
                zip = fields[10][0:5]
                year = fields[13][4:]
                currentAmount = fields[14]
                currentDonor = (zip, name)

                if currentDonor in donors:
                    currentKey = (cmte_id, zip, year)
                    if currentKey in validRecords.keys():
                        prevAmounts = validRecords[currentKey]
                        bisect.insort(prevAmounts, int(currentAmount))
                        totalAmount = sum(prevAmounts)
                        totalNumber = len(prevAmounts)
                        position = int(math.ceil(percentile * 1.0 / 100 * totalNumber))
                  
                        output.write(cmte_id + "|" + zip + "|" + year + "|" + str(prevAmounts[position - 1]) + "|" + str
                            (totalAmount) + "|" + str(totalNumber) + '\n')
                    else:
                        value = [int(currentAmount)]
                        validRecords[currentKey] = value
                        output.write(
                            cmte_id + "|" + zip + "|" + year + "|" + str(currentAmount) + "|" + str(
                                currentAmount) + "|" + '1' + '\n')

                else:
                    donors.add(currentDonor)
