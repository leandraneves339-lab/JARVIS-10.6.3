# Android Text-to-Speech

O JARVIS 10.6.3 usa o mecanismo nativo do Android para falar.

## Requisitos
- Android com Text-to-Speech habilitado.
- Idioma/voz Português (Brasil) disponível no mecanismo TTS do aparelho.
- Buildozer incluindo `pyjnius` (já configurado).

## Comportamento
- Ao iniciar, o JARVIS cria o `TextToSpeech` nativo.
- A resposta usa `QUEUE_FLUSH`, evitando acumular respostas antigas.
- Se o TTS não estiver disponível, o aplicativo reporta o erro em vez de fingir que falou.
- No PC, `pyttsx3` continua sendo usado.
