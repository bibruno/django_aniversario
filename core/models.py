from django.db import models # type: ignore
from django.utils import timezone # type: ignore
import re

class Collaborator(models.Model):
    name = models.CharField(max_length=100)  # Collaborator's name
    birth_date = models.DateField(default=timezone.now)  # Collaborator's birth date
    cpf = models.CharField(max_length=11, unique=True, default='00000000000')  # Collaborator's CPF
  
    def __str__(self):
        return f"Collaborator: {self.name}, Birthday: {self.birth_date}"  # String representation of the collaborator

    def save(self, *args, **kwargs):
        # Validate CPF before saving
        if not self.validate_cpf(self.cpf):
            raise ValueError("Invalid CPF")
        super().save(*args, **kwargs)

    @staticmethod
    def validate_cpf(cpf):
        # Extract only the digits from CPF, ignoring special characters
        numbers = [int(digit) for digit in cpf if digit.isdigit()]
        formatting = False
        digit_quantity = False
        validation1 = False
        validation2 = False

        # Check the structure of the CPF (111.222.333-44)
        if re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
            formatting = True

        # Check if the CPF has 11 digits
        if len(numbers) == 11:
            digit_quantity = True
            # Validate the first check digit
            sum_products = sum(a*b for a, b in zip (numbers[0:9], range (10, 1, -1)))
            expected_digit = (sum_products * 10 % 11) % 10
            if numbers[9] == expected_digit:
                validation1 = True

            # Validate the second check digit
            sum_products1 = sum(a*b for a, b in zip(numbers [0:10], range (11, 1, -1)))
            expected_digit1 = (sum_products1 *10 % 11) % 10
            if numbers[10] == expected_digit1:
                validation2 = True

        # Return True if all validations pass
        return digit_quantity and formatting and validation1 and validation2
