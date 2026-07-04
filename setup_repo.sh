#!/bin/sh
set -e
git lfs install || true
git lfs track "*.tif" "*.tiff" "*.jp2" "*.gpkg" "*.zip" "*.jpg" "*.png"
git add .gitattributes .gitignore README.md
git add .
git commit -m "Forli Digital Twin Master v3.1 completion kit"
git branch -M main
git remote add origin https://github.com/dal1312/-URLE.git || true
git push -u origin main
