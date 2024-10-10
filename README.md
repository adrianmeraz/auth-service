Troubleshooting

### Newest version of auth-service not found

#### Clear PyPi Cache

```
poetry cache clear pypi --all
```

#### Update package

```
poetry update py-aws-core
```

### Github Actions Setup

Go to Settings / Actions / General

Set ```Workflow Permissions``` to ```Read and write permissions```

Check ```Allow GitHub Actions to create and approve pull requests```

### Github Access Token Setup

Go to Settings / Developer Settings


Next, go to Personal access tokens / Tokens (classic)

Create new Token with following permissions:

* read:project
* read:public_key
* repo
* workflow
* write:discussion

Copy token somewhere to use later in GH_PAT environment variable