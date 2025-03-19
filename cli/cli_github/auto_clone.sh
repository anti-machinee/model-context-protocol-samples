# only main branch
# need to extend to other branches
# need to handle errors in pull
# checkout back to main
# scan other branches

for repo in */*; do
  if [ -d "$repo/.git" ]; then
    echo "Pulling latest changes in $repo..."
    git -C "$repo" pull
  else
    echo "$repo is not a Git repository."
  fi
done
