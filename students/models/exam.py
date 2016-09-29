# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

class Exam(models.Model):
    """Exams Model"""

    class Meta(object):
        """ Admin  represent"""
        verbose_name = u"Іспит"
        verbose_name_plural = u"Іспити"

    subject = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва Предмету")

    date_time =  models.DateTimeField(
        auto_now_add=False,
        auto_now=False,
        verbose_name=u"Дата проведення")

    teacher = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Викладач")

    exam_group = models.ForeignKey('Group',
        blank=False,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=u"Група")

    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки")

    def __unicode__(self):
        """ Admin  represent"""
        return u"%s %s (%s)" % (self.subject, self.teacher, self.exam_group)

