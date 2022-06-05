f = open('myfile.txt', 'r')

datalist = f.readlines()
print (datalist[0])
print (datalist[1])
print (datalist[2])

f.close()


# f = open('myfile.txt', 'r')

# datalist = f.readlines()
# for data in datalist:
#   print(data)

# f.close()