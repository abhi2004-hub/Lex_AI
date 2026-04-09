# Assets folder

This folder is intended to hold image assets from the `stitch/` design exports (screenshots, illustrations).

I couldn't move binary image files in this environment. To complete the move locally, run the commands below from your project root (`/Users/abhiii/Desktop/major`) in a terminal (zsh):

```bash
mkdir -p assets
mv stitch/lexai_landing_page/screen.png assets/landing-screen.png
mv stitch/lexai_advanced_dashboard/screen.png assets/dashboard-screen.png
mv stitch/lexai_detailed_risk_report/screen.png assets/detailed-risk-screen.png
mv stitch/lexai_interactive_redlining/screen.png assets/interactive-redlining-screen.png
mv stitch/document_version_history_tracked_changes/screen.png assets/version-history-screen.png
mv stitch/mitigation_strategy_dashboard/screen.png assets/mitigation-screen.png
# (optional) move other images
# mv stitch/<folder>/screen.png assets/<name>.png
```

After running the commands above, update any HTML references from `stitch/.../screen.png` to `assets/...`.

If you want, I can update the HTML pages to reference these names (I recommend updating the following pages):

- `index.html` -> `assets/landing-screen.png`
- `dashboard.html` -> `assets/dashboard-screen.png`
- `detailed-risk-report.html` -> `assets/detailed-risk-screen.png`
- `interactive-redlining.html` -> `assets/interactive-redlining-screen.png`
- `version-history.html` -> `assets/version-history-screen.png`
- `mitigation-dashboard.html` -> `assets/mitigation-screen.png`

I can apply those HTML updates now; images will load once you run the mv commands locally.