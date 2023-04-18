# Vocode hosted bot for EarnOS

To build;

```
docker build -t earnos-bot .
```

To run;

```
docker run -p 3001:3001 -e OPENAI_API_KEY=<your_openai_api_key> --name earnos-bot-instance earnos-bot
```
