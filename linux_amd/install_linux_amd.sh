#!/usr/bin/env bash
set -euo pipefail

echo "JARVIS AMD/ROCm installer"
echo "Este script NÃO escolhe uma GPU ou distribuição à força."
echo "Confira a compatibilidade oficial do ROCm 7.14 antes de prosseguir."
echo

if ! command -v apt >/dev/null 2>&1; then
  echo "Este instalador automático foi preparado para sistemas Debian/Ubuntu com apt."
  echo "Use o instalador oficial da AMD para outras distribuições."
  exit 1
fi

echo "[1/3] Dependências Python..."
sudo apt update
sudo apt install -y python3 python3-pip python3-setuptools python3-wheel

echo
echo "[2/3] Verificação do sistema..."
uname -r
if command -v lspci >/dev/null 2>&1; then
  lspci | grep -Ei 'VGA|3D|Display|AMD/ATI' || true
fi

echo
echo "[3/3] ROCm..."
echo "Por segurança, a instalação do ROCm/amdgpu NÃO é feita automaticamente."
echo "Use o instalador oficial da AMD após confirmar GPU + distro + kernel."
echo
echo "Para ROCm 7.14, consulte:"
echo "https://rocm.docs.amd.com/en/docs-7.14.0/install/rocm.html"
echo
echo "Depois de instalar, execute:"
echo "  ./check_amd_rocm.sh"
