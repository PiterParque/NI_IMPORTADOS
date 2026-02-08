from django import forms
from loja.models import Usuario, Produto, Pedido,Endereco,ItemPedido

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
        fields = [
            "cliente",
            "status",
            "endereco_entrega",
        ]


class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = [
            "perfume",
            "quantidade",
            "preco_unitario",
        ]
class EnderecoForm(forms.ModelForm):
    class Meta:
        model=Endereco
        fields="__all__"
        exclude = ['user'] 
EnderecoFormSet = forms.inlineformset_factory(
    Usuario,
    Endereco,
    form=EnderecoForm,
    extra=1,
    can_delete=True
)
ItemPedidoFormSet = forms.inlineformset_factory(
    Pedido,
    ItemPedido,
    form=ItemPedidoForm,
    extra=1,
    can_delete=True
)
