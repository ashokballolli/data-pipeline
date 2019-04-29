
def write(filename, content):
    myfile = open(filename, 'a')
    myfile.write(content+'\n')

    # Close the file
    myfile.close()

