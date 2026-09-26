import random
import tkinter as tk
from tkinter import font as tkfont


PALAVRAS = {
    "Animais": ["elefante", "girafa", "borboleta", "tartaruga", "leopardo", "canguru"],
    "Frutas": ["abacaxi", "melancia", "morango", "maracuja", "jabuticaba", "carambola"],
    "Países": ["brasil", "portugal", "argentina", "canada", "japao", "alemanha"],
    "Profissões": ["engenheiro", "professor", "medico", "programador", "advogado"],
    "Tecnologia": ["computador", "internet", "algoritmo", "teclado", "monitor", "python"],
}

MAX_ERROS = 6

class EstadoJogo:
    def __init__(self):
        self.categoria = None
        self.palavra = ""
        self.letras_certas = set()
        self.letras_erradas = set()
        self.vitorias = 0
        self.derrotas = 0
        self.nova_palavra()

    def nova_palavra(self):
        self.categoria = random.choice(list(PALAVRAS.keys()))
        self.palavra = random.choice(PALAVRAS[self.categoria]).lower()
        self.letras_certas = set()
        self.letras_erradas = set()

    def tentar(self, letra: str) -> bool:
        letra = letra.lower()
        if letra in self.letras_certas or letra in self.letras_erradas:
            return False 
        if letra in self.palavra:
            self.letras_certas.add(letra)
        else:
            self.letras_erradas.add(letra)
        return True

    @property
    def erros(self) -> int:
        return len(self.letras_erradas)

    @property
    def venceu(self) -> bool:
        return all(c in self.letras_certas for c in self.palavra)

    @property
    def perdeu(self) -> bool:
        return self.erros >= MAX_ERROS

    @property
    def palavra_exibida(self) -> str:
        return " ".join(c if c in self.letras_certas else "_" for c in self.palavra)



