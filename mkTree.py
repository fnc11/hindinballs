class Tree(object):
    # "Generic tree node."
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

    def printTree(self):
        assert isinstance(self, Tree)
        stck = [self]
        while(True):
            if len(stck) != 0:
                temp = stck.pop(0)
                print(temp.name)
                if len(temp.children) > 0:
                    for child in temp.children:
                        stck.insert(0, child)
            else:
                break

    def printLevelOrder(self):
        assert isinstance(self, Tree)
        que = [self]
        nums_at_level = 1
        levelNum = 0
        # maxLevel = -1
        levelDict = {0:[]}
        for i in range(1,15):
            levelDict[i]=[]
        count = 0
        while(True):
            if nums_at_level == 0:
                # print("level: "+str(levelNum))
                # if levelNum > maxLevel:
                #     maxLevel = levelNum
                levelNum += 1
                nums_at_level = count
                count = 0

            if len(que) != 0:
                nums_at_level -= 1
                temp = que.pop(0)
                # print(temp.name)
                levelDict[levelNum].append(temp.name)
                if len(temp.children) > 0:
                    for child in temp.children:
                        que.append(child)
                        count += 1
            else:
                break
        return levelDict
        # print(maxLevel)



root = Tree("root")
allNodes = {"root": root}

set2Word = {}
word2Set = {}

with open("set2WordV.txt","r") as s2w:
    cont = s2w.read()
    sets = cont.split("$")
    for set in sets:
        pairs = set.split(":")
        num = pairs[0]
        word = pairs[1]
        set2Word[num] = word
        word2Set[word] = num

# final cleansing of the paths
paths = []
clean_paths = []
with open("tree_struct.txt", 'r') as tree_struct:
    struct_cont = tree_struct.read()
    paths = struct_cont.split("$")
    # count = 0
    for path in paths:
        tokens = path.split("<-")
        num_of_tokens = len(tokens)
        new_path = tokens[0]
        for i in range(1, num_of_tokens):
            if tokens[i] in set2Word.keys():
                new_path += "<-" + tokens[i]
        clean_paths.append(new_path)

    for path in clean_paths:
        tokens = path.split("<-")
        # print(tokens)
        num_tokens = len(tokens)
        # saving prev_token to save it's child if they don't exist already
        prev_token = tokens[num_tokens - 1]
        # remember to leave last set, need to replace it with actual word
        for i in range(0, num_tokens - 2):
            name = str(tokens[num_tokens - 1 - i])
            # to avoid index out of bound error
            if i > 0:
                prev_token = tokens[num_tokens - i]
            if name in allNodes.keys():
                continue
            else:
                # create new node and save it's mapping in the allNodes dict
                temp = Tree(name)
                allNodes[name] = temp
                if i == 0:
                    # if it's the node that goes below root
                    allNodes["root"].add_child(temp)
                else:
                    # if it is some other node's child, other than root(prev_token's)
                    allNodes[prev_token].add_child(temp)
        # now for the last node, as word
        name = str(tokens[0])
        temp = Tree(name)
        allNodes[name] = temp
        # if the word is not directly attached to the root
        if num_tokens >= 3:
            allNodes[tokens[2]].add_child(temp)
        else:
            allNodes["root"].add_child(temp)

levelDict = root.printLevelOrder()
# print(levelDict)



# print(wordAndOrderDict)
# Now replace set in the levelDict with word and sort them, and replace the -1 in the wordAndOrderDict
# with correct place
setOrderNum = {'root': 1 }
with open("sameLevelWords.txt", "w") as slw:
    stck =[root]
    while(True):
        if len(stck) != 0:
            temp = stck.pop(0)
            if len(temp.children) > 0:
                o_list = temp.children
                c_list  = []
                for child in o_list:
                    word_name = child.name
                    if child.name in set2Word.keys():    
                        word_name = set2Word[child.name]
                    c_list.append(word_name)
                    stck.append(child)
                c_list.sort()
                k=0
                for i in c_list:
                    k=k+1
                    if i in word2Set.keys():
                        setOrderNum[word2Set[i]] = k
                    else:
                        setOrderNum[i] = k
        else:
            break
        slw.write("\n\n")

# printing cat codes of all the words in a file
with open("catCodes.txt", "w") as ctcd:
    # count = 0
    for path in clean_paths:
        tokens = path.split("<-")
        num_of_tokens = len(tokens)
        word = tokens[0]
        if tokens[0] in word2Set.keys():
            sen = str(setOrderNum[word2Set[tokens[0]]])
        # discussion need to be done here
        elif tokens[0] in setOrderNum.keys():
            # count += 1
            sen = str(setOrderNum[tokens[0]])
        else:
            continue

        for i in range(2, num_of_tokens):
            sen = str(setOrderNum[tokens[i]])+" "+sen

        # root order for every word
        # need to add special case for root*
        sen = "1 "+sen
        for j in range(0, 13-num_of_tokens):
            sen += " 0"
        ctcd.write(word+" "+sen+"\n")
    # print(count)




# root.printTree()
# printing word sense children file as English
with open("wordSenseChildren.txt","w") as wsc:
    stck = [root]
    while (True):
        if len(stck) != 0:
            temp = stck.pop(0)

            if temp.name in set2Word.keys():
                wsc.write(set2Word[temp.name])
            else:
                wsc.write(temp.name)

            if len(temp.children) > 0:
                for child in temp.children:
                    stck.insert(0, child)
                    if child.name in set2Word.keys():
                        wsc.write(" "+set2Word[child.name])
                    else:
                        wsc.write(" "+child.name)

            wsc.write("\n")
        else:
            break
