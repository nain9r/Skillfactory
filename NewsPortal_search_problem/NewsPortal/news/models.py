from django.db import models
import django.contrib.auth


class Author(models.Model):
    author_id = models.OneToOneField(django.contrib.auth.get_user_model(), on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rate = 0
        posts_comments_rate = 0
        comments_rate = 0
        for p in Post.objects.filter(author=self):
            posts_rate += p.rating
            for pc in Comment.objects.filter(post=p.id):
                posts_comments_rate += pc.rating

        for ac in Comment.objects.filter(user=self.author_id):
            comments_rate += ac.rating

        self.rating = posts_rate * 3 + posts_comments_rate + comments_rate
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    NEWS = 'n'
    ARTICLE = 'a'

    POST_TYPE = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=POST_TYPE, default=ARTICLE)
    pub_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    text = models.TextField(default='')
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:125] + ('...' if len(self.text) > 124 else '')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(django.contrib.auth.get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(default='')
    pub_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
