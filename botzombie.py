#set NOX VM window at 357,57


import ImageGrab
import sys
import os
import time
import win32api, win32con
import ImageOps
from numpy import *
import glob
save_Path = "C:\Users\Joseph\Desktop\Bot code\ScreenGrabs"
noxCount = 0
bugCount = 0
adCounter = 0
nox = { 0 : (380,68), 
        1 : (380,121),
        2 : (380,178),
        3 : (380,240),
        4 : (380,300),
        5 : (380,354),
        6 : (380,411),
        7 : (380,475),
        8 : (380,520),
        9 : (380,581),
        10 : (380,645),
        11 : (380,695),
        12 : (380,1),
        13 : (380,1),}
        #14 : (380,646) } #coords for nox start buttons

 
def screenGrabAll(tuple_TL, tuple_BR): #x-top, y-top, x-bottom, y-bottom
    im = ImageGrab.grab(bbox = (tuple_TL[0], tuple_TL[1], tuple_BR[0], tuple_BR[1]))
    im.save(save_Path + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im

def press(*args):
    '''
    one press, one release.
    accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
    '''
    VK_CODE = {"ESC" : 0x1B}
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0,0,0)
        time.sleep(.05)
        win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)
    time.sleep(1)

def deleteFiles():
    files = glob.glob("C:\\Users\\Joseph\\Desktop\\Bot code\\ScreenGrabs\\*.png")
    for f in files:
        os.remove(f)


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    #print "Click."          #completely optional. But nice for debugging purposes.

def setMousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))
     
def get_cords():
    time.sleep(5)
    x,y = win32api.GetCursorPos()
    print x,y

def startNoxPlayer():
    global noxCount
    global bugCount
    print("Start nox player ", noxCount)
    time.sleep(1)
    if (noxCount >= 14):
        print("All Done.")
        sys.exit()
    bugCount = 0 #reset bugCount in case we came from a bad game instance
    #noxer = "Nox"+str(nox.keys()[noxCount])
    time.sleep(3)
    os.startfile(r"C:\\Users\\Joseph\\Desktop\\Noxes\\Nox"+str(noxCount)+".lnk")
    # noxCoords = nox[noxCount
    # setMousePos(noxCoords)
    # leftClick()
    noxCount += 1
    time.sleep(40)
    setMousePos((1150,20)) #pin to top
    leftClick()
    setMousePos((1235,30)) #maximize window
    leftClick()
    time.sleep(2)
    startPVZH()

def closeNoxPlayer():
    print("Close nox player")
    global bugCount
    global adCounter
    bugCount = 0
    adCounter = 0
    setMousePos((1240,20)) #unpin from top
    leftClick()
    setMousePos((1345,20)) #press x button
    leftClick()
    time.sleep(1) #wait for confirm window to show up
    setMousePos((623,419)) #confirm
    leftClick()
    startNoxPlayer()

def startPVZH():
    print("start pzvh")
    pvzIcon = screenGrabAll((817,318), (1118,425)) #screen grab area where pvz icon can be
    if ((pvzIcon.getpixel((259,39)) == (255,255,253))):
        setMousePos((1070,360))
        leftClick()
    else:
        setMousePos((860,360))
        leftClick()
    time.sleep(60)
    startAds()

def startAds():
    print("start ads")
    time.sleep(5)
    global bugCount
    adButton = screenGrabAll((800,90), (860,145)) #screen grab around blue watch ad button
    if ((adButton.getpixel((31,41)) == (255,255,255))): #checking that these pixels are white -> means we can watch ads
        setMousePos((828,126))    
        leftClick()
        time.sleep(1)
        watchAd()
    update_Check = screenGrabAll((600,630), (700,650)) #check if the game is updating - takes long time
    if (update_Check.getpixel((78,11)) == (255,255,255)):
        print("Updating.")
        time.sleep(30)
        startAds()
    if bugCount >= 12: #if after 30sec ad button doesn't appear, close nox player
        closeNoxPlayer()
    if ((adButton.getpixel((30,40)) != (255,255,255))): #if ad button pixels are not there, retry and keep retrying until they appear
        bugCount += 1
        startAds()

    #blue = 52,44
    #white text = 30,40
    #screengrab around blue ad button, make sure pixels are there. if yes, click. if no???

def watchAd():
    print("watch ads")
    deleteFiles()
    global noxCount
    global adCounter
    greenBox = screenGrabAll((580,480), (745,545))
    blueDiamond = screenGrabAll((560,43), (591,69))
    if ((greenBox.getpixel((120,35)) != (255,255,255)) and greenBox.getpixel((123,48)) == (96,113,93)): #if grayed out, close nox player, start new one.
        print("grey")
        closeNoxPlayer()
    if (greenBox.getpixel((40,50)) == (111,111,111)):
        press("ESC")
        noxCount -= 1
        adCounter -= 2
        closeNoxPlayer()
    if ((greenBox.getpixel((40,50)) == (0,0,0)) and greenBox.getpixel((1,1)) == (0,0,0)):
        press("ESC")
        noxCount -= 1
        closeNoxPlayer()
    if (greenBox.getpixel((120,35)) == (255,255,255) and blueDiamond.getpixel((21,14)) == (16,114,254)): #if the green button is there and gem is up top, click play
        setMousePos((660,533))
        leftClick() #starts playing ad
        setMousePos((10,10))
        #while(greenBox.getpixel(60,60) != (55,136,13)) #check every 5 seconds that an ad is still playing, if so, press ESC. Else, try to start new ad.
        time.sleep(40)
    blueDiamond = screenGrabAll((560,43), (591,69))
    if ((blueDiamond.getpixel((21,14)) != (16,114,254))): #if blue diamond is not on screen, press ESC
        press("ESC")
    time.sleep(10)
    adCounter += 1
    if adCounter >= 22:
        closeNoxPlayer()
    watchAd()

    #have bug counter. if we get caught in a loop, need to be able to break out and open new nox window. bugCount var with an if statement that starts closeNoxPlayer
    #screengrab around green watch button, match pixels. if yes, click.
    #if ads are grayed out, close current nox window, start new one
    #if neither both green/white and grayed out pixels are seen, wait 5 sec, press ESC again. call watchAd





















def main():
    time.sleep(4)
    startNoxPlayer()
    #watchAd()
    #closeNoxPlayer()    
    #pass
    #im = screenGrabAll((800,90), (860,145))
    #startAds()
    #print(im.getpixel())
 
if __name__ == '__main__':
    main()