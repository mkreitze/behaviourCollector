#Behaviour collector, made by Matthew Kreitzer for level-map generation As of October 2020

#To use the code, simply put all behaviour records into the same directory as this file
#It will then generate a folder showcasing the level map, represented by a png, of each behaviour recorded 

#A Behaviour recrod is a text file that sorts a set of score matrices by (normally weak) behavioural equivalence
import os
import linecache
import libFBCAGen

#global inits (stolen from libFBCAGen)
CALength=libFBCAGen.CALength #Length of the generated image (for min use 5)
CAWidth=libFBCAGen.CAWidth #Width of the generated image (for min use 4)
useMinMap=libFBCAGen.useMinMap #checks if youre using 'min' map
useImages=libFBCAGen.useImages #checks if you want images
numOfGens=libFBCAGen.numOfGens #number of generations
numOfStates=libFBCAGen.numOfStates #number of states (good until 10)


#get a list of all files in the directory
allFileNames=os.listdir(os.getcwd())
curDirectory=os.getcwd()
#Fix the noise of the FBCA
CAMapInit=[]
CAMapInit=libFBCAGen.initCA(CAMapInit)
for fileName in allFileNames:
    #check if the last element is t, checks for .txt (could be done better)
    lastIndex=len(fileName)-1
    if(fileName[lastIndex]=='t'):
        curFile=open(fileName,"r")
        for idx,line in enumerate(curFile):
            #since every group of behaviours has “New behaviour set:X ” written before, check for : 
            if (line.find(':') != -1):
                #Attempts to make the directory based upon behaviourNum
                behaviourNum=line.split(':')
                #Ex: ['New behaviour set', '72 \n']
                #add in number by taking the second element
                temp=fileName.split('.')
                d=curDirectory+"/"+str(temp[0][:-1])+"file"+"/"
                libFBCAGen.createFolder(d)
                #Ex: Generates directory 72

                #Next we need to extract a score matrix from this behaviour set
                #This is done by taking the next line
                protoScoreMatrix=linecache.getline(fileName, idx+2).split(' ')
                #Ex: ['Points', 'x>9.59999999999993', 'y>0.19999999999976348', 'with', '[12.592848008753737,', '-12.192848008754211,', '-7.0071519912456495,', '6.6071519912461225]\n']
                #Only the 4,5,6 and 7th element are needed (for the two state case)
                #They also need to be cleaned up
                scoreMatrix=[]
                scoreMatrix.append(float(protoScoreMatrix[4][1:(len(protoScoreMatrix[4])-1)]))
                scoreMatrix.append(float(protoScoreMatrix[5][0:(len(protoScoreMatrix[5])-1)]))
                scoreMatrix.append(float(protoScoreMatrix[6][0:(len(protoScoreMatrix[6])-1)]))
                scoreMatrix.append(float(protoScoreMatrix[7][0:(len(protoScoreMatrix[7])-2)]))
                #Ex: ['12.592848008753737', '-12.192848008754211', '-7.0071519912456495', '6.6071519912461225']
                #Generate the FBCA
                CAMap=[]
                CAMap=libFBCAGen.copyOver(CAMapInit)
                gif=[]
                for n in range(numOfGens):
                    if (useImages==1):
                        gif.append(libFBCAGen.genIm(CAMap,n,d,behaviourNum[1][:-1]))
                    CAMap=libFBCAGen.updateMap(CAMap,scoreMatrix)
                if (useImages==1):
                    gif.append(libFBCAGen.genIm(CAMap,n,d,behaviourNum[1][:-1]))
                print("Finished "+str(behaviourNum[1][:-1]))
                if (useImages==1):
                    gif[0].save(d+str(behaviourNum[1][:-2])+'.gif',save_all=True,append_images=gif[1:],optimize=False,duration=100,loop=0)
    print("Finished "+str(fileName))