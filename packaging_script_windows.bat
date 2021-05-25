RMDIR "dist" /S /Q
RMDIR "build" /S /Q
pyinstaller --onefile --noconsole --icon Icon\CellService_icon.ico --hidden-import PyQt5.sip --hidden-import PyQt5.QtWidgets --hidden-import CellService_processing --hidden-import skimage.filters.rank.core_cy_3d --hidden-import CellService_analisys --add-data "Icon;Icon" CellService.py