class JogoDaForca(tk.Tk):
    COR_FUNDO = "#1e1e2f"
    COR_PAINEL = "#2a2a40"
    COR_TEXTO = "#f2f2f2"
    COR_ACERTO = "#4caf50"
    COR_ERRO = "#e94560"
    COR_BOTAO = "#3b3b58"
    COR_BOTAO_HOVER = "#53537a"

    def __init__(self):
        super().__init__()
        self.title("Jogo da Forca")
        self.configure(bg=self.COR_FUNDO)
        self.resizable(False, False)

        self.estado = EstadoJogo()
        self.botoes_letras = {}

        self.fonte_titulo = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.fonte_palavra = tkfont.Font(family="Consolas", size=26, weight="bold")
        self.fonte_normal = tkfont.Font(family="Segoe UI", size=12)
        self.fonte_botao = tkfont.Font(family="Segoe UI", size=11, weight="bold")

        self._montar_layout()
        self._atualizar_tela()

        self.bind("<Key>", self._tecla_pressionada)


    def _montar_layout(self):
        topo = tk.Frame(self, bg=self.COR_FUNDO)
        topo.pack(pady=(15, 5))

        tk.Label(
            topo, text="🎯 JOGO DA FORCA", font=self.fonte_titulo,
            bg=self.COR_FUNDO, fg=self.COR_TEXTO
        ).pack()

        self.label_categoria = tk.Label(
            topo, text="", font=self.fonte_normal, bg=self.COR_FUNDO, fg="#aaaaee"
        )
        self.label_categoria.pack(pady=(4, 0))

        corpo = tk.Frame(self, bg=self.COR_FUNDO)
        corpo.pack(padx=20, pady=10)

       
        self.canvas = tk.Canvas(
            corpo, width=220, height=250, bg=self.COR_PAINEL, highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, padx=(0, 20))
        self._desenhar_forca_base()

       
        painel_direito = tk.Frame(corpo, bg=self.COR_FUNDO)
        painel_direito.grid(row=0, column=1, sticky="n")

        self.label_palavra = tk.Label(
            painel_direito, text="", font=self.fonte_palavra,
            bg=self.COR_FUNDO, fg=self.COR_TEXTO
        )
        self.label_palavra.pack(pady=(10, 15))

        self.label_erradas = tk.Label(
            painel_direito, text="Letras erradas: ", font=self.fonte_normal,
            bg=self.COR_FUNDO, fg=self.COR_ERRO
        )
        self.label_erradas.pack()

        self.label_placar = tk.Label(
            painel_direito, text="", font=self.fonte_normal,
            bg=self.COR_FUNDO, fg="#cccccc"
        )
        self.label_placar.pack(pady=(10, 0))

        self.label_mensagem = tk.Label(
            painel_direito, text="", font=("Segoe UI", 13, "bold"),
            bg=self.COR_FUNDO, fg=self.COR_ACERTO
        )
        self.label_mensagem.pack(pady=(15, 0))

     
        teclado = tk.Frame(self, bg=self.COR_FUNDO)
        teclado.pack(pady=(5, 10))

        alfabeto = "abcdefghijklmnopqrstuvwxyz"
        linhas = [alfabeto[:9], alfabeto[9:18], alfabeto[18:]]
        for linha_idx, linha in enumerate(linhas):
            frame_linha = tk.Frame(teclado, bg=self.COR_FUNDO)
            frame_linha.pack(pady=2)
            for letra in linha:
                btn = tk.Button(
                    frame_linha, text=letra.upper(), width=3, font=self.fonte_botao,
                    bg=self.COR_BOTAO, fg=self.COR_TEXTO, activebackground=self.COR_BOTAO_HOVER,
                    relief="flat", bd=0,
                    command=lambda l=letra: self._clicar_letra(l)
                )
                btn.pack(side="left", padx=2)
                self.botoes_letras[letra] = btn

       
        self.botao_reiniciar = tk.Button(
            self, text="🔄 Nova Palavra", font=self.fonte_botao,
            bg="#5a5adf", fg="white", activebackground="#7a7aff",
            relief="flat", bd=0, padx=10, pady=6,
            command=self._reiniciar
        )
        self.botao_reiniciar.pack(pady=(0, 15))


    def _desenhar_forca_base(self):
        c = self.canvas
       
        c.create_line(20, 230, 150, 230, fill="#ffffff", width=4)
        
        c.create_line(50, 230, 50, 20, fill="#ffffff", width=4)
        
        c.create_line(50, 20, 150, 20, fill="#ffffff", width=4)
        
        c.create_line(150, 20, 150, 50, fill="#ffffff", width=3)

    def _desenhar_boneco(self, erros: int):
        c = self.canvas
        c.delete("boneco")
        partes = [
            lambda: c.create_oval(130, 50, 170, 90, width=3, outline=self.COR_ERRO, tags="boneco"),  # cabeça
            lambda: c.create_line(150, 90, 150, 150, width=3, fill=self.COR_ERRO, tags="boneco"),     # tronco
            lambda: c.create_line(150, 105, 120, 130, width=3, fill=self.COR_ERRO, tags="boneco"),    # braço esq
            lambda: c.create_line(150, 105, 180, 130, width=3, fill=self.COR_ERRO, tags="boneco"),    # braço dir
            lambda: c.create_line(150, 150, 125, 190, width=3, fill=self.COR_ERRO, tags="boneco"),    # perna esq
            lambda: c.create_line(150, 150, 175, 190, width=3, fill=self.COR_ERRO, tags="boneco"),    # perna dir
        ]
        for i in range(min(erros, len(partes))):
            partes[i]()

    def _tecla_pressionada(self, evento):
        letra = evento.char.lower()
        if letra.isalpha() and len(letra) == 1:
            self._clicar_letra(letra)

    def _clicar_letra(self, letra: str):
        if self.estado.venceu or self.estado.perdeu:
            return
        valido = self.estado.tentar(letra)
        if not valido:
            return

        btn = self.botoes_letras.get(letra)
        if btn:
            if letra in self.estado.letras_certas:
                btn.configure(bg=self.COR_ACERTO, state="disabled")
            else:
                btn.configure(bg=self.COR_ERRO, state="disabled")

        self._atualizar_tela()

    def _atualizar_tela(self):
        estado = self.estado
        self.label_categoria.config(text=f"Categoria: {estado.categoria}")
        self.label_palavra.config(text=estado.palavra_exibida.upper())
        self.label_erradas.config(
            text="Letras erradas: " + ", ".join(sorted(l.upper() for l in estado.letras_erradas))
        )
        self.label_placar.config(
            text=f"✅ Vitórias: {estado.vitorias}    ❌ Derrotas: {estado.derrotas}    "
                 f"Tentativas restantes: {MAX_ERROS - estado.erros}"
        )
        self._desenhar_boneco(estado.erros)

        if estado.venceu:
            self.label_mensagem.config(text="🎉 Parabéns, você venceu!", fg=self.COR_ACERTO)
            estado.vitorias += 1
            self._travar_teclado()
        elif estado.perdeu:
            self.label_mensagem.config(
                text=f"💀 Você perdeu! A palavra era: {estado.palavra.upper()}",
                fg=self.COR_ERRO
            )
            estado.derrotas += 1
            self._travar_teclado()
        else:
            self.label_mensagem.config(text="")

    def _travar_teclado(self):
        for btn in self.botoes_letras.values():
            btn.configure(state="disabled")

    def _reiniciar(self):
        vitorias, derrotas = self.estado.vitorias, self.estado.derrotas
        self.estado = EstadoJogo()
        self.estado.vitorias, self.estado.derrotas = vitorias, derrotas
        for btn in self.botoes_letras.values():
            btn.configure(state="normal", bg=self.COR_BOTAO)
        self._atualizar_tela()


if __name__ == "__main__":
    app = JogoDaForca()
    app.mainloop()