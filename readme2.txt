docker run -p 3000:3000 dashboard

steps to create npx app:
1.-)    npx create-next-app@latest
2.-)    npm install @mui/material @emotion/react @emotion/styled
export:
3.-)    docker export 6782cbf5c6d1 -o dashboard.tar
4.-)    docker import dashboard.tar mydashboard:latest

docker image save --output IMAGE [IMAGE...]

1) based on the present dockerfile:
docker build --tag arithmetic .

2) run the image:
docker run arithmetic

3) list the containers:
docker container ls --all

4) export the container into tar file:
docker export container-id > arithmetic.tar

5) import into image:
docker import arithmetic.tar put_any_name_here:latest

6) run and enter shell:
docker run -i -t put_any_name_here:latest shell

>>>>>>>>>>>>>>>>>>
1) save as image:
docker save arithmetic > arm_image.tar

2) load an image:
docker load < arm_image.tar