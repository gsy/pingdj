from django.db import models


class TiMethod(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ManyToManyField('TiMethod', related_name='ti_method_parent', blank=True)
    level = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<TiMethod: {}>'.format(self.name)


class TiBenchResult(models.Model):
    method = models.ForeignKey(TiMethod, on_delete=models.CASCADE)
    key_length = models.IntegerField(default=0)
    value_length = models.IntegerField(default=0)
    avg = models.FloatField(default=0.0)
    min = models.FloatField(default=0.0)
    max = models.FloatField(default=0.0)
    ts = models.DateTimeField()

    def __str__(self):
        return 'BenchResult - {}'.format(self.method)

    def __repr__(self):
        return '<TiBenchResult: {}>'.format(self.method)
