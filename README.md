# SoundFix
Restore or regenerate damaged, clipped, or overly-compressed audio assets (sound effects, music, and speech).
in lieu of a damaged file, e.g. a file

## Oops
I was wrong about a bunch of stuff, i thought the audio file was overly degraded and compressed. Now, I suspect that the opriginal example file was volume maximized. It clips, but not egregiously. The primary issue is that it is just too loud in comaprison to other in game sound files.

## Purpose
- assess the properties of an audio file and determine if and how it should be modified to better meet the needs of the user.

- if amplitude (volume) is the primary concern then systematically generate reduced / increased amplitude audio files for use in game 

- Fix clipped audio, excessive compression artifacts, low-bandwidth recordings, and missing-data segments.

- Improve asset quality for games, archives, and generative audio pipelines.

- implement a one to many audio file converter such that a single audio file can be converted to multiple files of different volumes / amplitudes

## Design
WoW's files are ogg Vorbis, well be keeping that.

## Example
- Example/source: https://www.wowhead.com/sound=8960/readycheck  
The infamous "Your dungeon is ready and now you are deaf.


## Words are Words
Audio (data) or (physical) Sound ?  
A microphone converts sound into audio, and a speaker converts audio into sound.

## Levels - dB or LUFS
LUFS (Loudness Units relative to Full Scale)  
Where Full Scale is the maximum signal level (0 dBFS) a digital system can handle before it runs out of data to describe the sound.

- cute labels or just LUFS or dB level changes ?  
  hmmm, myabe levels is too technical of an interface, also each file is a little different

- what if the sound is quiet and needs to be louder ?
- most wow sound files have been volume maximized
- assume original is as loud as needed and just reduce amplitude for now

### Volume Slider Positions
- original: no change
- max: ensure both channels are ~ 0 AND ≤ 0 dB, 100 %  
  original might be slightly above OR below this, i.e. this could make it a little quieter or a little louder. difference should be negligible.


## Volume Gradation Reference (21 Steps)

| Unit | Min  | 2     | 3     | 4     | 5     | 6     | 7     | 8     | 9     | 10    | 11    | 12    | 13    | 14    | 15    | 16    | 17    | 18    | 19    | 20    | Max   |
|:-----|-----:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
|  dB  |  -60 |   -57 |   -54 |   -51 |   -48 |   -45 |   -42 |   -39 |   -36 |   -33 |   -30 |   -27 |   -24 |   -21 |   -18 |   -15 |   -12 |    -9 |    -6 |    -3 |     0 |       |
| LUFS |-72.39| -69.39| -66.39| -63.39| -60.39| -57.39| -54.39| -51.39| -48.39| -45.39| -42.39| -39.39| -36.39| -33.39| -30.39| -27.39| -24.39| -21.39| -18.39| -15.39| -12.39|       |

with all of my adjustors turned up to max this minimum was still audible, could actually hear down to -66 or so but trying to keep things reasonable for every people use

## Methods and Approaches

- **AudioSR (Audio Super-Resolution):** diffusion-based upsampling to restore high-frequency content.
- **DreamAudio:** customized text-to-audio generation for recreating missing or damaged sounds.
- **Constrained Matching Pursuit:** sparse reconstruction technique for targeted artifact removal.
- goldwave
- izotope

## Resources

- Project / demo: https://audioldm.github.io/audiosr/

https://neuralanalog.com/

### Selected references

- Jin, Y., Ye, Z., Tian, Z., Liu, H., Kong, Q., Guo, Y., & Xue, W. (2026). Inference-time scaling for diffusion-based audio super-resolution. Proceedings of the AAAI Conference on Artificial Intelligence, 40(17), 14982–14990.

- Liu, H., Chen, K., Tian, Q., Wang, W., & Plumbley, M. D. (2024). AudioSR: Versatile audio super-resolution at scale. ICASSP 2024. https://doi.org/10.1109/icassp48485.2024.10447246

- Yuan, Y., et al. (2026). DreamAudio: Customized text-to-audio generation with diffusion models. IEEE Transactions on Audio, Speech, and Language Processing, 34.

Cited by: 2


https://audioldm.github.io/audiosr/  
Abstract  
Audio super-resolution is a fundamental task that predicts high-frequency components for low-resolution audio, enhancing audio quality in digital applications. Previous methods have limitations such as the limited scope of audio types (e.g., music, speech) and specific bandwidth settings they can handle (e.g., 4 kHz to 8 kHz). We introduce a diffusion-based generative model, AudioSR, that is capable of performing robust audio super-resolution on versatile audio types, including sound effects, music, and speech. Specifically, AudioSR can upsample any input audio signal within the bandwidth range of 2 kHz to 16 kHz to a high-resolution audio signal at 24 kHz bandwidth with a sampling rate of 48 kHz. Extensive objective evaluation on various audio super-resolution benchmarks demonstrates the strong result achieved by the proposed model. In addition, our subjective evaluation shows that AudioSR can acts as a plug-and-play module to enhance the generation quality of a wide range of audio generative models, including AudioLDM, Fastspeech2, and MusicGen. 
