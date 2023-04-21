# clash-parser-server
> A server to parser clash configuration

Parse clash configuration for those clash clients which don't support parsers.

## Dependencies
- flask
- requests
- PyYAML

## Usage
### Deploy through docker
Edit `parsers_url` in `docker-compose.yml` and deploy using docker-compose.
Or add it to your docker-compose configuration.

### Deploy directly
```sh
export parsers=%YOUR_PARSERS_URL
flask run -p 8080 -h 0.0.0.0
```

### Parsers style
For now only support json type parsers file.

And only support parsers for
- rules
- proxy-groups
- command( only able to set proxies for groups )

The example file is [here](https://gist.github.com/hlf20010508/06b75d34b2366d14636e599814fe5002)

```json
{
    "rules": [
        "DOMAIN-SUFFIX,example.com,DIRECT"
    ],
    "proxy_groups": [
        {
            "name": "EXAMPLE1",
            "type": "select"
        },
        {
            "name": "EXAMPLE2",
            "type": "url-test",
            "url": "http://www.gstatic.com/generate_204",
            "interval": 300,
            "lazy": true
        },
    ],
    "in_group_proxies": [
        {
            "name": "EXAMPLE",
            "proxies": {
                "include": [
                    "keyword1"
                ],
                "exclude": [
                    "keyword2"
                ]
            },
            "groups": [
                "group1",
                "group2"
            ]
        },
    ]
}
```

This is equal to

```yaml
parsers:
  - url: https://your_clash_url.com
    yaml:
      prepend-rules:
        - DOMAIN-SUFFIX,example.com,DIRECT
      append-proxy-groups:
        - name: EXAMPLE1
          type: select
        - name: EXAMPLE2
          type: url-test
          url: 'http://www.gstatic.com/generate_204'
          interval: 300
          lazy: true
      commands:
        - proxy-groups.EXAMPLE.proxies=[]groupNames|group1|group2
        - proxy-groups.EXAMPLE.proxies+[]proxyNames|^(?:(?!keyword2).)*?keyword1.*$  # this means add proxies whose name have keyword1 but don't have keyword2
```