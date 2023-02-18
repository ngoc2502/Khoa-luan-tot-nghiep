import csv
import os

def del_empty(inpath,outpath):
    with open(inpath, 'r', newline='') as f_in, open(outpath, 'w', newline='') as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)
        rows = [row for row in reader if any(field.strip() for field in row)]  # use list comprehension to filter rows
        f_in.seek(0)  # reset the file pointer to the beginning of the file
        writer.writerows(rows)  # write filtered rows to output file

    os.replace(outpath, inpath)

del_empty("./fulllist01.csv","./fulllist01_out.csv")