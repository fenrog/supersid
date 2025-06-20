# SuperSID on Windows 10

## 1) Install Python

There are 2 options for setting up your python environment for SuperSID. You can either create a virtual environment to run the program (option 1.1), or you can install directly into the system environment (option 1.2).

The preferred solution is 1.1 (virtual environment) for two reasons:

a) It allows you to have virtual environments with different Python setups and
b) the audio modules *sounddevice* and *pyaudio* seem to behave better. They will offer less configuration options for audio cards but there is a higher chance to actually work as expected.

The table below is a comparison between the behaviour of installations 1.1) and 1.2) for the use of a USB sound card which can sample at 48000 Hz and 96000 Hz (and Windows is configured to 96000 Hz).<br/>
sampler.py: y = working, n = not working<br/>
supersid.py: y = working, not found = warning, numbers or crash = error<br/>
measures x kHz: y = working, cutoff = working but frequency is cut off, falling back to working default = working, nonsense signal = appears to work but the signal is nonsense, -- = not working

| <br/>module | <br/>host-API       | <br/>sampling rate | 1.1)<br/>sampler.py | <br/>supersid.py | <br/>measures f>20 kHz, f>40 kHz, f>80 kHz | 1.2)<br/>sampler.py | <br/>supersid.py | <br/>measures f>20 kHz, f>40 kHz, f>80 kHz |
|:------------|:--------------------|-------------------:|:-------------------:|:----------------:|:-------------------------------------------|:-------------------:|:----------------:|:-------------------------------------------|
| sounddevice | MME                 |              48000 |                   y |                y |                                          y |                   y |                y |                                          y |
| sounddevice | MME                 |              96000 |                   y |                y |                                          y |                   y |                y |                                          y | 
| sounddevice | MME                 |             192000 |                   y |                y |                         y cutoff at 48 kHz |                   y |                y |                         y cutoff at 48 kHz |
| sounddevice | Windows DirectSound |              48000 |                   y |                y |                                          y |                   n |        not found |          y falling back to working default |
| sounddevice | Windows DirectSound |              96000 |                   y |                y |                                          y |                   n |        not found |          y falling back to working default |
| sounddevice | Windows DirectSound |             192000 |                   y |                y |                         y cutoff at 48 kHz |                   n |        not found |                         y cutoff at 48 kHz |
| sounddevice | Windows WASAP       |              48000 |                   n |            -9997 |                                          n |                   n |        not found |          y falling back to working default |
| sounddevice | Windows WASAP       |              96000 |                   y |            -9999 |                                          n |                   n |        not found |          y falling back to working default |
| sounddevice | Windows WASAP       |             192000 |                   n |            -9997 |                                          n |                   n |        not found |                         y cutoff at 48 kHz |
| sounddevice | Windows WDM-KS      |              48000 |                   y |                y |                                          y |                   y |                y |                                          y |
| sounddevice | Windows WDM-KS      |              96000 |                   y |                y |                                          y |                   y |                y |                                          y |
| sounddevice | Windows WDM-KS      |             192000 |                   n |            -9996 |                                         -- |                   n |            -9996 |                                          n |

