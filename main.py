import requests
import shutil

def populateIds():
    output = ["4febbfc99fc9fdf4"]
    #get list of all ids ever
    #this is probably a webtrawler?
    #only needs to be run once
    return output

def downloadSkin(skinID):

    #download a single skin
    #www.minecraftskins.com or https://namemc.com
     
    url = 'https://namemc.com/texture/' + skinID + ".png?v=2"
    print(url)
    r = requests.get(url, stream=True)
    if(r.status_code == 200):
        #img.png is probably the file name, can likely be overriden
        with open("img.png", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    return "test"
    

def analyzeSkin(skin):
    #returns the group that it belongs to 
    #By primary color, eye shape

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
    
def skinMixer(skindata):
    #Skin data contains a num (0-1) for each generated image
    #Take that image & scale basied on the sum of transparentcies
    #Should create a completely opake image
    return #a png of a minecraft skin based on the data

def main():
    #Make the "average" skin amonugst skins on skindex
    #this will eventually be a webapp (probably written rails in ruby?)
    
    #here's the deal
    #download a bunch of skins from 
    #www.minecraftskins.com or https://namemc.com
    #this is probably a webtrawler?
    #this returns a bunch of minecraft skins somehow
    
    idList = populateIds()
    for id in idList:
        skin = downloadSkin(id) #This is passed some form of id that lets it download the skin
        print(skin)
        #Analyze the skin
        #where the magic happens
        #groupId = analyzeSkin(skin)
        #Skins are sorted into groups and then averaged on to their group's collected image
        #mergeSkin(skin, groupId)


    #Now we've got the skins merged into groups, 
    #We need an interface for making the skin
    #customSkinData = [0, 1, 1, 0]
    #Skin image is a png file of the created skin
    #skinImage = skinMixer(customSkinData)

    #then we make a web interface to tie it all together!

if __name__ == "__main__":
    main()