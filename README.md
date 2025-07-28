# grvpn

[![build](https://github.com/Gaucho-Racing/grlink/actions/workflows/build.yml/badge.svg)](https://github.com/Gaucho-Racing/grlink/actions/workflows/build.yml)
[![Netlify Status](https://api.netlify.com/api/v1/badges/d9d24841-17a3-42c1-8aa0-634d8fd333e8/deploy-status)](https://app.netlify.com/sites/grlink/deploys)
[![Docker Pulls](https://img.shields.io/docker/pulls/gauchoracing/grlink?style=flat-square)](https://hub.docker.com/r/gauchoracing/grlink)
[![Release](https://img.shields.io/github/release/gaucho-racing/grlink.svg?style=flat-square)](https://github.com/gaucho-racing/grlink/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<div style="display: flex; gap: 10px;">
  <img src="assets/home.png" alt="GRLink Dashboard" width="49%" />
  <img src="assets/details.png" alt="GRLink Dashboard" width="49%" />
</div>

GRLink is Gaucho Racing's custom URL shortener.

Check out our wiki page [here](https://wiki.gauchoracing.com/books/grlink) to learn more.

## Getting Started

### Setup local database

Start by running SingleStore locally using the provided Docker image.

```
docker run \
    -d --name singlestoredb-dev \
    -e ROOT_PASSWORD="password" \
    -p 3306:3306 -p 8080:8080 -p 9000:9000 \
    ghcr.io/singlestore-labs/singlestoredb-dev:latest
```

Note the `--platform linux/amd64` instruction which is required when running on Apple Silicon.

```
docker run \
    -d --name singlestoredb-dev \
    -e ROOT_PASSWORD="password" \
    --platform linux/amd64 \
    -p 3306:3306 -p 8080:8080 -p 9000:9000 \
    ghcr.io/singlestore-labs/singlestoredb-dev:latest
```

Once running, create the `grlink` database that the application is going to use. You can do this by executing the following command from the Studio UI (accessible at http://localhost:8080).

```sql
CREATE DATABASE grlink;
```

### Configure environment variables

Create a `.env` file in the root level of the repository and copy in the following environemnt variables.

```
ENV=DEV
PORT=7000

DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=password
DATABASE_NAME=grlink

SENTINEL_URL=https://sentinel-api.gauchoracing.com
SENTINEL_JWKS_URL=https://sso.gauchoracing.com/.well-known/jwks.json
SENTINEL_CLIENT_ID=
SENTINEL_CLIENT_SECRET=
SENTINEL_TOKEN=
SENTINEL_REDIRECT_URI=http://localhost:5173/auth/login
```

Make sure to set the client id and secret for your application. If you don't have one already, you can create one through [Sentinel](https://sso.gauchoracing.com/applications).

### Start the backend

Make sure you have [Go](https://go.dev/) version [1.23](https://go.dev/doc/devel/release#go1.23.0) or above installed.

The following command will automatically install dependencies, source the `.env` file, and start the application.

```
make run
```

The backend should now be listening on `localhost:7000` (or whatever you set `PORT` to).

### Start the frontend

Navigate to the `web/` directory and execute the following.

```
npm install
npm run dev
```

Make sure to update the `SENTINEL_CLIENT_ID` and `BACKEND_URL` values in `src/consts/config.tsx`.

Open [http://localhost:5173](http://localhost:5173) with your browser to see the result.

## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b gh-username/my-amazing-feature`)
3. Commit your Changes (`git commit -m 'Add my amazing feature'`)
4. Push to the Branch (`git push origin gh-username/my-amazing-feature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.
