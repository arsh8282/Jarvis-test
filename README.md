# JARVIS (Phase 1: Foundation)

Personal Android assistant in Python + Kivy. Built with Buildozer in GitHub Actions, so a phone is enough.

## Status
Working in source: navigation (10 sections), dark/light theme, accent and text-size settings, text-chat
interface with saved history and copy button, voice screen preview, history list, settings, about.
Placeholder only: Gemini replies (Phase 2), speech (Phase 4), code/file tools (Phase 3), device control (Phase 5), WhatsApp (Phase 6).

Not yet verified on a device: the APK build and the Kivy UI have not been run. Only the logic tests have.

## Build from an Android phone
1. Create a GitHub repository (private is fine) in the mobile browser.
2. Add file > Create new file. Name it `.github/workflows/build-apk.yml`. Paste the contents of `build-apk.yml`. Commit.
3. Add file > Upload files. Upload `jarvis_source.zip` (do not unzip it). Commit.
4. Actions tab > "Build APK" > Run workflow. The first run unpacks the zip into real files, runs the tests, and builds (about 30 to 60 minutes).
5. Open the finished run, download the `jarvis-debug-apk` artifact (a zip), extract it, and install the APK. Allow "install unknown apps" for your browser or file manager if asked.
6. If it fails, download the `build-log` artifact and send me the last 60 lines of `build.log`.

## Run tests (no Android needed)
`PYTHONPATH=. python -m unittest discover -s tests -v`

## Layout
`main.py` entry | `ui/` screens | `assistant/` engine and persona | `storage/` settings and history |
`tools/`, `android_bridge/`, `security/` reserved for later phases | `buildozer.spec` | `ci/build-apk.yml`

## Pinned versions (unverified in this session)
Kivy 2.3.0, python-for-android v2024.01.21, Buildozer 1.5.0, Cython 0.29.36, NDK 25b, Android API 33, Java 17, arm64-v8a only.
