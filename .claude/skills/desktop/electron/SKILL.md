---
name: electron
description: "Builds cross-platform desktop applications with Electron, React, and IPC communication. Use for native desktop apps with web tech."
category: desktop
tags: [electron, desktop, react, native, cross-platform]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# Electron

> Cross-platform desktop apps with JavaScript, HTML, and CSS.

## Quick Start
```javascript
// main.js
const { app, BrowserWindow, ipcMain } = require('electron');

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: __dirname + '/preload.js',
    },
  });
  win.loadURL('http://localhost:5173'); // or loadFile('dist/index.html')
}

app.whenReady().then(createWindow);

// IPC handler
ipcMain.handle('get-user-data', async () => {
  return { name: 'Alice', role: 'admin' };
});
```

```javascript
// preload.js
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('electronAPI', {
  getUserData: () => ipcRenderer.invoke('get-user-data'),
});
```

## When to Use
- Cross-platform desktop apps (Windows, Mac, Linux)
- Apps built with web frameworks (React, Vue, Svelte)
- Not for lightweight apps (better Tauri)

## Step-by-Step Instructions
1. Init: `npm init; npm install electron --save-dev`
2. Create `main.js` with window creation
3. Create `preload.js` for secure IPC
4. Build and package: `npx electron-builder`

## Dependencies
```bash
npm install electron --save-dev
npm install electron-builder --save-dev
```

## Examples
Input: `npm run start` → Output: Native desktop window with web app

## Resources
- [Electron Docs](https://www.electronjs.org/docs)
- [Examples](./examples/)

## Troubleshooting
- **App bloat from `node_modules`** — the build packed everything.
  Use `electron-builder` `files`/`asar` and exclude dev dependencies.
- **Blank white screen** — renderer crashed. Check DevTools console and
  verify the preload script has `contextIsolation`-safe IPC wiring.
- **App not restarting** — main window destroys on close. Prevent `window-all-closed`
  quit on macOS, or attach the `before-quit` lifecycle hook.
- **Native modules fail to load** — ABI mismatch after a Node upgrade.
  Rebuild with `electron-rebuild` and pin the Electron ABI version.

## Validation
1. App window opens correctly
2. IPC communication works
3. App packages for target OS
