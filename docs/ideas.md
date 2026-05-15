# Ideas

Future ideas, references, and exploratory notes that are outside the current batch loudness conversion MVP.

## Current Understanding
The original example file may not be overly degraded or compressed. It appears to be volume maximized. It may clip, but not egregiously. The primary issue is that it is too loud in comparison to other in-game sound files.

## Volume Gradation (21 Steps)

| Unit | Min  | 2     | 3     | 4     | 5     | 6     | 7     | 8     | 9     | 10    | 11    | 12    | 13    | 14    | 15    | 16    | 17    | 18    | 19    | 20    | Max   |
|:-----|-----:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
|  dB  |  -60 |   -57 |   -54 |   -51 |   -48 |   -45 |   -42 |   -39 |   -36 |   -33 |   -30 |   -27 |   -24 |   -21 |   -18 |   -15 |   -12 |    -9 |    -6 |    -3 |     0 |       |
| LUFS |-72.39| -69.39| -66.39| -63.39| -60.39| -57.39| -54.39| -51.39| -48.39| -45.39| -42.39| -39.39| -36.39| -33.39| -30.39| -27.39| -24.39| -21.39| -18.39| -15.39| -12.39|       |

With all adjustors turned up to max, the minimum was still audible. It was possible to hear down to about -66 dB, but the current tool should keep things reasonable for general use.

## Methods and Approaches

Future restoration and regeneration ideas:

- **AudioSR (Audio Super-Resolution):** diffusion-based upsampling to restore high-frequency content.
- **DreamAudio:** customized text-to-audio generation for recreating missing or damaged sounds.
- **Constrained Matching Pursuit:** sparse reconstruction technique for targeted artifact removal.
- GoldWave
- iZotope

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
