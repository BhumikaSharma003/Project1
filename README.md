#A. Write and share a small note about your choice of system to schedule periodic tasks (such as downloading a list of ISINs every 24 hours). Why did you choose it? Is it reliable enough; Or will it scale? If not, what are the problems with it? And, what else would you recommend to fix this problem at scale in production?
Answer: For scheduling periodic tasks my choice would be cron jobs or Celery with a task queue (e.g., Redis) and a scheduler like Celery Beat.
Cron jobs can be a problem for later production upgrades, due to which we can say better choice will be celery as it can handle multiple periodic and background tasks efficiently.
Beside that, redis is also reliable and well monitored but it can struggle with large tasks scheduling.
For lage scale production we can work on Kubernetes cromjobs or we can switch to cloud services like AWS.
#B. In what circumstances would you use Flask instead of Django and vice versa?
I would use flask for projects that are focused on requirements like lightweight development or that may need more flexiblity in devlopment. We can customise far more in flask than django. ALso it consumes lesser resources.
On the other hand, Django is used when we need to meet tight deadines, or we have to work on large, complex projects. Django comes with built in functionalities, like admin panel, authentication, ORM. Django also Provides protection against SQL injection, CSRF, XSS, and more.
#In Conclusion
Use Flask when you need a minimal, customizable API or microservice.
Use Django when you need a full-fledged web app with a database and built-in admin support.
