echo "login to gitlab to push image"
docker login registry.gitlab.com/lpbt/lpbt

TAG=v0.lpbt.1

docker build ./bot -t lpbt/bot:$TAG
docker tag lpbt/bot:$TAG registry.gitlab.com/lpbt/lpbt/bot:$TAG

docker build ./backend -t lpbt/backend:$TAG
docker tag lpbt/backend:$TAG registry.gitlab.com/lpbt/lpbt/backend:$TAG

docker build ./frontend -t lpbt/frontend:$TAG
docker tag lpbt/frontend:$TAG registry.gitlab.com/lpbt/lpbt/frontend:$TAG

echo "pushing to gitlab"

docker push registry.gitlab.com/lpbt/lpbt/bot:$TAG
docker push registry.gitlab.com/lpbt/lpbt/backend:$TAG
docker push registry.gitlab.com/lpbt/lpbt/frontend:$TAG


