#!/usr/bin/env bash
set -u

echo "=== JARVIS AMD/ROCm CHECK ==="
echo

echo "[Sistema]"
uname -a
echo
if command -v lsb_release >/dev/null 2>&1; then
  lsb_release -a 2>/dev/null || true
fi

echo
echo "[Kernel]"
uname -r

echo
echo "[GPU]"
if command -v lspci >/dev/null 2>&1; then
  lspci | grep -Ei 'VGA|3D|Display|AMD/ATI' || echo "GPU AMD não encontrada via lspci."
else
  echo "lspci não instalado."
fi

echo
echo "[AMDGPU]"
if command -v modinfo >/dev/null 2>&1 && modinfo amdgpu >/dev/null 2>&1; then
  modinfo amdgpu | grep -E '^(version|filename):' || true
else
  echo "Módulo amdgpu não disponível."
fi

echo
echo "[ROCm]"
if command -v rocminfo >/dev/null 2>&1; then
  rocminfo 2>/dev/null | grep -E 'Name:|gfx[0-9]+' | head -30 || true
else
  echo "rocminfo não encontrado."
fi

if command -v rocm-smi >/dev/null 2>&1; then
  echo
  echo "[ROCm SMI]"
  rocm-smi 2>/dev/null || true
elif command -v amd-smi >/dev/null 2>&1; then
  echo
  echo "[AMD SMI]"
  amd-smi 2>/dev/null || true
fi

echo
echo "[Python]"
python3 --version 2>/dev/null || true
python3 -m pip --version 2>/dev/null || true

echo
echo "Diagnóstico concluído. Nenhum pacote foi instalado."
