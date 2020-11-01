from numpy import genfromtxt


def GetUnique(lst):
    unique_lst = []
    for i in lst:
        is_unique = True
        for j in unique_lst:
            if(i == j):
                is_unique = False
        if is_unique:
            unique_lst.append(i)

    return unique_lst


#P(x) = elem
#input: class values, class constant value
#output: value, str format1, str format2
def Prob(lst, elem):
    counter = 0
    for i in lst:
        if i == elem:
            counter+=1

    str_output1 = str(counter) + '/' + str(len(lst))
    str_output2 = 'P(x = ' + str(elem) + ')'
    return (counter/len(lst), str_output1, str_output2)

#P(x = val| expected)
#input: class value, target values, class constant value, target constant value
#output: value, str format1, str format2
def  ConditionalProb(class_lst, target_lst, class_value, target_value):
    total_class_value = 0 #laplace
    total_target_value = 0

    for i in range(len(target_lst)):
        if target_lst[i] == target_value:
            total_target_value+=1
            if class_lst[i] == class_value:
                total_class_value+=1
    
    str_output1 = str(total_class_value) + '/' + str(total_target_value)
    str_output2 = 'P(x = ' + str(class_value) + '| ' + str(target_value) + ')'
    return (total_class_value/total_target_value, str_output1, str_output2)

#new_object tuple(values, class_indexes)
def NaiveBayes(new_object, dataset, target_lst):
    target_values = GetUnique(target_lst)
    v_object, i_object = new_object
    result_lst = [] 
    
    #generate all object's probabilities for each target from unique value list 
    for i in target_values:
        tmp_lst = []
        nxt_object = 0
        for j in i_object:
           tmp_lst.append( ConditionalProb(ConvertColumnToList(dataset, j), target_lst, v_object[nxt_object], i) )
           nxt_object+=1
        tmp_lst.append(Prob(target_lst, i))
        result_lst.append( tmp_lst[:] )
   
    
    output_lst = []
    bottom = 0
    str_condprobs = ''
    
    #iterate probabilities get values to divide top/bottom 
    for i in range( len(result_lst) ):
        
        #strings
        top = 1
        str_top = 'P('+ str(target_values[i]) + '|'
        str_bottom = '/ (P(' 
        for j in range(len(i_object)):
            str_bottom += 'x' + str(i_object[j]) + '=' + str(v_object[j]) + '+'
            str_top += 'x' + str(i_object[j]) + '=' + str(v_object[j]) + ', '
        str_top = str_top[:len(str_top)-2] + ') = ('

        #top part multiply
        for j in result_lst[i]:        
            v, s1, s2 = j
            top *= v
            
            #strings
            str_top += ' ' + str(s1) + ' X'
            str_condprobs += s2 + '=' + str(v) + '\n'
        
        #bottom part sum
        bottom += top

        #output
        str_top = str_top[:len(str_top)-1] + ')'
        str_bottom = str_bottom[:len(str_bottom)-1] + '))'
        output_lst.append( [top, 0 , (str_top + str_bottom)] )
        
    
    #when bottom is ready, insert it
    for out in output_lst:
        out[1] = bottom
        
    #calculate naive bayes
    bayes = []
    str_output =  '******* Conditional Probabilities **********\n' + str_condprobs + '\n********** Naive Bayes ********** '
    for n in output_lst:
        naive = n[0]/n[1]
        bayes.append(naive)
        str_output += '\n' +  n[2] + '  =  ' + str(naive) 

    return bayes, str_output


def ConvertColumnToList(dataset, index):
    lst = []
    for i in range(len(dataset)):
        lst.append(dataset[i][index])

    return lst


#read dataset
file_name = 'base.csv'
dataset = genfromtxt(file_name, delimiter = ';')

print(dataset)
column_target = ConvertColumnToList(dataset, 3)
b,s = NaiveBayes( ([0,1,0], [0,1,2]), dataset, column_target)
print(s)
