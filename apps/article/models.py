from django.db import models
import markdown

from material.models import MaterialCategory, MaterialTag, PostBaseInfo
from utils.RelativeImageExtension import RelativeImageExtension
from BlogBackendProject.settings import MEDIA_URL_PREFIX


class ArticleInfo(PostBaseInfo):
    """
    文章基本信息
    """

    def save(self, *args, **kwargs):
        self.post_type = 'article'
        super(ArticleInfo, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name + '列表'


class ArticleDetail(models.Model):
    """
    文章详细信息
    """
    article_info = models.ForeignKey(ArticleInfo, null=True, blank=True, related_name='details', verbose_name="内容",
                                     help_text="内容")
    origin_content = models.TextField(null=False, blank=False, verbose_name="原始内容", help_text="原始内容")
    formatted_content = models.TextField(verbose_name="处理后内容", help_text="处理后内容")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="修改时间",
                                       help_text="修改时间")

    def save(self, *args, **kwargs):
        self.formatted_content = markdown.markdown(self.origin_content,
                                                   extensions=[
                                                       'markdown.extensions.extra',
                                                       'markdown.extensions.abbr',
                                                       'markdown.extensions.attr_list',
                                                       'markdown.extensions.def_list',
                                                       'markdown.extensions.fenced_code',
                                                       'markdown.extensions.footnotes',
                                                       'markdown.extensions.tables',
                                                       'markdown.extensions.smart_strong',
                                                       'markdown.extensions.admonition',
                                                       'markdown.extensions.codehilite',
                                                       'markdown.extensions.headerid',
                                                       'markdown.extensions.meta',
                                                       'markdown.extensions.nl2br',
                                                       'markdown.extensions.sane_lists',
                                                       'markdown.extensions.smarty',
                                                       'markdown.extensions.toc',
                                                       'markdown.extensions.wikilinks',
                                                       RelativeImageExtension({
                                                           'base_urls': [
                                                               MEDIA_URL_PREFIX
                                                           ]
                                                       })
                                                   ], lazy_ol=False)
        super(ArticleDetail, self).save(*args, **kwargs)

    def __str__(self):
        return self.article_info.title

    class Meta:
        verbose_name = "文章详情"
        verbose_name_plural = verbose_name + '列表'
