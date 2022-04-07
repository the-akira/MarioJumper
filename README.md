# Mario Jumper

Desenvolvido para o Desafio Simplicode.

![img](https://raw.githubusercontent.com/the-akira/MarioJumper/main/images/screenshot.png)

## Instalação

Para jogar **Mario Jumper** é necessário ter o [Python](https://www.python.org/downloads/) instalado em sua máquina.

Realize a clonagem do repositório:

```
git clone https://github.com/the-akira/MarioJumper.git
```

Instale a biblioteca [PyGame](https://www.pygame.org/wiki/GettingStarted):

```
python3 -m pip install -U pygame --user
```

Dentro do diretório principal, execute o jogo através do comando:

```
python3 main.py
```

Boa diversão!

## Regras do Jogo

- Você deve desviar dos inimigos, seja rápido.
- As moedas aparecem em posições aleatórias, para vencer é necessário coletar 20 moedas.
- Se a barra verde acabar (ou seja, sua vida zerou), significa que você perdeu.
- O cogumelo verde é capaz de curar a sua vida.

## Controles

- `arrow keys`: para mover o personagem (:arrow_left: esquerda) e (direita :arrow_right:)
- `barra de espaço`: para pular
- `p`: para pausar o jogo