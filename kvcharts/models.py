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
    mean = models.FloatField(default=0.0)
    lower_bound = models.FloatField(default=0.0)
    upper_bound = models.FloatField(default=0.0)
    ts = models.DateTimeField()
    args = models.TextField(blank=True)
    estimates = models.TextField(blank=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'BenchResult - {}'.format(self.method)

    def __repr__(self):
        return '<TiBenchResult: {}>'.format(self.method)
