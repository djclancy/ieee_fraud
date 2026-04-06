import csv


## Check if files are sorted
def sorted_and_in_order(filename):
    '''Checks to see if the first column of csv file name (file)'''
    is_first_line = True
    hold = None
    order = None
    output = True
    with open(filename) as f:
        for line in f:
            words = line.split(',')
            id = words[0]
            if is_first_line:
                is_first_line=False
                continue
            id = int(id)
            if hold is None:
                hold = id
            else:
                if order is None:
                    order = (id>hold)
                elif order:
                    if id < hold:
                        output = False
                else:
                    if id > hold:
                        output = False
    return output, order

'''
# Checks to make sure all files are in ascending order
csv_files = ['raw_data/'+a+'_'+b+'.csv' for a in ['train','test'] for b in ['transaction', 'identity']]
orders = []
sorts = []
for file in csv_files:
    is_sorted, order = sorted_and_in_order(file)
    sorts.append(is_sorted)
    orders.append(order)
print(is_sorted)
print(orders)
'''

csv_files = ['raw_data/'+a+'_'+b+'.csv' for a in ['train','test'] for b in ['transaction', 'identity']]
csv_train = csv_files[:2]
csv_test = csv_files[2:]
csv_files = {'train':csv_train, 'test':csv_test}

for traintest, csv_li in csv_files.items():
    l_name, r_name = csv_li
    primary_key = 'TransactionID'
    out_file_name = 'raw_data/' + traintest + '_merge.csv'
    with open(l_name,'r', newline='') as l_file, \
        open(r_name, 'r', newline='') as r_file, \
        open(out_file_name, 'w', newline='') as out_file:

        reader_l, reader_r = csv.DictReader(l_file),csv.DictReader(r_file) 

        rows_l, rows_r = iter(reader_l), iter(reader_r)

        columns_l, columns_r  = reader_l.fieldnames, reader_r.fieldnames


        output_cols = columns_l + [r for r in columns_r if r != primary_key]

        writer = csv.DictWriter(out_file, fieldnames=output_cols)
        writer.writeheader()
        
        rowL = next(rows_l, None)
        rowR = next(rows_r, None)
        


        while rowL is not None or rowR is not None:
            line = {col_name:'' for col_name in output_cols}
            if rowL is None:
                line.update(rowR)
                rowR = next(rows_r, None)
            elif rowR is None:
                line.update(rowL)
                rowL = next(rows_l, None)
            else:
                keyL, keyR = int(rowL[primary_key]), int(rowR[primary_key])
                if keyL == keyR:
                    line.update(rowL)
                    line.update({c:v for c,v in rowR.items() if c!= primary_key})
                    rowL = next(rows_l, None)
                    rowR = next(rows_r, None)
                elif keyL<keyR:
                    line.update(rowL)
                    rowL = next(rows_l, None)
                else: 
                    line.update(rowR)
                    rowR = next(rows_r, None)
            writer.writerow(line)
