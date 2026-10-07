# JARVIS 10.5

Assistente pessoal multiplataforma com uma interface HUD inspirada na referência enviada pelo usuário.

## Plataformas
- Windows/Linux/macOS: interface Kivy + comandos + TTS local.
- Android: interface Kivy + integração opcional com reconhecimento de voz e TTS nativos.

## Instalação no computador

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

## Android

A forma recomendada é compilar com Buildozer em Linux/WSL:

```bash
pip install buildozer
buildozer android debug
```

O arquivo `buildozer.spec` já contém as dependências básicas.

## Configuração
Copie `.env.example` para `.env` e preencha somente o que quiser usar.
O Jarvis funciona sem chave de API: nesse modo ele usa comandos locais e respostas básicas.

## Estados
ONLINE, LISTENING, THINKING, SPEAKING e OFFLINE.

## Comandos locais
- "hora"
- "data"
- "status do sistema"
- "abrir navegador"
- "abrir calculadora"
- "quem é você"
- "desligar jarvis"

O código foi separado em núcleo, voz e interface para permitir adicionar novos módulos sem quebrar a interface.


## JARVIS 10.5.1
Inclui:
- memória local em JSON;
- roteador de ações com lista fechada;
- IA opcional por endpoint HTTP configurável;
- comandos "lembre ..." e "o que você lembra";
- maior separação entre interface, núcleo, memória e ações.

A IA é opcional. Sem configurar `JARVIS_API_URL`, o núcleo local continua funcionando.

## JARVIS 10.5.2
- Reconhecimento de voz no computador via SpeechRecognition.
- Reconhecimento nativo no Android.
- Painéis reativos de diagnóstico.
- Contador de comandos e indicação de estado da voz.
- IA externa continua opcional e configurável.

## JARVIS 10.6.0
- Modo de escuta contínua com palavra de ativação configurável.
- Botão WAKE para ligar/desligar o modo contínuo.
- O reconhecimento só encaminha uma frase quando detecta a palavra de ativação.
- Exemplo: "Jarvis, que horas são?"
- O modo contínuo depende do reconhecimento de voz disponível no dispositivo.

## JARVIS 10.6.1
- HUD reconstruído com anéis segmentados, núcleo animado, telemetria, varredura e marcadores.
- Centro da interface mostra o estado atual do núcleo.
- Visual desenhado por código para adaptar-se a diferentes tamanhos de tela.
