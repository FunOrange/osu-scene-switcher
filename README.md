# obs-osu-gameplay-toggle
This OBS script automatically adjusts desktop and microphone audio sources upon entering osu! gameplay. This makes it so that the song isn't playing too loud on the song select screen when i'm trying to talk. It also makes it so that my key taps aren't too loud when i'm playing the game.

The core concept of changing settings depending on gameplay can be extended to, for example, automatically switch between different scenes, one for gameplay and another for outside of gameplay. I'm thinking of making it so that instead of having a facecam and a handcam both on screen at all times, it switches from facecam to handcam when entering gameplay, and then reverts back outside of gameplay. It would be a better use of screen space, plus it would hide my horrid game face from the viewers while i'm concentrated on the game.

## Setup/Installation
### 1. Get python 3.6.x for OBS
You can download it here: https://sourceforge.net/projects/portable-python/files/Portable%20Python%203.6.5/Portable%20Python%203.6.5%20Basic%20%28x64%29%20R2.exe/download  

Double click the exe and the following folder will be created:  
`Portable Python 3.6.5 x64 R2`  
Navigate to:  
`Portable Python 3.6.5 x64 R2\App\Python`  
and copy the address from the address bar.

Now, in OBS Studio, go to Tools > Scripts > Python Settings and paste the address in the text box.

### 2. Add the script to OBS Studio
Download `obs-osu-noise-suppression-switcher.py`.  
In OBS Studio, go to Tools > Scripts and click the '+' button. Navigate to where `obs-osu-noise-suppression-switcher.py` was downloaded.

### 3. Set Up Stream Companion
Install Stream Companion if you haven't already.  
Open settings. In the 'Output patterns' tab, click 'Add new'. For the new output pattern, enter the following:  

File/Command name: `osu_status`  
Formatting: `!status!`  

Find the location of this new text file. For example, for me this is `C:\Program Files (x86)\StreamCompanion\Files\osu_status.txt`. Copy this address.  

### 4. Set up the script
In OBS Studio, add a Noise Suppression filter (preferably RNNoise) to the audio source of your choice.  
Then, go to Tools > Scripts and click on `obs-osu-noise-suppression-switcher.py`. Paste the address you just copied into `osu! status file location`. Then enter the name of the audio source which you want to toggle Noise Suppression for. For me, the settings look like this:  

osu! status file location: `C:\Program Files (x86)\StreamCompanion\Files\osu_status.txt`  
Target source (eg. Mic/Aux): `Mic/Aux`  

At this point the script should be active, and should always be active every time you open OBS.
