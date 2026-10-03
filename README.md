# Visualize — Android APK (online build)

This is a Python + Kivy Android app. The included GitHub Actions workflow builds a debug APK in the cloud.

## Build without installing Android tools on your computer

1. Sign in to GitHub and create a new repository (private is fine).
2. Upload **all contents** of this folder, including the hidden `.github` folder.
3. Open the repository's **Actions** tab.
4. Select **Build Android APK** and click **Run workflow**. A push to `main` also triggers a build.
5. Open the completed workflow run and download the `visualize-debug-apk` artifact.
6. Extract the downloaded artifact, transfer the `.apk` to your Android phone, and tap it to install.
7. If Android asks, allow your browser/file manager to install unknown apps.

## Notes

- This creates a debug APK for testing, not a Play Store release.
- The first Android build can take a while.
- If the build fails, open the workflow run and inspect the failing step's log.
- For Google Play, configure a signed release build and store signing secrets securely in GitHub Actions.
