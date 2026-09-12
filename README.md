# Dojang de Bolso

App de treino de Taekwondo **ATA Songahm** feito para o Felipe, faixa azul decidida
na ATA de Londrina. Abre no celular, instala na tela de início e funciona offline.

**No ar:** https://renatanz86-oss.github.io/dojang-felipe/

Não tem nenhuma relação com o Impulso nem com o repositório `elevo` — é projeto separado.

## O que tem dentro

| Aba | O que faz |
| --- | --- |
| **Hoje** | Forma atual, foco técnico do dia, sequência de dias treinados, treino guiado |
| **Formas** | As 11 formas Songahm, contador de voltas, os 10 pontos que o instrutor avalia, anotações |
| **Sparring** | Cronômetro de rounds configurável, placar, 8 combinações explicadas, checklist de equipamento |
| **Armas** | Bastão, nunchaku, bastões curtos, faca e kamas: segurança, drills e a sequência da escola |
| **Mais** | Chutes desenhados e animados, vídeos para assistir, coreano com quiz, escada de faixas, campeonato, diário, gravação de vídeo |

O **treino guiado** monta a sessão (15, 30 ou 45 min) e conduz passo a passo com
cronômetro, bipe e vibração; ao terminar, registra sozinho no diário.

Os **chutes** são desenhados por um boneco articulado paramétrico: cada movimento
tem três poses (guarda → câmara → extensão) e o app interpola entre elas.
Nada de imagem externa — o desenho é gerado em SVG na hora.

## Dados

Tudo fica **no aparelho do aluno**: `localStorage` para progresso, diário, anotações
e recordes; `IndexedDB` para os vídeos e fotos que ele grava. Nada é enviado para
servidor nenhum, não há login e não há conta.

## Conteúdo da ATA

As formas Songahm são material registrado da ATA e os vídeos oficiais ficam no
MyATA, com o login da escola. Este app **não reproduz** esse material: o que é
específico da ATA (sequência de movimentos, pontuação de campeonato, exigências de
exame) aparece sempre marcado para confirmar com o instrutor, com campos editáveis
para o aluno anotar o que vem da aula. Os vídeos linkados são de canais abertos de
escolas licenciadas, identificados pelo canal.

## Como mexer

`src/app.html` é a fonte única. Depois de editar:

```bash
python build.py
git add -A && git commit -m "..." && git push
```

O GitHub Pages republica sozinho em um ou dois minutos. O `build.py` embrulha a
fonte num documento HTML completo, gera o `sw.js` com um novo número de cache
(assim o celular pega a versão nova) e não toca em mais nada.
