from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator
)


class RussianUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if not user:
            return
        super().validate(password, user)

    def get_help_text(self):
        return _('Пароль не должен быть слишком похож на другую вашу личную информацию.')


class RussianMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _('Этот пароль слишком короткий. Он должен содержать минимум %(min_length)d символов.'),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _('Ваш пароль должен содержать минимум %(min_length)d символов.') % {'min_length': self.min_length}


class RussianCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _('Этот пароль слишком распространён.'),
                code='password_too_common',
            )

    def get_help_text(self):
        return _('Ваш пароль не может быть широко используемым паролем.')


class RussianNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _('Этот пароль полностью состоит из цифр.'),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _('Ваш пароль не может полностью состоять из цифр.')

