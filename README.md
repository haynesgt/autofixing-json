I want to be able to write command line queries like this.

```
es-search query: must: exists: field: deleted :exists range: created_at: gt: 2020 :query size: 1000
```
