from allauth.account.adapter import DefaultAccountAdapter


class CustomAdapter(DefaultAccountAdapter):
    def clean_display_name(self, display_name):
        return display_name

    def clean_state(self, state):
        return state

    def save_user(self, request, user, form, commit=True):
        user = super(CustomAdapter, self).save_user(request, user, form, commit=False)
        user.display_name = form.cleaned_data.get('display_name')
        user.state = form.cleaned_data.get('state')
        user.save()