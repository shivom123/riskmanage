class Meta:
	pass

fields = {
    'first_name': models.CharField(max_length=255),
    'last_name': models.CharField(max_length=255),
}
attrs = {'__module__': "RiskApp", 'Meta': Meta}
if fields:
	attrs.update(fields)
model = type(name, (models.Model,), attrs)
model.__module__

