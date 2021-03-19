import requests
import shutil
from PIL import Image
import colorsys
from enum import IntEnum
from collections import defaultdict

class Color(IntEnum):
    NONE = -1
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

class Version(IntEnum):
    NOT_SKIN = -1
    OLD = 0
    CURRENT = 1

class SkinGroup:
    color = Color.NONE
    version = Version.NOT_SKIN

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
    ((h,l,s)) = colorsys.rgb_to_hls(R/255, G/255, B/255)
    h = h * 360
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
    for xCoord in range(x, x + width):
        for yCoord in range(y, y + height):
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
    #face
    colorDictionary[getColorFromSubsection(skin, 8, 8, *headSize)] += .25
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
    #torso
    torsoSize = ((24,12))
    hipSize = ((8,4))
    colorDictionary[getColorFromSubsection(skin, 16, 20, *torsoSize)] += (4 * .8)
    colorDictionary[getColorFromSubsection(skin, 20, 16, *hipSize)] += (4 * .2)

    #iterate over dictionary, find max color value & return it
    maxValue = -1
    outputColor = Color.NONE
    for ((key, value)) in colorDictionary.items():
        if maxValue < value:
            maxValue = value
            outputColor = key
    return outputColor


    
def analyzeSkin(skin):
    oldSkinSize = ((64, 32))
    newSkinSize = ((64, 64))
    output = SkinGroup()
    #is this an old or new skin? (check image size)
    if skin.size == oldSkinSize :
        output.version = Version.OLD
    elif skin.size == newSkinSize:
        output.version = Version.CURRENT
        output.color = getMainColor(skin) #group ID
    
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

    return output
    
def skinMixer(imgInput, composite, acc):
    img = imgInput.convert("RGBA")
    (width, height) = (img.width, img.height)
    composite = composite.resize((width,height))
    alpha = 1 / acc
    #fill this in later
    #Skin data contains a num (0-1) for each generated image
    #Take that image & scale basied on the sum of transparentcies
    #Should create a completely opaque image
    return Image.blend(composite, img, alpha=alpha)

def getOutput(colorImages, group):
    output = colorImages.get(group.color)
    if output == None :
        skinUrl = "intermediates/group_" + str(group.color) + ".png"
        colorImages[group.color] = Image.open(skinUrl).convert("RGBA")
        output = colorImages[group.color]
    return output

def saveOutput(colorImages, img, group):
    savingLocation = colorImages.get(group.color)
    if savingLocation != None : #You've used this function wrong if we get here, but so be it
        colorImages[group.color] = img

def saveAll(colorImages):
    for ((color, image)) in colorImages.items():
        print("saving: " + str(color))
        skinUrl = "intermediates/group_" + str(color) + ".png"
        image.save(skinUrl, "png")

def generateSkin(settings):
    #add up to 1 or 100?
    #add up to 100
    output = Image.open("output.png").convert("RGBA")
    imagesMixed = 0
    for value in range(Color.BLACK, Color.MULTI):
        mixingAmount = 0
        if settings[value] != 0:
            mixingAmount = settings[value] / (imagesMixed + settings[value])
            imagesMixed += settings[value]
            skinUrl = "intermediates/group_" + str(Color(value)) + ".png"
            intermediate = Image.open(skinUrl).convert("RGBA")
            output = Image.blend(output, intermediate, mixingAmount).convert("RGBA")
    
    output.save("output.png", "png")
    output.show()
    
            


def main():
    #Make the "average" skin amonugst skins on skindex
    #this will eventually be a webapp (probably written rails in ruby?)
    #here's the deal
    #download a bunch of skins from 
    #www.minecraftskins.com or https://namemc.com
    #this is probably a webtrawler?
    #this returns a bunch of minecraft skins somehow

    
    settings = [] #figure out what the settings need to be
    colorImages = {}
    colorIterator = defaultdict(int)

    ActivateSkinDownload = False
    GenerateIntermediates = False
    idList = []

    if(GenerateIntermediates):
        idList = populateIds()

    #open output image
    #output = Image.open("output.png").convert("RGBA")
    for id in idList:
        if ActivateSkinDownload :
            downloadSkin(id) #This is passed some form of id that lets it download the skin
        #Analyze the skin
        #where the magic happens
        print("Processing skin #" + str(id))
        skinUrl = "minecraft_temp/" + str(id) + ".png"
        skinBase = Image.open(skinUrl)

        skin = skinBase.convert("RGB")
        group = analyzeSkin(skin)
        if group.version != Version.CURRENT or group.color == Color.NONE:
            continue
        #pass group into output 
        colorIterator[group.color] += 1
        output = skinMixer(skin, getOutput(colorImages, group), colorIterator[group.color]) 
        #save to grouping
        saveOutput(colorImages, output, group)
        #Skins are sorted into groups and then averaged on to their group's collected image
        #mergeSkin(skin, groupId)

    if(GenerateIntermediates):
        saveAll(colorImages)
    
    #Now we've got the skins merged into groups, 
    #We need an interface for making the skin

    #needs 10 values
    settings = [0,0,0,0.5,0,0,0,0,0,0.5]
    generateSkin(settings)

    #customSkinData = [0, 1, 1, 0]
    #Skin image is a png file of the created skin
    #skinImage = (customSkinData)

    #then we make a web interface to tie it all together!

if __name__ == "__main__":
    main()