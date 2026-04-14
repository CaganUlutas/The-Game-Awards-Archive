from django.db import models
from django.utils.text import slugify

class Game(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    description = models.TextField(null=True, blank=True)
    trailer_url = models.URLField(null=True, blank=True)

    metacritic_score = models.IntegerField(null=True, blank=True)
    released = models.DateField(null=True, blank=True)

    hltb_main = models.CharField(max_length=50, blank=True, null=True)
    hltb_extra = models.CharField(max_length=50, blank=True, null=True)
    hltb_completionist = models.CharField(max_length=50, blank=True, null=True)

    background_image = models.URLField(null=True, blank=True)

    rating = models.FloatField(null=True, blank=True)  # RAWG rating
    ratings_count = models.IntegerField(null=True, blank=True)

    developers = models.CharField(max_length=255, null=True, blank=True)
    genres = models.CharField(max_length=255, null=True, blank=True)
    platforms = models.CharField(max_length=255, null=True, blank=True)
    
    steam_url = models.URLField(null=True, blank=True)
    playstation_url = models.URLField(null=True, blank=True)
    xbox_url = models.URLField(null=True, blank=True)
    nintendo_url = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
        else:
            base_slug = self.slug

        slug = base_slug
        counter = 1

        while Game.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AwardYear(models.Model):
    year = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.year)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Nomination(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    year = models.ForeignKey(AwardYear, on_delete=models.CASCADE)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.game} - {self.category} ({self.year})"
