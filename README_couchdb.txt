fauxton:
http://localhost:5984/_utils/
http://localhost:6984/_utils/

dashboard
Jimena1000

{
  "_id": "_design/trx",
  "_rev": "13-4d65f0f4f5b77ac5e520d14bb005c012",
  "views": {
    "by_fields": {
      "map": "function(doc) {\r\n  if(doc.type && doc.method) {\r\n    emit([doc.type, doc.method], doc);\r\n  }\r\n}\r\n"
    }
  },
  "language": "javascript"
}