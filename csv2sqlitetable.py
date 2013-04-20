
import csv
import sys
import sqlite3

def scrub(str):
    return ''.join( chr for chr in str if chr.isalnum() )

if len(sys.argv) < 4:
    print "Usage:"
    print "\tcsv2sqlitetable.py csvfilename sqlitefilename sqlitetablename [headerRow] [primaryKey]"
    print ""
    print "headerRow is the number of lines to ignore at the start of the file.  Use this if the header is not on the first line"
    print "Defaults to 0"
    print ""
    print "primaryKey is the 0-based column number of the column which should be interpreted as the primary key."
    print "if this is not specified then no primary key is added to the created table"
    sys.exit(0)



csvFilename = sys.argv[1]
sqliteDb = sys.argv[2]
sqliteTable = sys.argv[3]
headerRow = 0
if len(sys.argv) > 4:
    headerRow = int(sys.argv[4])

with open(csvFilename, "rb") as csvFile:
    csvreader = csv.reader(csvFile, delimiter=',', quotechar='"')
    readCount = 0
    
    insertColumnFragment = ""
    insertParamsFragment = ""
    colCount = 0
    
    conn = sqlite3.connect(sqliteDb)
    conn.text_factory = str
    for row in csvreader:
        if readCount == headerRow:
            #parse the header and create the table
            sqlFragment = "("
            insertParamsFragment = "("
            colCount = len(row)
            for i in range(colCount):
                if i == 0:
                    sqlFragment += scrub(row[i]) 
                    insertParamsFragment += "?"
                else:
                    sqlFragment += " , " + scrub(row[i]) 
                    insertParamsFragment += ",?"
            sqlFragment += ")"
            insertParamsFragment += ")"
            insertColumnFragment = sqlFragment
            
            sqlquery = "CREATE TABLE  " + scrub(sqliteTable) + " " + sqlFragment
            conn.execute(sqlquery)
            
        elif readCount > headerRow:
            #add or trim length items from the row so it matches the number of items in the header
            while len(row) < colCount:
                row.append("")
            while len(row) > colCount:
                row.pop()
            
            sqlquery = "INSERT INTO " + scrub(sqliteTable) + " " + insertColumnFragment + " VALUES " + insertParamsFragment
            conn.execute(sqlquery, row)
            if readCount % 10000 == 0:
                print "Inserted " + str(readCount) + " rows"
        else:
            #skip the row
            print "Skipped row " + str.join("", row)
            
        readCount += 1

    conn.close()
        
        