| <br/>module | <br/>host-API       | <br/>sampling rate | 1.1)<br/>sampler.py | <br/>supersid.py | <br/>measures f>20 kHz, f>40 kHz, f>80 kHz | 1.2)<br/>sampler.py | <br/>supersid.py | <br/>measures f>20 kHz, f>40 kHz, f>80 kHz |
|:------------|:--------------------|-------------------:|:-------------------:|:----------------:|:-------------------------------------------|:-------------------:|:----------------:|:-------------------------------------------|
| pyaudio     | MME                 |              48000 |                   y |                y |                                          y |                   y |                y |                                          y |
| pyaudio     | MME                 |              96000 |                   y |                y |                                          y |                   y |                y |                                          y |
| pyaudio     | MME                 |             192000 |                   y |                y |                         y cutoff at 48 kHz |                   y |                y |                         y cutoff at 48 kHz |
| pyaudio     | Windows DirectSound |              48000 |                   n |                y |                          n nonsense signal |                   n |        not found |          y falling back to working default |
| pyaudio     | Windows DirectSound |              96000 |                   n |                y |                          n nonsense signal |                   n |        not found |          y falling back to working default |
| pyaudio     | Windows DirectSound |             192000 |                   n |                y |                          n nonsense signal |                   n |        not found |                         y cutoff at 48 kHz |
| pyaudio     | Windows WASAP       |              48000 |                   n |            crash |                                          n |                   n |        not found |          y falling back to working default |
| pyaudio     | Windows WASAP       |              96000 |                   y |                y |                          n nonsense signal |                   n |        not found |          y falling back to working default |
| pyaudio     | Windows WASAP       |             192000 |                   n |            crash |                                          n |                   n |        not found |                         y cutoff at 48 kHz |
| pyaudio     | Windows WDM-KS      |              48000 |                   n |            crash |                                          n |                   n |            crash |                                          n |
| pyaudio     | Windows WDM-KS      |              96000 |                   n |            crash |                                          n |                   n |            crash |                                          n |
| pyaudio     | Windows WDM-KS      |             192000 |                   n |            crash |                                          n |                   n |            crash |                                          n |

