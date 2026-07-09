---
name: synology-nas
description: Synology NAS connection details -- IP, DSM URL, mount points, SMB config
type: reference
---

- **IP**: 192.168.2.109 | **DSM**: https://192.168.2.109:5001 | **Creds**: `/root/.synology-creds`
- **Mounted**: `/mnt/synology/Backups`, `/mnt/synology/3D`, `/mnt/synology/n8n`, `/mnt/synology/ComfyUI`
- **SMB**: vers=3.0, uid/gid=1001, ~108 MB/s write
- **ComfyUI output**: `/mnt/synology/ComfyUI/output` -> `/app/output` inside container (all generated images save here)
