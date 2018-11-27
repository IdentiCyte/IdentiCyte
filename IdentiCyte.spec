# -*- mode: python -*-

block_cipher = None


a = Analysis(['IdentiCyte\\__main__.py'],
             pathex=['.\\IdentiCyte'],
             binaries=[],
             datas=[],
             hiddenimports=['scipy._lib.messagestream', 'sklearn', 'sklearn.neighbors.typedefs', 'pandas', 'pywt._extensions._cwt', 'setuptools._vendor'],
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
          name='IdentiCyte',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=False )
