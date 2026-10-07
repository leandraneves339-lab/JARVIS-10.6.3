# JARVIS 10.6.3 — Android TTS revisado

Esta versão adiciona **Android Text-to-Speech nativo** usando `pyjnius` e `android.speech.tts.TextToSpeech`.

## Melhorias
- Android usa TTS nativo em português do Brasil (`pt-BR`).
- Desktop continua usando `pyttsx3`.
- Diagnóstico distingue TTS disponível de indisponível.
- SpeechRecognizer Android mantém referências Java para evitar coleta prematura.
- Reconhecimento de voz retorna erros ao aplicativo.
- Release limpo sem `__pycache__`/`.pyc`.

## Validação
- Python: `compileall` OK.
- Android físico/emulador: requer teste de execução e mecanismo de voz instalado no dispositivo.
- APK não é declarado como compilado neste pacote.
