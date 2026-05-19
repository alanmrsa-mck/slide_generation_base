"""
Export every slide in a PPTX as a PNG using PowerPoint COM automation.
Usage: py render_slides.py <path_to_pptx> [output_dir]
"""
import sys, pathlib, os
import win32com.client

pptx_path  = pathlib.Path(sys.argv[1]).resolve()
out_dir    = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else pptx_path.parent / "slides_png"
out_dir.mkdir(exist_ok=True)

print(f"Opening: {pptx_path}")
print(f"Output:  {out_dir}")

ppt = win32com.client.Dispatch("PowerPoint.Application")
ppt.Visible = True   # must be visible on Windows for export to work reliably

try:
    prs = ppt.Presentations.Open(str(pptx_path), ReadOnly=True, Untitled=False, WithWindow=False)
    for i in range(1, prs.Slides.Count + 1):
        out_path = str(out_dir / f"slide_{i:02d}.png")
        prs.Slides(i).Export(out_path, "PNG", 1920, 1080)
        print(f"  Exported slide {i} -> {out_path}")
    prs.Close()
finally:
    ppt.Quit()

print("Done.")
