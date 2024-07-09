from django.db import models # type: ignore
from django.utils import timezone # type: ignore
import re
from input_mask.widgets import InputMask # type: ignore

class Collaborator(models.Model):
    name = models.CharField(max_length=100)  # Nome do colaborador
    birth_date = models.DateField(default=timezone.now)  # Data de nascimento do colaborador
    cpf = models.CharField(max_length=11, unique=True, default='00000000000')  # CPF do Collaborado 
  
    def __str__(self):
        return f"Collaborator: {self.name}, Birthday: {self.birth_date}"  # Método para retornar a representação em string do colaborador

    def save(self, *args, **kwargs):
        # Método para salvar o objeto no banco de dados. Valida o CPF antes de salvar.
        if not self.validate_cpf(self.cpf):
            raise ValueError("Invalid CPF")
        super().save(*args, **kwargs)

    @staticmethod
    def validate_cpf(cpf):
        # Método estático para validar o CPF. Retorna True se o CPF for válido, caso contrário, retorna False.
        numbers = [int(digit) for digit in cpf if digit.isdigit()]
        formatting = False
        digit_quantity = False
        validation1 = False
        validation2 = False

         # Primeiro, verifica a formatação e a quantidade de dígitos do CPF.

        if re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
            formatting = True

        
        if len(numbers) == 11:
            digit_quantity = True
             # Em seguida, realiza a validação dos dois dígitos verificadores do CPF.
            sum_products = sum(a*b for a, b in zip (numbers[0:9], range (10, 1, -1)))
            expected_digit = (sum_products * 10 % 11) % 10
            if numbers[9] == expected_digit:
                validation1 = True
           
            sum_products1 = sum(a*b for a, b in zip(numbers [0:10], range (11, 1, -1)))
            expected_digit1 = (sum_products1 *10 % 11) % 10
            if numbers[10] == expected_digit1:
                validation2 = True

        # Return True if all validations pass
        return digit_quantity and formatting and validation1 and validation2
