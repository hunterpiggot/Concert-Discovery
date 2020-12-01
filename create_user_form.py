from models import UserInformation


def create_user(form):
    email = form.email.data
    first_name = form.first_name.data
    last_name = form.last_name.data
    password = form.password.data
    city = form.city.data
    state = form.state.data
    search_radius = form.search_radius.data
    new_user = UserInformation.register(
        email, first_name, last_name, password, city, state, search_radius
    )
    return new_user
