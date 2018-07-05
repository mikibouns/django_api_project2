from django.db import models
# from django.contrib.auth.models import User
from auth_app.models import User


class Sites(models.Model):
    class Meta:
        db_table = 'sites'

    name = models.CharField(max_length=150)
    addedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    siteDescription = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, request, name, siteDesc):
        new_person = cls(name=name, siteDescription=siteDesc, addedBy=request.user)
        return new_person

    def pages_children(self):
        '''метод для отображения содержимого поля ForeignKey'''
        return Pages.objects.filter(siteID=self)


class Persons(models.Model):
    class Meta:
        db_table = 'persons'

    name = models.CharField(max_length=150)
    addedBy = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def keywords_children(self):
        '''метод для отображения содержимого поля ForeignKey'''
        return KeyWords.objects.filter(personID=self)

    @classmethod
    def create(cls, request, person):
        new_person = cls(name=person, addedBy=request.user)
        return new_person


class Pages(models.Model):
    class Meta:
        db_table = 'pages'

    URL = models.CharField(max_length=150, unique=True)
    siteID = models.ForeignKey(Sites, on_delete=models.CASCADE)
    foundDateTime = models.DateTimeField(auto_now_add=True)
    lastScanDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.URL

    @classmethod
    def create(cls, request, urls, person):
        if isinstance(urls, str):
            urls = urls.replace(' ', '').split(',')
        urls_id = []
        for url in urls:
            new_url = cls(name=url, personID=person)
            new_url.save()
            urls_id.append({"id": new_url.id,
                             "name": new_url.name})
        return urls_id

class PersonsPageRank(models.Model):
    class Meta:
        db_table = 'personspagerank'

    personID = models.ForeignKey(Persons, on_delete=models.CASCADE)
    pageID = models.ForeignKey(Pages, on_delete=models.CASCADE)
    rank = models.IntegerField(blank=True)

    def __str__(self):
        return '<{}, {}>'.format(self.personID, self.pageID)

    def persons_children(self):
        return Persons.objects.filter(id=self.personID.id)

    def pages_children(self):
        return Pages.objects.filter(id=self.id)

    def sites_children(self):
        return Sites.objects.filter(id=self.pageID.siteID.id)


class Log(models.Model):
    class Meta:
        db_table = 'log'

    adminID = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=150)
    logDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<{}, {}>".format(self.adminID, self.action)


class KeyWords(models.Model):
    class Meta:
        db_table = 'keywords'

    personID = models.ForeignKey(Persons, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, request, words, person):
        if isinstance(words, str):
            words = words.replace(' ', '').split(',')
        words_id = []
        for word in words:
            new_word = cls(name=word, personID=person)
            new_word.save()
            words_id.append({"id": new_word.id,
                             "name": new_word.name})
        return words_id