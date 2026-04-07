# Fix: Dashboard Charts Not Loading

## Problem

❌ Error: `Failed to load data dashboard-charts.js:600:13`

This happens because **file://** protocol has security restrictions that prevent loading local files via JavaScript.

---

## Solution: Start Local Web Server

You have **2 methods**:

### **Method 1: Quick Batch File (Windows)**

Simply **double-click** `start-server.bat` in your project folder.

Then visit: `http://localhost:8000/dashboard.html`

---

### **Method 2: PowerShell Command**

Open PowerShell in your project folder:

```powershell
python -m http.server 8000
```

Then open browser to: `http://localhost:8000/dashboard.html`

---

### **Method 3: Manual Steps**

1. Open **PowerShell**
2. Navigate to project:
   ```powershell
   cd "v:\My Projects\Simulated-Work IV"
   ```

3. Start server:
   ```powershell
   python -m http.server 8000
   ```

4. Open browser:
   ```
   http://localhost:8000/dashboard.html
   ```

5. To stop: Press **Ctrl+C** in PowerShell

---

## Why This Happens

| Method | Works? | Why? |
|--------|--------|------|
| `file:///path/to/dashboard.html` | ❌ | Browser blocks local file access for security |
| `http://localhost:8000/dashboard.html` | ✅ | Server simulates real website, allows file access |

---

## Verify Data Files Exist

Before starting server, check if your data files exist:

```powershell
# Check files
ls data/processed/

# Should show:
# - daily_bed_occupancy.csv
# - analysis_summary.json
```

If missing, run:
```powershell
python run_complete_analysis.py
python generate_visualizations.py
```

---

## Troubleshooting

### "Port 8000 already in use"
```powershell
python -m http.server 8001    # Use different port
# Then visit: http://localhost:8001/dashboard.html
```

### "Python not found"
Make sure Python is installed and in PATH:
```powershell
python --version
```

### Files still not loading
1. Check browser console: **F12** → **Console** tab
2. Look for specific file path errors
3. Verify files exist in correct locations
4. Clear browser cache: **Ctrl+Shift+Del**

---

## After Server Starts

You'll see:
```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

**Open browser to:** `http://localhost:8000/dashboard.html`

✅ Charts should load now!

---

## Server Running Tips

- **Keep terminal open** while using dashboard
- **Don't close** the PowerShell window
- **Press Ctrl+C** when done to stop server
- Server runs on your machine only (not accessible to others)

---

## Permanent Solution: Use Streamlit

For a better experience without server setup:

```powershell
streamlit run app.py
```

This starts automatically and opens in browser! 🎉

---

**Questions?** Let me know if you hit any issues!
