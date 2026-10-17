from mongoengine import connect

connect(
    host='mongodb://localhost:27017/biblioteca_virtual',
    alias='default'
)