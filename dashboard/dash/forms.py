from django import forms
from Store.models import Item , Coupon

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['sku', 'price', 'Category', 'description', 'discAv', 'image' ,'is_Active']

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

class ItemEditForm(forms.ModelForm):

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = Item
        fields = ['price','Category','description','discAv','image','is_Active']

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_value' , 'valid_to', 'is_active']
        widgets = {
            'valid_from': forms.DateInput(attrs={'type': 'date'}),
            'valid_to': forms.DateInput(attrs={'type': 'date'}),
        }