def new_data_set(train, test):
    """merge old train and test data set and create a new one"""
    import random 
    new_train = open('output/link_prediction/new_train.csv', 'w')
    new_test = open('output/link_prediction/new_test.csv','w')

    train_lines = train.readlines()
    test_lines  = test.readlines()
    all_lines = train_lines[1:] + test_lines[1:]

    print(train_lines[0], end='', file=new_train)
    print(test_lines[0], end='', file=new_test)

    new_test_lines_index = random.sample(range(len(all_lines)), len(test_lines[1:]))
    for index in new_test_lines_index:
        print(all_lines[index], end='', file=new_test)
    new_train_lines_index = set(range(len(all_lines)))-set(new_test_lines_index)
    for index in new_train_lines_index:
        print(all_lines[index], end='', file=new_train)

if __name__ == '__main__':
    train = open('output/link_prediction/train_feature.csv', 'r')
    test = open('output/link_prediction/test_feature.csv', 'r')
    new_data_set(train, test)
