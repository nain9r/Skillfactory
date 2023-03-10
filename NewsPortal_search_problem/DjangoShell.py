from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment

user1 = User.objects.create_user(username='author1')
user2 = User.objects.create_user(username='author2')

author1 = Author.objects.create(author_id=user1)
author2 = Author.objects.create(author_id=user2)

category1 = Category.objects.create(category='Наука')
category2 = Category.objects.create(category='В мире')
category3 = Category.objects.create(category='Кино')
category4 = Category.objects.create(category='Искусство')

post_a1 = Post.objects.create(
    author=author1,
    type='A',
    header='Невозможные объекты: в глубоком космосе найдены "разрушители Вселенной"',
    text='Астрономы заглянули в начало времен и увидели то, что противоречит'
         ' современным представлениям об устройстве Вселенной.',
)

post_a2 = Post.objects.create(
    author=author1,
    type='A',
    header='Что известно о продолжениях «Аватара»?',
    text='Сборы «Аватар: Путь воды» преодолели 2 млрд долларов, сиквел стал четвертым самым кассовым фильмом всех'
         ' времен и народов, и это значит, что франшиза с нами надолго. Съемки второй и третьей частей велись'
         ' параллельно, четвертая запущена в разработку. «Аватар 3» должен выйти 20 декабря 2024-го,'
         ' «Аватар 4» — 18 декабря 2026-го, «Аватар 5» — 22 декабря 2028-го.',
)

post_n1 = Post.objects.create(
    author=author2,
    type='N',
    header='«Кит» с Бренданом Фрейзером собрал в кинотеатрах 30 млн долларов ',
    text='Инди-драма «Кит» Даррена Аронофски превзошла ожидания и смогла освоить в мировом прокате 30 млн долларов.'
         ' Это сумма в десять раз превышает изначальный бюджет ленты — $3 млн.',
)

a1_cat_1 = PostCategory.objects.create(post=post_a1, category=category1)
a1_cat_2 = PostCategory.objects.create(post=post_a1, category=category2)
a2_cat_1 = PostCategory.objects.create(post=post_a2, category=category3)
a2_cat_2 = PostCategory.objects.create(post=post_a2, category=category4)
n1_cat_1 = PostCategory.objects.create(post=post_n1, category=category2)
n1_cat_2 = PostCategory.objects.create(post=post_n1, category=category3)

com1 = Comment.objects.create(post=post_a1, user=user1, text='Очередные "разрушители Вселенной"'
                                                             '... Сколько таких уже находили?')
com2 = Comment.objects.create(post=post_a1, user=user2, text='Как интересно!')
com3 = Comment.objects.create(post=post_a2, user=user2, text='А про что там? Про синих человечков же?')
com4 = Comment.objects.create(post=post_n1, user=user1, text='Очень годное кино, говорят. Надо смотреть')


post_a1.like()
post_a1.dislike()
post_a2.like()
post_a2.like()
post_a2.like()
post_n1.like()
post_n1.dislike()
com1.like()
com1.like()
com2.like()
com2.dislike()
com3.dislike()
com4.like()
com4.dislike()


author1.update_rating()
author2.update_rating()


best_author = Author.objects.all().order_by('-rating')[0]
print(f'Лучший автор: {best_author.author_id.username}, его рейтинг: {best_author.rating}')


best_article = Post.objects.order_by('-rating')[0]
print('Дата:', best_article.pub_date)
print('Автор:', best_author.author_id.username)
print('Рейтинг:', best_article.rating)
print('Заголовок:', best_article.header)
print('Превью:', best_article.preview())


comments = Comment.objects.filter(post=best_article)
for c in comments:
    print('Дата комментария:', c.pub_date)
    print('Автор:', c.user)
    print('Рейтинг:', c.rating)
    print('Текст:', c.text)
