import requests
import shutil
from PIL import Image

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
    return pixel

def getColorFromSubsection(img, x, y, height, width):
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
    for key, value in pixelGroups:
        if currentMax < value:
            output = key
            currentMax = value


    return output #returns a group color

def analyzeSkin(skin):
    #returns the group that it belongs to 
    #By primary color, eye shap

    #Figure out the primary color
    
    #first, split everything into parts ie, arms, legs, jacket etc
    #Then determine the average color of that limb
    #Then determine which color is the "most"
    #Must have a low variance to have a main "color"
    #hair & face are seperate & weighted lower
    #torso & jacket are weighted higher
    #Limbs are counted as normal
    #colors have arbitrary ranges for where "red" stops and where "orange" starts for instance

    #Then figure out the eye pattern
    #"steve" or "classic" eyes
    #"vertical eyes" see wilbur soot's skin
    #"anime eyes" what it says on the tin
    #"No eyes" see dream's skin

    #each id contains the data of both of these traits

    return 0 #group ID

def mergeSkin(skin, groupId):
    if skin or groupId:
        skin = groupId
    return
    
def skinMixer(filename, composite, acc):
    img = Image.open(filename).convert("RGBA")
    (width, height) = (img.width, img.height)
    composite = composite.resize((width,height))
    alpha = 1 / acc
    #I don't think this is working properly
    #fill this in later
    #Skin data contains a num (0-1) for each generated image
    #Take that image & scale basied on the sum of transparentcies
    #Should create a completely opaque image
    return Image.blend(composite, img, alpha=alpha)
   
def main():
    #Make the "average" skin amonugst skins on skindex
    #this will eventually be a webapp (probably written rails in ruby?)
    
    #here's the deal
    #download a bunch of skins from 
    #www.minecraftskins.com or https://namemc.com
    #this is probably a webtrawler?
    #this returns a bunch of minecraft skins somehow
    
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
        skin = "minecraft_temp/" + str(id) + ".png"
        output = skinMixer(skin, output, acc) # pass f in in
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