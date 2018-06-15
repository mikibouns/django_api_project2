from django.db import models
# from auth_app.models import User
from django.contrib.auth.models import User


class Sites(models.Model):
    class Meta:
        db_table = 'sites'

    name = models.CharField(max_length=150)
    addedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    siteDescription = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Persons(models.Model):
    class Meta:
        db_table = 'persons'

    name = models.CharField(max_length=150)
    addedBy = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Pages(models.Model):
    class Meta:
        db_table = 'pages'

    URL = models.CharField(max_length=150, unique=True)
    siteID = models.ForeignKey(Sites, on_delete=models.CASCADE)
    foundDateTime = models.DateTimeField(null=True, blank=True)
    lastScanDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.URL


class PersonsPageRank(models.Model):
    class Meta:
        db_table = 'personspagerank'

    PersonID = models.ForeignKey(Persons, on_delete=models.CASCADE, primary_key=True)
    PageID = models.ForeignKey(Pages, on_delete=models.CASCADE)
    Rank = models.IntegerField(blank=True)

    def __str__(self):
        return '<{}, {}>'.format(self.PersonID, self.PageID)


class Log(models.Model):
    class Meta:
        db_table = 'log'

    adminID = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=150)
    logDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<{}, {}>".format(self.adminID, self.action)


class KeyWords(models.Model):
    class Meta:
        db_table = 'keywords'

    personID = models.ForeignKey(Persons, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
