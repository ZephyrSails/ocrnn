import csv
import sys
import editdistance
import types

right = {}
wrong = {}

'''
This python program is used to transfer data to form the set of (predict_data, actual_data)
for training of RNN
the output example:
("Decision 1 End Process Process 3 Process 4 Process 5", "Decision 1; End; Process1; Process2; Process 3;
Process 4; Process 5; Start")
'''

def getclosestlist(right_list, ocr_list):

    if type(right_list) is types.StringType:
        right_list = [right_list]
    if type(ocr_list) is types.StringType:
        ocr_list = [ocr_list]
    tword = ''
    result = []
    min_num = 1000
    for ele1 in right_list:
        for ele2 in list(ocr_list):
            dist = (int)(editdistance.eval(ele1,ele2))
            if dist < min_num:
                min_num = dist
                tword = ele2
            else:
                pass
        result.append(tword)
    return result
        
        


def ge_train_correct(rightcsvdir, ocr_result_dir):
    '''

    :param rightcsvdir: the csv data set of actual data
    :param ocr_result_dir: data set of predicted data
    :return: write to file traindata.txt

    '''
    with open(rightcsvdir) as rightfile:
        reader = csv.reader(rightfile)
        id = ''
        for row in reader:
            try:
                [id, content] = filter(None, row)
            except ValueError:
                print 'warning1 the value is:' + str(id)
                break
            content = content.replace('Null','').replace('\r\r','@').replace(';','').split('@')
            right[id] = content


    with open(ocr_result_dir) as wrongfile:
        reader = csv.reader(wrongfile)
        for row in reader:
            [id, content] = row[0].split('\t')
            content = sorted(content.split(';'))
            wrong[id] = content

    file_object = open('traindata.txt', 'w')

    for (k, v) in right.items():
        try:
            ocr_target = getclosestlist(v, wrong[k])
        except ValueError:
            print 'warning2'
            break
        results = ';'.join(ocr_target) + '","' + ';'.join(v)
        file_object.write('("' + results + '")' + '\n')
    print 'suceess!'
    file_object.close()




def main():
    if len(sys.argv) != 3:
        print "please enter the following information in the order of:"
        print "python traindata.py <correctpath> <wrongpath>"
        sys.exit()
    else:
        rightcsvdir = sys.argv[1]
        ocr_result_dir = sys.argv[2]
        ge_train_correct(rightcsvdir,ocr_result_dir)

if __name__ == '__main__':
    #main()
    ge_train_correct('./right.csv', './ocr.csv')


