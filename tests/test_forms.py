from forms import Username


def test_username_form_valid():
    form = Username(data={"username": "Martin"})

    assert form.validate() is True


def test_username_form_empty():
    form = Username(data={"username": ""})

    assert form.validate() is False