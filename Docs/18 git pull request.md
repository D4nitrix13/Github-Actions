crear una rama para simulawr  una nueva funcionalidad

git switch -c add-new-feature
git add . <file-change>
git commit -m "Add new feature..."
crear cambios cualquiera solo para integrar subir y en la pull requesta añadir titutlo y descripcion
este

.github/workflows/python-tests.yml
podemos indicarlo con lista mediante [] o guiones -
ejemplo 1
on:
  push:
    branches: [master]
  pull_request:
    types: [opened, synchronize, reopened]

ejemplo 2

on:
  push:
    branches:
        - master
  pull_request:
    types:
      - opened
      - synchronize
      - reopened
