from flask_restful import fields
from datetime import datetime


def date_format(date):
    return date.strftime('%d-%m-%Y') if date else None

section = {
    "id":fields.Integer,
    "name":fields.String,
    "date_created":fields.String(attribute=lambda x:date_format(x.date_created)),
    "description":fields.String,
    "image":fields.String

}

sections = {
    "sections":fields.List(fields.Nested(section))
}