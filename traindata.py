import csv
import sys


right = {}
wrong = {}

'''
This python program is used to transfer data to form the set of (predict_data, actual_data)
for training of RNN
the output example:
("Decision 1 End Process Process 3 Process 4 Process 5", "Decision 1; End; Process1; Process2; Process 3;
Process 4; Process 5; Start")
'''
def mergedic(dic2, dic1):
    '''
    used to merge two dictionary
    :param dic2: the first dictionary
    :param dic1: the second dictionary
    :return:
    '''
    for (k, v) in dic1.items():
        helper = []
        if dic2.has_key(k):

            helper.append(dic1[k])
            helper.append('"')
            helper.append(',')
            helper.append('"')
            helper.append(dic2[k])

            dic2[k] = ''.join(helper)
        else:
            raise NameError
    return dic2


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
                print 'warning! the value is:' + str(id)
                break
            content = ';'.join(content.replace('Null','').replace('\r\r','@').replace(';','').split('@'))
            right[id] = content


    with open(ocr_result_dir) as wrongfile:
        reader = csv.reader(wrongfile)
        for row in reader:
            [id, content] = row[0].split('\t')
            content = sorted(content.split(';'))
            wrong[id] = ' '.join(content)

    file_object = open('traindata.txt', 'w')
    for (k, v) in mergedic(right, wrong).items():
        file_object.write('("' + v + '")' + '\n')
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
    main()

