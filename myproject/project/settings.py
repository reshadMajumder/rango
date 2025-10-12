DATABASE_URL='sqlite://db.sqlite3'
TORTOISE_ORM={
    'connections':{'default': DATABASE_URL},
    'apps':{
        'models':{
            'models':['aerich.models',"apps.students.models"],
            'default_connection':'default'
            }
        }
}

INSTALLED_APPS = [
    "apps.students",
]
