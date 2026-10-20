import re
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect

User = get_user_model()

def register_view(request):

    # Если пользователь уже вошёл,
    # повторно регистрироваться ему не нужно
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        # Получаем данные
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
     
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        agreement = request.POST.get("agreement")


        # Здесь будут ошибки
        errors = {}


        # =========================================
        # ИМЯ
        # =========================================



        # =========================================
        # ФАМИЛИЯ
        # =========================================




        # =========================================
        # USERNAME
        # =========================================

        if not username:

            errors["username"] = "Введите логин."

        elif len(username) < 3:

            errors["username"] = (
                "Логин должен содержать минимум 3 символа."
            )

        elif len(username) > 150:

            errors["username"] = "Логин слишком длинный."

        elif not re.match(r"^[\w.@+-]+$", username):

            errors["username"] = (
                "Логин может содержать буквы, цифры "
                "и символы @ . + - _"
            )

        elif User.objects.filter(
            username__iexact=username
        ).exists():

            errors["username"] = (
                "Пользователь с таким логином уже существует."
            )


        # =========================================
        # EMAIL
        # =========================================

        if not email:

            errors["email"] = "Введите Email."

        else:

            try:
                validate_email(email)

            except ValidationError:

                errors["email"] = (
                    "Введите корректный Email."
                )

            else:

                if User.objects.filter(
                    email__iexact=email
                ).exists():

                    errors["email"] = (
                        "Пользователь с таким Email "
                        "уже зарегистрирован."
                    )


        # =========================================
        # ТЕЛЕФОН
        # =========================================




        # =========================================
        # ПАРОЛЬ
        #=========================================

        if not password1:
            errors["password1"] = "Введите пароль."

        if not password2:

            errors["password2"] = (
                "Повторите пароль."
            )


        if (
            password1
            and password2
            and password1 != password2
        ):

            errors["password2"] = (
                "Пароли не совпадают."
            )


        # =========================================
        # ПРОВЕРКА НАДЁЖНОСТИ ПАРОЛЯ DJANGO
        # =========================================

        if password1 and password1 == password2:

            # Создаём временного пользователя,
            # чтобы Django мог проверить,
            # не похож ли пароль на username/email
            temp_user = User(
                username=username,
                email=email,

            )

            try:

                validate_password(
                    password1,
                    user=temp_user
                )

            except ValidationError as error:

                errors["password1"] = " ".join(
                    error.messages
                )


        # =========================================
        # СОГЛАСИЕ С ПРАВИЛАМИ
        # =========================================

        if not agreement:

            errors["agreement"] = (
                "Необходимо принять правила сайта."
            )


        # =========================================
        # ЕСЛИ ЕСТЬ ОШИБКИ
        # =========================================

        if errors:

            context = {
                "errors": errors,
                "form_data": {

                    "username": username,
                    "email": email,

                }
            }

            return render(
                request,
                "registration/register.html",
                context
            )

        try:

            with transaction.atomic():

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,

                )


                # Если в твоей User-модели
                # позже появится поле phone
                if any(
                    field.name == "phone"
                    for field in User._meta.fields
                ):

            

                    user.save(
                        update_fields=["phone"]
                    )


        except IntegrityError:

            messages.error(
                request,
                "Не удалось создать аккаунт. "
                "Проверьте введённые данные."
            )
            return render(
                request,
                "registration/register.html",
                {
                    "form_data": {

                        "username": username,
                        "email": email,
  
                    }
                }
            )

        login(
            request,
            user
        )
        messages.success(
            request,
            "Регистрация успешно завершена!"
        )
        return redirect("home")
    return render(
        request,
        "registration/register.html"
    )

def login_view(request):
    return render(
        request,
        "registration/login.html"
    )

@login_required
def profile(request):
    places = request.user.listings.select_related("category")
    return render(request, "registration/profile.html", {"places": places})


@login_required
def profile_edit(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("profile")
    return render(request, "registration/profile_edit.html", {"form": form})


def logout_view(request):

    if request.user.is_authenticated:
        logout(request)
        messages.success(
            request,
            "Вы успешно вышли из аккаунта."
        )

    return redirect("home")