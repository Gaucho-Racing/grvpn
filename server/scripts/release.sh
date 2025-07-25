#!/bin/bash

set -a
. .env

# Get the version from config.go
VERSION=$(grep 'var Version =' config/config.go | cut -d '"' -f 2)

# Check if version was successfully extracted
if [ -z "$VERSION" ]
  then
    echo "Error: Could not extract version from config/config.go"
    exit 1
fi

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null
then
    echo "GitHub CLI (gh) is not installed. Please install it to proceed."
    exit 1
fi

# Check if goreleaser is installed
if ! command -v goreleaser &> /dev/null
then
    echo "goreleaser is not installed. Please install it to proceed."
    exit 1
fi

# Check if GITHUB_TOKEN is set
if [ -z "$GITHUB_TOKEN" ]
then
    echo "GITHUB_TOKEN is not set. Please set it to proceed."
    exit 1
fi

# Create a release tag
git tag -s v$VERSION -m "Release version $VERSION"
git push origin v$VERSION

# Create a release
goreleaser release --clean

echo "Package released successfully for version $VERSION"