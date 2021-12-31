#!/bin/sh

echo "Checking Semi-Linear History"

base_branch=$1

echo "Base Branch: $base_branch"

if git merge-base --is-ancestor origin/$base_branch HEAD; then
  echo "Semi-Linear history verified."
  return 0
fi
echo "So Semi linear history could be verified, check failed."
return 1
