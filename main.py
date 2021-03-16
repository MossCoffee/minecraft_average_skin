import requests
import shutil
from PIL import Image
import colorsys
from enum import Enum
from collections import defaultdict

class Color(Enum):
    BLACK = 0
    WHITE = 1
    GREY = 2
    RED = 3
    ORANGE = 4
    YELLOW = 5
    GREEN = 6
    CYAN = 7
    BLUE = 8
    MAGENTA = 9
    MULTI = 10

def populateIds():
    output = []
    fileName = "id_file"
    with open(fileName, 'r') as f:
        for line in f:
            output.append(line.rstrip())

    return output

def downloadSkin(skinID):

    #download a single skin
    #www.minecraftskins.com or https://namemc.com
     
    url = 'https://namemc.com/texture/' + skinID + ".png?v=2"
    r = requests.get(url, stream=True)
    fileName = "minecraft_temp/" + str(skinID) + ".png"
    if(r.status_code == 200):
        #img.png is probably the file name, can likely be overriden
        with open(fileName, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    return str(skinID) + ".png"

def getColorGroup(pixel):
    ((R, G, B)) = pixel
    #print("R: " + str(R) + " G: " + str(G) + " B: " + str(B))
    ((h,l,s)) = colorsys.rgb_to_hls(R/255, G/255, B/255)
    h = h * 360
    #print("h: " + str(h) + " l: " + str(l) + " s: " + str(s))
    if l < .2: return Color.BLACK
    if l > .8: return Color.WHITE
    
    if s < 0.25: return Color.GREY

    if h < 15: return Color.RED
    if h < 38: return Color.ORANGE
    if h < 75: return Color.YELLOW
    if h < 150: return Color.GREEN
    if h < 210: return Color.CYAN
    if h < 270: return Color.BLUE
    if h < 330: return Color.MAGENTA
    return Color.RED

def getColorFromSubsection(img, x, y, width, height):
    pixelGroups = {}
   # print("(" + str(x) + "," + str(y) + ") - (" + str(x + width) + "," + str(y + height) + ")")
    for xCoord in range(x, x + width):
        for yCoord in range(y, y + height):
            #print("(" + str(xCoord) + "," + str(yCoord) + ")")
            group = getColorGroup(img.getpixel((xCoord, yCoord)))
            currval = 1
            if group in pixelGroups:
                currval += pixelGroups[group]
            pixelGroups[group] = currval

    output = -1
    currentMax = -1
    for key, value in pixelGroups.items():
        if currentMax < value:
            output = key
            currentMax = value

    return output #returns a group color

def getMainColor(skin):
    #first, split everything into parts ie, arms, legs, jacket etc
    #Then determine the average color of that limb
    #Then determine which color is the "most"
    #Must have a low variance to have a main "color"
    #hair & face are seperate & weighted lower
    #torso & jacket are weighted higher
    #Limbs are counted as normal
    colorDictionary = defaultdict(int)
    

    #hair
    headSize = ((8,8))
    colorDictionary[getColorFromSubsection(skin, 8, 0, *headSize)] += .25
    colorDictionary[getColorFromSubsection(skin, 0, 8, *headSize)] += .25
    colorDictionary[getColorFromSubsection(skin, 16, 8, *headSize)] += .25
    colorDictionary[getColorFromSubsection(skin, 24, 8, *headSize)] += .25
    print("hair")
    #face
    colorDictionary[getColorFromSubsection(skin, 8, 8, *headSize)] += .25
    print("face")
    #limbs
    limbSize = ((16,12))
    jointSize = ((8,4))
    
    #right leg
    colorDictionary[getColorFromSubsection(skin, 0, 20, *limbSize)] += .8
    colorDictionary[getColorFromSubsection(skin, 4, 16, *jointSize)] += .2

    #left leg
    colorDictionary[getColorFromSubsection(skin, 16, 52, *limbSize)] += .8
    colorDictionary[getColorFromSubsection(skin, 20, 48, *jointSize)] += .2

    #right arm
    colorDictionary[getColorFromSubsection(skin, 40, 20, *limbSize)] += .8
    colorDictionary[getColorFromSubsection(skin, 44, 16, *jointSize)] += .2

    #left arm
    colorDictionary[getColorFromSubsection(skin, 32, 52, *limbSize)] += .8
    colorDictionary[getColorFromSubsection(skin, 36, 48, *jointSize)] += .2
    print("limbs")
    #torso
    torsoSize = ((24,12))
    hipSize = ((8,4))
    colorDictionary[getColorFromSubsection(skin, 16, 20, *torsoSize)] += (4 * .8)
    colorDictionary[getColorFromSubsection(skin, 20, 16, *hipSize)] += (4 * .2)
    print("torso")
    print(colorDictionary)

    #iterate over dictionary, find max color value & return it


def analyzeSkin(skin):
    #returns the group that it belongs to 
    #By primary color, eye shap

    #Figure out the primary color
    

    #colors have arbitrary ranges for where "red" stops and where "orange" starts for instance

    #Then figure out the eye pattern
    #"steve" or "classic" eyes
    #"vertical eyes" see wilbur soot's skin
    #"anime eyes" what it says on the tin
    #"No eyes" see dream's skin

    #each id contains the data of both of these traits

    return getMainColor(skin) #group ID

def mergeSkin(skin, groupId):
    if skin or groupId:
        skin = groupId
    return
    
def skinMixer(imgInput, composite, acc):
    img = imgInput.convert("RGBA")
    (width, height) = (img.width, img.height)
    composite = composite.resize((width,height))
    alpha = 1 / acc
    #I don't think this is working properly
    #fill this in later
    #Skin data contains a num (0-1) for each generated image
    #Take that image & scale basied on the sum of transparentcies
    #Should create a completely opaque image
    return Image.blend(composite, img, alpha=alpha)

def getOutput(group):
    #Get the proper output file to merge the image with 
    return group

def main():
    #Make the "average" skin amonugst skins on skindex
    #this will eventually be a webapp (probably written rails in ruby?)
    #here's the deal
    #download a bunch of skins from 
    #www.minecraftskins.com or https://namemc.com
    #this is probably a webtrawler?
    #this returns a bunch of minecraft skins somehow
    skinUrl = "testskin.png"
    


    idList = populateIds()
    #to do: make a copy of the starting file 

    #open output image
    output = Image.open("output.png").convert("RGBA")
    acc = 1
    for id in idList:
        #skin = downloadSkin(id) #This is passed some form of id that lets it download the skin
        #Analyze the skin
        #where the magic happens
        #groupId = analyzeSkin(skin)
        skinUrl = "minecraft_temp/" + str(id) + ".png"
        skin = Image.open(skinUrl).convert("RGB")
        group = analyzeSkin(skin)
        
        #pass group into output 
        output = skinMixer(skin, getOutput(group), acc) # pass f in in
        acc += 1
        #Skins are sorted into groups and then averaged on to their group's collected image
        #mergeSkin(skin, groupId)

    output.save("output.png", "png")
    #Now we've got the skins merged into groups, 
    #We need an interface for making the skin
    #customSkinData = [0, 1, 1, 0]
    #Skin image is a png file of the created skin
    #skinImage = skinMixer(customSkinData)

    #then we make a web interface to tie it all together!

if __name__ == "__main__":
    main()