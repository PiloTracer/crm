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