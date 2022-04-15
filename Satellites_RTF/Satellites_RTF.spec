# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Satellites_RTF.py'],
             pathex=['C:\\Users\\Олег\\source\\repos\\Satellites_RTF\\Satellites_RTF'],
             binaries=[],
             datas=[],
             hiddenimports=['matplotlib'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Satellites_RTF',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
