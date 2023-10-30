from django.db import models
from datetime import datetime
from django.template.defaultfilters import slugify


# HOME SECTION

class Home(models.Model):
    name = models.CharField(max_length=20)
    greetings_1 = models.CharField(max_length=5)
    greetings_2 = models.CharField(max_length=5)
    #home_picture = models.ImageField(upload_to='picture/')
    # save time when modified
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# ABOUT SECTION

class About(models.Model):
    heading = models.CharField(max_length=50)
    career = models.CharField(max_length=20)
    description = models.TextField(blank=False)
    #profile_img = models.ImageField(upload_to='profile/')

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.career


class Profile(models.Model):
    about = models.ForeignKey(About,
                              on_delete=models.CASCADE)
    social_name = models.CharField(max_length=10)
    link = models.URLField(max_length=200)


# SKILLS SECTION

class Category(models.Model):
    name = models.CharField(max_length=20)

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return self.name


class Skills(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=20)


# PORTFOLIO SECTION

class Portfolio(models.Model):
    cv_file = models.FileField(upload_to='doc/', null=True, default=None)

    def __str__(self):
        return f'Portfolio {self.id}'


# BLOG CATEGORIES

class BlogCategories(models.TextChoices):
    WORLD = 'world'
    #ENVIRONMENT = 'environment'
    TECHNOLOGY = 'technology'
    #DESIGN = 'design'
    #CULTURE = 'culture'
    BUSINESS = 'business'
   # POLITICS = 'politics'
    OPINION = 'opinion'
    SCIENCE = 'science'
    HEALTH = 'health'
    STYLE = 'style'
    TRAVEL = 'travel'


# BLOG MONTHS

class BlogMonths(models.TextChoices):
    JANUARY = 'styczeń'
    FEBRUARY = 'luty'
    MARCH = 'marzec'
    APRIL = 'kwiecień'
    MAY = 'maj'
    JUNE = 'czerwiec'
    JULY = 'lipiec'
    AUGUST = 'sierpień'
    SEPTEMBER = 'wrzesień'
    OCTOBER = 'październik'
    NOVEMBER = 'listopad'
    DECEMBER = 'grudzień'


# POST SECTION

class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    category = models.CharField(max_length=50, choices=BlogCategories.choices, default=BlogCategories.WORLD)
    thumbnail = models.ImageField(upload_to='photos/%Y/%m/%d/')
    excerpt = models.CharField(max_length=80)
    year = models.CharField(max_length=4, default="2023", blank=True)
    month = models.CharField(max_length=50, choices=BlogMonths.choices, default=BlogMonths.JANUARY, blank=True)
    day = models.CharField(max_length=2, default=1, blank=True)
    body = models.TextField()
    featured = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    published = models.BooleanField(default=False)
    photo_detailed = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    def save(self, *args, **kwargs):
        original_slug = slugify(self.title)
        queryset = BlogPost.objects.all().filter(slug__iexact=original_slug).count()

        count = 1
        slug = original_slug
        while (queryset):
            slug = original_slug + '-' + str(count)
            count += 1
            queryset = BlogPost.objects.all().filter(slug__iexact=slug).count()

        self.slug = slug

        if self.featured:
            try:
                temp = BlogPost.objects.get(featured=True)
                if self != temp:
                    temp.featured = False
                    temp.save()
            except BlogPost.DoesNotExist:
                pass

        super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
