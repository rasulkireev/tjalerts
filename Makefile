
redis:
	redis-stack-server --port 6381

shell:
	poetry run python manage.py shell_plus --ipython

meili:
	meilisearch --master-key="NiuZMCgbfbajR-REAxTAnjW2MS2ftJnSWZBy9ChN-WI"
