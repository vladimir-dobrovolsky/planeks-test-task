# planeks-test-task

TL;DR: Everything works apart from:
- conditional display of input range in columns (should use some js there)
- 'start' range option for a number of sentences in Text column type
- saving in media folder on heroku - I'm quite certain it's read-only, so I went with AWS S3 instead

Also, there's a row limit (100 max) for generated files in generate_data_set() in models.py (just in case).

Thanks for the test task, fiddled with a lot of things I planned to learn about.

Given more time I'd also write tests and use JavaScript + REST APIs for schema editing pages instead of Django's form views.
