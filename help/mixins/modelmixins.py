
class CategoryModelProperties:

    @property
    def featured_articles(self):
        articles = self.articlecategory_set.model.objects.filter(
            featured=True, category=self
        ).values_list('article_id')
        return self.article_set.model.objects.filter(id__in=articles)


class ArticleModelProperties:
    pass

class ArticleModelMethods:
    pass
