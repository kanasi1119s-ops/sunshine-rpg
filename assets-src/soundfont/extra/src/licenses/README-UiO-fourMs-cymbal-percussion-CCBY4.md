# Cymbal percussion: motion capture, audio and video (2011)

Recordings of cymbal-playing actions captured at the fourMs Lab, University of Oslo, on 12 April 2011. A percussionist performed a structured set of cymbal strokes: flams, rolls and staccato strokes at several dynamic levels, with and without damping, plus a free improvisation. Each take was recorded simultaneously with two motion capture systems (an optical infrared system controlled by Qualisys Track Manager, and a full-body Xsens MVN inertial suit) together with synchronised audio and video. The data are distributed as six ZIP archives grouped by modality/format.

## Background

The parallel use of an optical (Qualisys) and an inertial (Xsens) motion capture system on the same performances was a methodological interest in comparing or combining the two capture technologies in a complex and time-critical task (cymbal performance).

## Contents

Take names encode a systematic stroke taxonomy (mixed Norwegian/English terms), broader than a simple summary suggests: `flam_upwards`/`flam_downwards`, `rulleslag` (drum/cymbal roll), `staccato` (also spelled `staccatto` in some filenames — both spellings occur in the data), `impro` (improvisation), and a large suspended-cymbal family (`suspeso_attack`/`suspeso_nonattack`, `center`/`midt`/`kant` (rim), `soft`/`strong`), plus `suspeso_tremolo` (incl. `cresc`/`diminuendo` variants), `suspeso_reference`, and a couple of `test` takes. (`suspeso` appears to be a spelling of *sospeso*, "suspended".)

Dynamics are encoded as `soft`/`medium`/`strong` or `p`/`mf`/`f`, with `_damped` variants for muted strokes.

| File | Size | Format | Contents |
|------|------|--------|----------|
| `QTM.zip` | 149.1 MB | ZIP of `.qtm` | 72 raw Qualisys Track Manager capture files, one per take, named by stroke type (e.g. `staccato_f0001.qtm`, `flam_downwards_b_medium0001.qtm`). |
| `XsensMvn.zip` | 420.1 MB | ZIP of `.mvn` / `.mvnx` | Native Xsens MVN inertial motion-capture recordings, `Cymbal 1-001.mvn` … `Cymbal 1-071.mvn` (71 takes), plus one `Cymbal 1-006.mvnx` (XML export) and a bundled `Cymbal_recording_naming.txt` session-naming key. |
| `MP4.zip` | 123.6 MB | ZIP of `.mp4` | 72 video clips (camera "video2"), H.264 720×480, 30 fps, AAC stereo 44.1 kHz. Durations range ≈1.8–21.6 s (median ≈7.6 s). File names match the take names. |
| `WAV.zip` | 38 MB | ZIP of `.wav` | 72 audio files (from "video2"), PCM 16-bit, 44.1 kHz, mono. Durations range ≈1.8–21.6 s (median ≈7.6 s). Also contains `__MACOSX` resource-fork entries (macOS zip artefacts). |
| `XsensC3D.zip` | 14.5 MB | ZIP of `.c3d` | 71 C3D exports of the Xsens data, `Cymbal 1-001.c3d` … `Cymbal 1-071.c3d`, plus the same bundled `Cymbal_recording_naming.txt` naming key. |
| `QAM.zip` | 23.9 kB | ZIP of `.qam` | 3 Qualisys AIM (Automatic Identification of Markers) model files: `bjoern.qam`, `bjoern_aim2.qam`, `bjoern_aim_mallet.qam` — the marker-labelling models used to auto-identify markers in QTM. |

QTM, WAV and MP4 each hold 72 takes with identical basenames, so the raw optical capture, video and audio of the same performance can be matched exactly by filename. 

The Xsens archives (`XsensMvn.zip`, `XsensC3D.zip`) hold 71 takes each, using a separate `Cymbal 1-NNN` numbering; the bundled `Cymbal_recording_naming.txt` maps each session number to a stroke name (e.g. sessions 05–10 = staccato soft→strong, 11–16 = flam upwards, 17–21 = roll, 22 = impro, 42–71 = suspeso variants, 1–4 = tests), and marks session 26 as `feil` (Norwegian for "error"/bad take), which is why the Xsens archives have one fewer take than QTM/WAV/MP4.

## Data formats

- **QTM (`.qtm`)** — native binary project/capture files of Qualisys Track Manager (QTM), the software controlling the fourMs optical infrared marker system. They contain the raw 3D marker trajectories and session settings and are opened in QTM; from there they can be re-exported to TSV, C3D, MAT, etc.
- **QAM (`.qam`)** — Qualisys AIM model files. AIM ("Automatic Identification of Markers") models store a labelled marker skeleton that QTM uses to automatically identify and name markers across takes.
- **MVN / MVNX (`.mvn`, `.mvnx`)** — Xsens MVN inertial motion-capture files. `.mvn` is the native binary session format opened in Xsens MVN Studio; `.mvnx` is an open XML export of segment/joint kinematics that can be parsed without the Xsens software.
- **C3D (`.c3d`)** — the standard biomechanics binary format for 3D marker/analog data (here, exports of the Xsens data). Readable by most motion-analysis tools and by open libraries (e.g. `ezc3d`, Python `c3d`, MATLAB toolboxes).
- **MP4 (`.mp4`)** — H.264 video with AAC audio; plays in any standard media player.
- **WAV (`.wav`)** — uncompressed PCM audio.

## Recording setup

- **Location / date:** fourMs Lab, Department of Musicology, University of Oslo — 12 April 2011.
- **Optical motion capture:** Qualisys system controlled from Qualisys Track Manager (QTM), with AIM marker models (`.qam`).
- **Inertial motion capture:** Xsens MVN full-body suit (native `.mvn`, with C3D and MVNX exports).
- **Audio/video:** a camera track labelled "video2" providing 720×480 / 30 fps H.264 video and 44.1 kHz audio.

## Provenance

Collected at the fourMs Lab, University of Oslo. Migrated from the fourMs Lab website in 2026. Original page path: `research/Datasets/20110412-cymbals/index.html`.

## License and citation

**License:** CC BY 4.0

**Cite as** (fill in the Zenodo DOI once minted):

> Jensenius, A. R., Godøy, R. I., Voldsund, A., & Løken, B. A. (2011). *Cymbal percussion: multimodal motion capture, audio and video (fourMs Lab, 12 April 2011)* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX

## Creators note

Creators confirmed by the depositor (2026-07-14): Alexander Refsum Jensenius, Rolf Inge Godøy, and Arve Voldsund (University of Oslo). Performer: Bjørn Arne Løken (credited as creator; the `bjoern*` Qualisys AIM files refer to him).
