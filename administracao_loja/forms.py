from django import forms
from loja.models import Usuario, Produto, Pedido,Endereco

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
class EnderecoForm(forms.ModelForm):
    class Meta:
        model=Endereco
        fields="__all__"
        exclude = ["usuario"]
