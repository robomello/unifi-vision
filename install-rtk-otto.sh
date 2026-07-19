#!/usr/bin/env bash
# Pinned, checksum-verified RTK install for the Claude Code running ON the OTTO box.
# No `curl | sh`. Reviewable. Reversible (rtk init --uninstall).
# Default = ADVISORY mode (no forced command rewrite). Flip MODE=rewrite only after MBUSI approval.
set -euo pipefail

RTK_VERSION="v0.42.4"
TARGET="x86_64-unknown-linux-musl"                  # Linux x86_64; change if OTTO differs (uname -m)
SHA256="34975116da11e09e502501daf758143e0b22ed3a42a10eb67fb693a6270d9e36"  # verified for v0.42.4 musl tarball
MODE="${MODE:-advisory}"                            # advisory | rewrite
BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"

echo ">> RTK ${RTK_VERSION} (${TARGET}), mode=${MODE}"

# 1. download pinned release + verify checksum (abort if mismatch)
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
url="https://github.com/rtk-ai/rtk/releases/download/${RTK_VERSION}/rtk-${TARGET}.tar.gz"
echo ">> downloading $url"
curl -fsSL -o "$tmp/rtk.tgz" "$url"
echo "${SHA256}  $tmp/rtk.tgz" | sha256sum -c -      # <-- hard gate; stops here on mismatch

# 2. place binary on PATH
mkdir -p "$BIN_DIR"
tar xzf "$tmp/rtk.tgz" -C "$BIN_DIR" rtk
chmod +x "$BIN_DIR/rtk"
"$BIN_DIR/rtk" --version
case ":$PATH:" in *":$BIN_DIR:"*) ;; *) echo "!! add $BIN_DIR to PATH (e.g. in ~/.bashrc)";; esac

# 3. wire into Claude Code
if [ "$MODE" = "advisory" ]; then
  # Adds RTK awareness so Claude Code *chooses* `rtk grep`/`rtk git diff`; NO PreToolUse rewrite.
  # Nothing is auto-suppressed; fully under your control; lower savings, near-zero risk.
  "$BIN_DIR/rtk" init --no-patch
  echo ">> ADVISORY installed. In Claude Code, instruct it to prefer 'rtk grep' / 'rtk git diff'"
  echo "   and avoid the suppressing filters (rtk log / rtk test) on anything it acts on."
else
  # Full auto-rewrite hook. PREVIEW first, then apply. Bigger savings, but suppressing filters
  # (log / match_output short-circuits) can hide a real failure from Claude Code.
  echo ">> DRY-RUN preview of settings.json + CLAUDE.md changes:"
  "$BIN_DIR/rtk" init -g --dry-run -vv
  read -r -p ">> apply these changes? [y/N] " ok
  [ "$ok" = "y" ] && "$BIN_DIR/rtk" init -g || echo ">> skipped patching."
fi

echo ">> done. Verify savings later with: rtk gain   |   Roll back with: rtk init --uninstall"
echo ">> footprint: binary at $BIN_DIR/rtk, local analytics at ~/.local/share/rtk/history.db"
