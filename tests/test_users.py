from app.models import User


def test_password_is_hashed():
    user = User(
        username="mazel",
        email="mazel@example.com",
    )

    user.set_password("Example-Strong-Password-123!")

    assert user.password_hash != "Example-Strong-Password-123!"
    assert user.check_password("Example-Strong-Password-123!")
    assert not user.check_password("wrong-password")


def test_same_password_produces_different_hashes():
    first = User(
        username="user_one",
        email="one@example.com",
    )
    second = User(
        username="user_two",
        email="two@example.com",
    )

    first.set_password("Example-Strong-Password-123!")
    second.set_password("Example-Strong-Password-123!")

    assert first.password_hash != second.password_hash
