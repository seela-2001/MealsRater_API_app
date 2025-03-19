import uuid
from django.db import models
from customers.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Meal(models.Model):
    meal_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='meals/photo/',null=True,blank=True)

    def __str__(self):
        return self.title
    
class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review = models.TextField(blank=True, null=True)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return str(self.stars)
    
    class Meta:
        unique_together = (('user','meal'),)
        indexes = [
            models.Index(fields=['user','meal']),
        ]
