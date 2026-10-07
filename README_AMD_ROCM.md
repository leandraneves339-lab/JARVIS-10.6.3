# JARVIS — Linux AMD / ROCm

Incluído nesta versão:
- detecção de GPU AMD
- detecção do módulo `amdgpu`
- detecção de ROCm/`rocminfo`
- detecção de ferramentas SMI
- `python3-setuptools`
- `python3-wheel`
- diagnóstico do kernel

## Segurança da instalação

O instalador **não força** `amdgpu-dkms` ou uma versão de kernel específica.
ROCm depende da combinação entre GPU, distribuição, kernel, driver e firmware.

Use primeiro:

```bash
cd linux_amd
./check_amd_rocm.sh
```

Para Debian/Ubuntu, o auxiliar:

```bash
./install_linux_amd.sh
```

instala somente as dependências Python e mostra o próximo passo. A instalação do driver/ROCm deve ser feita de acordo com a matriz oficial da AMD.
