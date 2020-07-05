import win32api, win32con, win32gui, os, requests, json, shutil
#----------------------------------------------------------------------

desktopDescription = True
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
desktopDescriptionFile = os.path.join(desktop, 'description.txt')

def setWallpaper(path):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 10, win32con.REG_SZ, "10")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, 1+2)


def getAPOD(payload, path):
    r = requests.get('https://api.nasa.gov/planetary/apod', params=payload)
    print(r.status_code)
    rc = r.json()
    r = requests.get(rc['hdurl'])
    if r.status_code == 200:
        with open(path, 'wb') as f:
            f.write(r.content)
    setWallpaper(path)
    if desktopDescription:
        with open(desktopDescriptionFile, 'w') as f:
            f.write(rc['title'])
        with open(desktopDescriptionFile, 'a') as f:
            f.write('\n\n')
            f.write(rc['explanation'])

    

if __name__ == "__main__":
    payload = {
        'hd': True,
        'api_key': 'YOUR API KEY'
    }
    path = os.path.abspath('apod.jpg')
    getAPOD(payload, path)
    print(path)
    