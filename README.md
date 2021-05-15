# osu_scene_switcher.py
Switches scenes upon entering osu! gameplay. I don't want people to see my drooling face while I'm concentrating on the game.

## Setup/Installation
### 1. Get python 3.6.x for OBS
You can download it here: https://sourceforge.net/projects/portable-python/files/Portable%20Python%203.6.5/Portable%20Python%203.6.5%20Basic%20%28x64%29%20R2.exe/download  

Double click the exe and the following folder will be created:  
`Portable Python 3.6.5 x64 R2`  
Navigate to:  
`Portable Python 3.6.5 x64 R2\App\Python`  
and copy the address from the address bar.

Now, in OBS Studio, go to Tools > Scripts > Python Settings and paste the address in the text box. For example, mine looks like this:  
**Python Install Path (64bit)**  
`C:/Users/funor/Downloads/Portable Python 3.6.5 x64 R2/App/Python`

### 2. Add the script to OBS Studio
Download `osu_scene_switcher.py`.  
In OBS Studio, go to Tools > Scripts and click the '+' button. Navigate to where `osu_scene_switcher.py` was downloaded.

### 3. Set Up Stream Companion
Install Stream Companion if you haven't already.  
Open settings. In the 'Output patterns' tab, click 'Add new'. For the new output pattern, enter the following:  

File/Command name: `osu_status`  
Formatting: `!status!`  

Find the location of this new text file. For example, for me this is `C:\Program Files (x86)\StreamCompanion\Files\osu_status.txt`. Copy this address.  

### 4. Configure the script
Go to Tools > Scripts and select `osu_scene_switcher.py`. Paste the address you just copied into `osu! status file location`. Then enter the names of the two scenes you want to switch between. For me, the settings look like this:  

osu! status file location: `C:\Program Files (x86)\StreamCompanion\Files\osu_status.txt`  
Scene to switch to when entering gameplay: `osu! twitch (handcam)`  
Scene to switch to when exiting gameplay: `osu! twitch (facecam)`  

At this point the script should be active, and should always be active every time you open OBS.