### 1.1) Install Anaconda3 2021.05 including Python 3.8.12 (64 bit), create a supersid environment and install the Python modules
- Download [Anaconda 2021.05](https://repo.anaconda.com/archive/Anaconda3-2021.05-Windows-x86_64.exe)
- Install *Anaconda3-2021.05-Windows-x86_64.exe*
    - Welcome to Anaconda3 2021.05 --> Next
    - License Agreement --> I agreee
    - (x) All users (requires admin privileges) --> Next
    - Choose Install Location: keep 'C:\ProgramData\Anaconda3' --> Next
    - Advanced Installation Options: select none --> Install
    - Installation Complete --> Next
    - advertisement for PyCharm Pro --> Next
    - Completing Anaconda3 2021.05: deselect both --> Finish

Open an `Anaconda Command Promt (Anaconda3)`
```console
    > conda update -n base -c defaults conda
    > conda create --name supersid python=3.8
    > conda activate supersid
    > conda install numpy
    > conda install pandas
    > conda install matplotlib
    > conda install PyAudio
    > pip install PyPubSub
    > pip install sounddevice
    > pip install ephem
```

### 1.2) Install Python 3.13.5 (64 bit)
- Download [Python 3.13.5 (64-bit)](https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe)
- Install *python-3.13.5-amd64.exe*
    - Select both [x] Use admin privileges ... and [x] Add python.exe to path, Customize installation, Next
    - Select all, including [x] py launcher [x] for all users, Next
	- Advaned options: additionally select [x] Install Python 3.13 for all users
    - Double check the install location changed to *C:\\Program Files\\Python313*
    - Install
    - Disable path length limit
    - Close

Open a `CMD` window.
```console
    > "C:\Program Files\Python313\python.exe" -m pip install --upgrade pip
```

If you choose the option 1.2 (system level install), then you'll have to replace any occurence of `python` below with `"C:\Program Files\Python313\python.exe"`.


## 2) Install SuperSID
- You can simply go to [SuperSID](https://github.com/sberl/supersid). Press the green 'Code' button and click 'Download ZIP', **or** download [supersid-master.zip](https://github.com/sberl/supersid/archive/refs/heads/master.zip) directly.
- Then extract the zip to the folder where you want to install SuperSID.

**or**

- You can first install [Git for Windows](https://gitforwindows.org/).
- Then open a GIT console in the folder you want to install SuperSID.

```console
    $ git clone https://github.com/sberl/supersid.git
```

To update (pull) to the latest version, do:
```console
    $ cd <path to your supersid installation>
    $ git pull
```

### Install the Python 3.13.5 Python modules
If you choose the option 1.2 (system level install), then you'll have to continue the Python modules installation.
```console
    > "C:\Program Files\Python313\python.exe" -m pip install -r requirements.txt
```

## 3) Choose your Sound Card

Identify the available audio library / host API / audio device / sample rate combinations. If you have grep available, you can filter the results.

The [Thesycon USB Descriptor Dumper](https://www.thesycon.de/eng/usb_descriptordumper.shtml) may give you some insights about the device capabilities. I.e. supported sample rate and bits per sample.

If your proprietary sound card software has configuration options to select microphone input or line input, select the line input.<br/>
If your proprietary sound card software has configuration options, deselect all sound effects, set 16 bit and the desired sample rate (48000, 96000 or 192000).<br/>
If your sound card does not come with a proprietary configuration software, you may want to follow the guide [How do I Change the Sample Rate and Bit Depth on a USB Microphone?](https://www.audio-technica.com/en-us/support/audio-solutions-question-of-the-week-how-do-i-change-the-sample-rate-and-bit-depth-on-a-usb-microphone/).

- use `python sampler.py` in order to get a complete list including the errors
- use `python sampler.py | grep -v "peak freq \[0\] Hz" | grep "duration 1\.[012]"` in order to get a compact list of the acceptable candidates. This command will take a while before it outputs anything.
- use `python sampler.py | grep -v "peak freq \[0\] Hz" | grep "duration 1\.[012]" -B2 -A2` in order to get a verbose list of the acceptable one channel candidates. This command will take a while before it outputs anything.
- use `python sampler.py -n2 | grep -v "peak freq \[0, 0\] Hz" | grep "duration 1\.[012]" -B2 -A2` in order to get a verbose list of the acceptable two channel candidates. This command will take a while before it outputs anything.

```console
    > cd <path to your supersid installation>\src\
    > python sampler.py | grep -v "peak freq \[0\] Hz" | grep "duration 1\.[012]" -B2 -A2
```

Find the right card line you want to use based on the card name and the frequency you want to sample.
Make sure that the time is approximately one second, not fractions of a second and not multiples of a second.

The experience with a small set of sound cards leads to following rules of thumb:

- **sounddevice** behaves more gracefully than **pyaudio**
- **MME: <YourSoundCard>** is typically a good choice

Caution: The **MME** host API allows to configure higher sampling rates than the configuration of the HW or the HW allows.
It will simply upsample the data in the driver but there is a hard cutoff at the limit of the sound card configuration or at the limit of the ADC.
This cutoff will be visible in the graphical viewer of supersid.py (tk).

Selected:
```example
    sounddevice device 'MME: Microsoft Sound Mapper - Input', sampling rate 192000, format S32_LE
    sounddevice 'MME: Microsoft Sound Mapper - Input' at 192000 Hz
    192000 <class 'numpy.int32'> read from sounddevice 'MME: Microsoft Sound Mapper - Input', shape (192000,), format S32_LE, duration 1.09 sec, peak freq [9984] Hz
    [     0      0 -65536      0      0      0      0 -65536      0      0]
    Vector sum -517996544
```

The important parts are in this line<br/>
**192000** <class 'numpy.int32'> read from sounddevice '**MME: Microsoft Sound Mapper - Input**', shape (192000,), format **S32_LE**, duration 1.09 sec, peak freq [9984] Hz

The corresponding lines of the configuration file 'supersid.cfg':
```example
    [PARAMETERS]
    audio_sampling_rate = 192000

    [Capture]
    Audio = sounddevice
    Device = MME: Microsoft Sound Mapper - Input
    Format = S32_LE
```


## 4) Adapt the your supersid\Config\supersid.cfg file

See [ConfigHelp.md](./ConfigHelp.md)


## 5) Start the SuperSID program

```console
    > cd <path to your supersid installation>\src
    > python supersid.py -c ..\Config\supersid.cfg
```
