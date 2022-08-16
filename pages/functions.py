def unique(list):
    unique_list = []

    for x in list:
        if x not in unique_list:
            unique_list.append(x)

    return unique_list

def prepare_choices(list):
    choices = []
    i = 0

    for x in unique(list):
        choices.append((x[0],x[0]))
        i+=1
    
    return choices
