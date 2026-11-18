import tkinter as tk
import tkinter.font as tkfont

primeiro = None
operacao = ''
novo = True
SIMBOLOS = {'+': '+', '-': '−', '*': '×', '/': '÷', '**': '^'}


def calcular(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            return None
        return a / b
    elif op == '**':
        try:
            return a ** b
        except OverflowError:
            return None


def formatar(x):
    if isinstance(x, complex):
        return 'Erro'
    texto = f'{x:.3f}'.rstrip('0').rstrip('.')
    if texto == '-0':
        texto = '0'
    return texto


def mostrar_erro(mensagem):
    global primeiro, operacao, novo
    visor.set(mensagem)
    conta.set('')
    primeiro = None
    operacao = ''
    novo = True


def ler_visor():
    try:
        return float(visor.get())
    except ValueError:
        return None


def apertar_numero(n):
    global novo
    if novo:
        visor.set('')
        novo = False
    if n == '.' and '.' in visor.get():
        return
    if n == '.' and visor.get() == '':
        visor.set('0')
    visor.set(visor.get() + n)


def apertar_operacao(op):
    global primeiro, operacao, novo
    numero = ler_visor()
    if numero is None:
        return
    if primeiro is not None and not novo:
        resultado = calcular(primeiro, numero, operacao)
        if resultado is None or formatar(resultado) == 'Erro':
            mostrar_erro('Não é possível')
            return
        primeiro = resultado
        visor.set(formatar(resultado))
    elif primeiro is None:
        primeiro = numero
    operacao = op
    novo = True
    conta.set(f'{formatar(primeiro)} {SIMBOLOS[op]}')


def apertar_igual():
    global primeiro, operacao, novo
    numero = ler_visor()
    if primeiro is None or numero is None:
        return
    resultado = calcular(primeiro, numero, operacao)
    if resultado is None or formatar(resultado) == 'Erro':
        if operacao == '/':
            mostrar_erro('Não divide por 0')
        else:
            mostrar_erro('Não é possível')
        return
    conta.set(f'{formatar(primeiro)} {SIMBOLOS[operacao]} {formatar(numero)} =')
    visor.set(formatar(resultado))
    primeiro = None
    operacao = ''
    novo = True


def limpar():
    global primeiro, operacao, novo
    visor.set('0')
    conta.set('')
    primeiro = None
    operacao = ''
    novo = True


def apagar():
    global novo
    if novo:
        return
    texto = visor.get()[:-1]
    if texto == '' or texto == '-':
        visor.set('0')
        novo = True
    else:
        visor.set(texto)


def trocar_sinal():
    numero = ler_visor()
    if numero is None:
        return
    visor.set(formatar(-numero))


def tecla(evento):
    t = evento.char
    piscar(t, evento.keysym)
    if t in '0123456789.':
        apertar_numero(t)
    elif t == ',':
        apertar_numero('.')
    elif t in '+-*/':
        apertar_operacao(t)
    elif t == '^':
        apertar_operacao('**')
    elif t == '=' or evento.keysym in ('Return', 'KP_Enter'):
        apertar_igual()
    elif evento.keysym == 'BackSpace':
        apagar()
    elif evento.keysym == 'Escape':
        limpar()


FUNDO = '#121218'
CARTAO = '#1b1b24'
TEXTO = '#f4f4f8'
APAGADO = '#7d7d92'
ESTILOS = {
    'numero': ('#262632', '#30303e', '#1f1f29', TEXTO),
    'especial': ('#34344a', '#3e3e57', '#2b2b3e', '#c9c9ff'),
    'operacao': ('#2e2a52', '#3a3466', '#262245', '#a89bff'),
    'igual': ('#7c6cff', '#8f81ff', '#6a5ae6', '#ffffff'),
}


class Botao(tk.Canvas):
    def __init__(self, pai, texto, tipo, funcao, largura=78, altura=64):
        super().__init__(pai, width=largura, height=altura, bg=FUNDO, highlightthickness=0, cursor='hand2')
        self.normal, self.hover, self.apertado, letra = ESTILOS[tipo]
        self.funcao = funcao
        self.forma = self.retangulo(2, 2, largura - 2, altura - 2, 18, self.normal)
        self.create_text(largura / 2, altura / 2, text=texto, fill=letra, font=(FONTE, 19, 'bold' if tipo != 'numero' else 'normal'))
        self.bind('<Enter>', lambda e: self.pintar(self.hover))
        self.bind('<Leave>', lambda e: self.pintar(self.normal))
        self.bind('<ButtonPress-1>', lambda e: self.pintar(self.apertado))
        self.bind('<ButtonRelease-1>', self.soltar)

    def retangulo(self, x1, y1, x2, y2, r, cor):
        pontos = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
                  x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
        return self.create_polygon(pontos, smooth=True, fill=cor, outline='')

    def pintar(self, cor):
        self.itemconfig(self.forma, fill=cor)

    def soltar(self, evento):
        self.pintar(self.hover)
        self.funcao()

    def piscar(self):
        self.pintar(self.apertado)
        self.after(120, lambda: self.pintar(self.normal))


def ajustar_visor(*args):
    tamanho = len(visor.get())
    if tamanho <= 9:
        rotulo_visor.config(font=(FONTE, 44, 'bold'))
    elif tamanho <= 13:
        rotulo_visor.config(font=(FONTE, 32, 'bold'))
    else:
        rotulo_visor.config(font=(FONTE, 22, 'bold'))


def piscar(t, nome):
    mapa = {'*': '×', '/': '÷', '-': '−', '^': 'xʸ', ',': '.', '=': '='}
    if nome in ('Return', 'KP_Enter'):
        t = '='
    elif nome == 'BackSpace':
        t = '⌫'
    elif nome == 'Escape':
        t = 'C'
    t = mapa.get(t, t)
    if t in todos_botoes:
        todos_botoes[t].piscar()


janela = tk.Tk()
janela.title('Calculadora')
janela.configure(bg=FUNDO, padx=18, pady=18)
janela.resizable(False, False)

FONTE = 'Arial'
for nome in ('Segoe UI Variable Display', 'Segoe UI', 'Inter', 'DejaVu Sans'):
    if nome in tkfont.families():
        FONTE = nome
        break

visor = tk.StringVar(value='0')
conta = tk.StringVar(value='')

cartao = tk.Frame(janela, bg=CARTAO, padx=18, pady=14)
cartao.grid(row=0, column=0, columnspan=4, sticky='we', pady=(0, 14))
tk.Label(cartao, textvariable=conta, anchor='e', bg=CARTAO, fg=APAGADO,
         font=(FONTE, 13)).pack(fill='x')
rotulo_visor = tk.Label(cartao, textvariable=visor, anchor='e', bg=CARTAO, fg=TEXTO,
                        font=(FONTE, 44, 'bold'), height=1)
rotulo_visor.pack(fill='x')
visor.trace_add('write', ajustar_visor)

botoes = [
    ('C', 'especial', limpar), ('⌫', 'especial', apagar), ('xʸ', 'operacao', lambda: apertar_operacao('**')), ('÷', 'operacao', lambda: apertar_operacao('/')),
    ('7', 'numero', None), ('8', 'numero', None), ('9', 'numero', None), ('×', 'operacao', lambda: apertar_operacao('*')),
    ('4', 'numero', None), ('5', 'numero', None), ('6', 'numero', None), ('−', 'operacao', lambda: apertar_operacao('-')),
    ('1', 'numero', None), ('2', 'numero', None), ('3', 'numero', None), ('+', 'operacao', lambda: apertar_operacao('+')),
    ('±', 'especial', trocar_sinal), ('0', 'numero', None), ('.', 'numero', None), ('=', 'igual', apertar_igual),
]

todos_botoes = {}
for i, (texto, tipo, funcao) in enumerate(botoes):
    if funcao is None:
        funcao = lambda n=texto: apertar_numero(n)
    b = Botao(janela, texto, tipo, funcao)
    b.grid(row=1 + i // 4, column=i % 4, padx=5, pady=5)
    todos_botoes[texto] = b

janela.bind('<Key>', tecla)
janela.mainloop()
