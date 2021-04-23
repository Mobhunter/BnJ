from django.forms import CharField, EmailField, PasswordInput, Form, BooleanField
from django.core.validators import validate_slug
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import password_validators_help_texts, UserAttributeSimilarityValidator, MinimumLengthValidator
from django.forms.fields import IntegerField
from collections import OrderedDict

class LoginForm(Form):
    user = None
    username = CharField(max_length=255, label="Логин")
    password = CharField(max_length=255, label="Пароль", widget=PasswordInput)
    remember_me = BooleanField(label="Оставаться в системе", required=False)

    def check(self):
        if not self.is_valid() or not self.is_bound:
            return False
        try:
            user = User.objects.get(username=self.cleaned_data["username"])
        except User.DoesNotExist:
            self.add_error("username", "Пользователя с таким логином не существует")
            return False
        else:
            if not check_password(self.cleaned_data["password"], user.password):
                self.add_error("password", "Неверный пароль")
                return False
            elif not user.is_active:
                self.add_error(None, "Этот пользователь не подтвердил свой адрес электронной почты.")
                return False
        self.user = user
        return True


class RegistrationForm(Form):
    genres = []
    instruments = []
    username = CharField(label="Имя пользователя", max_length=150, help_text="Не более 150 символов. Только буквы, цифры и символы @/./+/-/_", validators=[validate_slug])
    email = EmailField(label="Электронная почта")
    password = CharField(label="Пароль", widget=PasswordInput, validators=[UserAttributeSimilarityValidator, MinimumLengthValidator], help_text="\n".join(password_validators_help_texts()))
    password1 = CharField(label="Повторите ваш пароль", widget=PasswordInput)
    age = IntegerField(label="Возраст", required=False)
    Avant_garde_Jazz = BooleanField(required=False, label='Авангардный джаз')
    Afro_Cuban_Jazz = BooleanField(required=False, label='Афро-кубинский джаз')
    Bebop = BooleanField(required=False, label='Бибоп')
    Bossanova = BooleanField(required=False, label='Босанова')
    Jazz_Manush = BooleanField(required=False, label='Джаз-мануш')
    Jazz_Rap = BooleanField(required=False, label='Джаз-рэп')
    Jazz_Funk = BooleanField(required=False, label='Джаз-фанк')
    Jazz_Fusion = BooleanField(required=False, label='Джаз-фьюжн')
    Dixieland = BooleanField(required=False, label='Диксиленд')
    Cool_Jazz = BooleanField(required=False, label='Кул-джаз')
    Latin_American_Jazz = BooleanField(required=False, label='Латиноамериканский джаз')
    Modal_Jazz = BooleanField(required=False, label='Модальный джаз')
    New_Orleans_Jazz = BooleanField(required=False, label='Новоорлеанский джаз')
    Nu_Jazz = BooleanField(required=False, label='Ню-джаз')
    Punk_Jazz = BooleanField(required=False, label='Панк-джаз')
    Postbop = BooleanField(required=False, label='Постбоп')
    Swing = BooleanField(required=False, label='Свинг')
    Ska_Jazz = BooleanField(required=False, label='Ска-джаз')
    Smooth_jazz = BooleanField(required=False, label='Smooth jazz')
    Soul_Jazz = BooleanField(required=False, label='Соул-джаз')
    Stride = BooleanField(required=False, label='Страйд')
    Free_Jazz = BooleanField(required=False, label='Фри-джаз')
    Hard_Bop = BooleanField(required=False, label='Хард-боп')
    Jazz_Fusion = BooleanField(required=False, label='Джаз-фьюжн')
    Chicago_Jazz = BooleanField(required=False, label='Чикагский джаз')
    Acid_Jazz = BooleanField(required=False, label='Эйсид-джаз')
    Alternative_rock = BooleanField(required=False, label='Альтернативный рок')
    Alternative_rock = BooleanField(required=False, label='Арт-рок')
    Beat = BooleanField(required=False, label='Бит')
    Garage_Rock = BooleanField(required=False, label='Гаражный рок')
    Glam_Rock = BooleanField(required=False, label='Глэм-рок')
    Gothic_Rock = BooleanField(required=False, label='Готик-рок')
    Grunge = BooleanField(required=False, label='Гранж')
    Indie_Rock = BooleanField(required=False, label='Инди-рок')
    Instrumental_Rock = BooleanField(required=False, label='Инструментальный рок')
    Math_rock = BooleanField(required=False, label='Математический рок')
    Noise_rock = BooleanField(required=False, label='Нойз-рок')
    Pub_rock = BooleanField(required=False, label='Паб-рок')
    Punk_rock = BooleanField(required=False, label='Панк-рок')
    Post_punk = BooleanField(required=False, label='Пост-панк')
    Proto_punk = BooleanField(required=False, label='Прото-панк')
    Psychedelic_rock = BooleanField(required=False, label='Психоделический рок')
    Southern_Rock = BooleanField(required=False, label='Сатерн-рок')
    Surf_Rock = BooleanField(required=False, label='Сёрф-рок')
    Soft_Rock = BooleanField(required=False, label='Софт-рок')
    Space_Rock = BooleanField(required=False, label='Спейс-рок')
    Stoner_Rock = BooleanField(required=False, label='Стоунер-рок')
    Folk_Rock = BooleanField(required=False, label='Фолк-рок')
    Hard_Rock = BooleanField(required=False, label='Хард-рок')
    Heartland_Rock = BooleanField(required=False, label='Хартленд-рок')
    Experimental_Rock = BooleanField(required=False, label='Экспериментальный рок')
    Christian_Rock = BooleanField(required=False, label='Христианский рок')
    VanguardMetal = BooleanField(required=False, label='Авангард-метал')
    BlackMetal = BooleanField(required=False, label='Блэк-метал')
    Viking_metal = BooleanField(required=False, label='Викинг-метал')
    Glam_metal = BooleanField(required=False, label='Глэм-метал')
    Gothic_metal = BooleanField(required=False, label='Готик-метал')
    Groove_metal = BooleanField(required=False, label='Грув-метал')
    Dark_metal = BooleanField(required=False, label='Дарк-метал')
    Doom_metal = BooleanField(required=False, label='Дум-метал')
    Death_metal = BooleanField(required=False, label='Дэт-метал')
    CelticMetal = BooleanField(required=False, label='Кельтик-метал')
    Mat_metal = BooleanField(required=False, label='Мат-метал')
    Neoclassical_metal = BooleanField(required=False, label='Неоклассический метал')
    OrientalMetal = BooleanField(required=False, label='Ориентал-метал')
    PowerMetal = BooleanField(required=False, label='Пауэр-метал')
    PaganMetal = BooleanField(required=False, label='Пейган-метал')
    Post_metal = BooleanField(required=False, label='Пост-метал')
    Progressive_metal = BooleanField(required=False, label='Прогрессивный метал')
    Symphonic_metal = BooleanField(required=False, label='Симфоник-метал')
    SludgeMetal = BooleanField(required=False, label='Сладж-метал')
    Speed_metal = BooleanField(required=False, label='Спид-метал')
    StonerMetal = BooleanField(required=False, label='Стоунер-метал')
    Thrash_metal = BooleanField(required=False, label='Трэш-метал')
    Folk_metal = BooleanField(required=False, label='Фолк-метал')
    Heavy_metal = BooleanField(required=False, label='Хеви-метал')
    Delta_Blues = BooleanField(required=False, label='Дельта-блюз')
    Electric_Blues = BooleanField(required=False, label='Электрик-блюз')
    Chicago_Blues = BooleanField(required=False, label='Чикаго-блюз')
    Texas_Blues = BooleanField(required=False, label='Техас-блюз')
    Country_Blues = BooleanField(required=False, label='Кантри-блюз')
    Europop = BooleanField(required=False, label='Европоп')
    Dance_pop = BooleanField(required=False, label='Данс-поп')
    Electropop = BooleanField(required=False, label='Электропоп')
    Mashup = BooleanField(required=False, label='Мэшап')
    Operatic_pop = BooleanField(required=False, label='Operatic pop')
    Sophisti_pop = BooleanField(required=False, label='Sophisti-pop')
    Space_age_pop = BooleanField(required=False, label='Space age pop')
    Sunshine_pop = BooleanField(required=False, label='Sunshine pop')
    Tin_pop = BooleanField(required=False, label='Тин-поп')
    Traditional_pop_music = BooleanField(required=False, label='Традиционная поп-музыка')
    J_pop = BooleanField(required=False, label='J-pop')
    K_pop = BooleanField(required=False, label='K-pop')
    C_pop = BooleanField(required=False, label='C-pop')
    Q_pop = BooleanField(required=False, label='Q-pop')
    Mandopop = BooleanField(required=False, label='Mandopop')
    solo_guitar_tool = BooleanField(required=False, label='Соло-гитара')
    rythm_guitar_tool = BooleanField(required=False, label='Ритм-гитара')
    guitar_tool = BooleanField(required=False, label='Соло и ритм - гитара')
    bass_tool = BooleanField(required=False, label='Бас-гитара')
    vocals_tool = BooleanField(required=False, label='Вокал')
    drums_tool = BooleanField(required=False, label='Ударные')
   

    def check(self):
        if not self.is_valid() or not self.is_bound:
            return False
        if self.cleaned_data["password"] != self.cleaned_data["password1"]:
            self.add_error("password", "Пароли не совпадают")
            return False
        query1 = User.objects.filter(email=self.cleaned_data["email"])
        if len(query1) > 0:
            self.add_error("email", "Пользователь с данным адресом почты существует.")
            return False
        query2 = User.objects.filter(username=self.cleaned_data["username"])
        if len(query2) > 0:
            self.add_error("email", "Пользователь с данным псевдонимом существует.")
            return False
        for key, item in self.cleaned_data.items():
            if isinstance(item, bool):
                if key.endswith("tool"):
                    if item:
                        self.instruments.append(key)
                else:
                    if item:
                        self.genres.append(key)
        return True
        

class PasswordResetForm(Form):
    email = EmailField(label="Введите ваш адрес электронной почты")

    def check(self):
        if not self.is_valid() or not self.is_bound:
            return False
        query = User.objects.get(email=self.cleaned_data["email"])
        if len(query) == 0:
            self.add_error(self.email, "Пользователя с данным адресом электронной почты не существует")
            return False
        return True


class PasswordChangeForm(Form):
    password = CharField(label="Придумайте новый пароль", widget=PasswordInput, validators=[UserAttributeSimilarityValidator, MinimumLengthValidator], help_text="\n".join(password_validators_help_texts()))
    password1 = CharField(label="Повторите новый пароль", widget=PasswordInput)

    def check(self):
        if not self.is_valid() or not self.is_bound:
            return False
        if self.cleaned_data["password"] != self.cleaned_data["password1"]:
            self.add_error(self.password, "Пароли не совпадают")
            return False
        return True
    