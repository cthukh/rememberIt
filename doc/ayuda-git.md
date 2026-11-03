# Git: comandos de uso diario

Guía rápida: cada comando, qué hace y un ejemplo.

## Empezar

### `git init`
Convierte la carpeta actual en un repositorio de git.
```bash
cd ~/mi-proyecto
git init
```

### `git clone`
Descarga un repositorio completo desde internet a tu PC.
```bash
git clone https://github.com/usuario/repo.git
```

## Día a día

### `git status`
Muestra qué archivos cambiaste, cuáles están listos para guardar y cuáles no. Es el que más vas a usar.
```bash
git status
```

### `git add`
Marca archivos para incluirlos en el próximo commit.
```bash
git add archivo.txt     # un archivo
git add .               # todo lo que cambió
```

### `git commit`
Guarda una "foto" de lo que marcaste con `git add`, con un mensaje que explica el cambio.
```bash
git commit -m "Agrego página de docker a la wiki"
```

### `git diff`
Muestra línea por línea qué cambiaste (antes de hacer `add`).
```bash
git diff
git diff archivo.txt
```

### `git log`
Muestra el historial de commits.
```bash
git log --oneline       # una línea por commit, más fácil de leer
git log --oneline -5    # solo los últimos 5
```

## Sincronizar con el remoto (GitHub, GitLab...)

### `git remote add`
Conecta tu repo local con uno en internet. Se hace una sola vez.
```bash
git remote add origin https://github.com/usuario/wiki.git
git remote -v           # ver a dónde está conectado
```

### `git push`
Sube tus commits al remoto.
```bash
git push origin main
git push -u origin main   # la primera vez: deja recordado el destino
```

### `git pull`
Baja los cambios del remoto y los une con tu copia local (hace `fetch` + `merge`).
```bash
git pull origin main
```

### `git fetch`
Solo baja los cambios del remoto, **sin** mezclarlos con tu trabajo. Sirve para mirar antes de unir.
```bash
git fetch origin
git log HEAD..origin/main --oneline   # ver qué hay nuevo
```

## Ramas

### `git branch`
Lista, crea o borra ramas.
```bash
git branch                # ver ramas
git branch prueba         # crear rama (sin cambiarte a ella)
git branch -d prueba      # borrar rama ya fusionada
```

### `git switch`
Cambia de rama.
```bash
git switch main
git switch -c nueva-idea  # crea la rama y se cambia a ella
```

### `git merge`
Une otra rama a la que estás parado ahora.
```bash
git switch main
git merge nueva-idea      # trae a main lo de nueva-idea
```
Si dos ramas tocaron la misma línea, git te avisa del **conflicto**: abre el archivo, elige qué dejar (borra las marcas `<<<<<<<`, `=======`, `>>>>>>>`), luego `git add archivo` y `git commit`.

## Deshacer cosas

### `git restore`
Descarta los cambios de un archivo y lo deja como en el último commit. **No se puede recuperar lo descartado.**
```bash
git restore archivo.txt
```

### `git restore --staged`
Saca un archivo de lo marcado con `add`, sin perder los cambios.
```bash
git restore --staged archivo.txt
```

### `git commit --amend`
Corrige el último commit (mensaje o archivos olvidados). Solo si todavía no hiciste `push`.
```bash
git commit --amend -m "Mensaje corregido"
```

### `git revert`
Crea un commit nuevo que deshace otro anterior. Es la forma segura, porque no borra historial.
```bash
git revert abc1234        # el código sale de git log --oneline
```

### `git reset`
Mueve la rama hacia atrás en el historial.
```bash
git reset --soft HEAD~1   # deshace el commit, conserva los cambios marcados
git reset HEAD~1          # deshace el commit, conserva los cambios sin marcar
git reset --hard HEAD~1   # deshace el commit Y borra los cambios (peligroso)
```

## Guardar cosas para después

### `git stash`
Guarda tus cambios en un cajón temporal y deja el directorio limpio. Útil si necesitas cambiar de rama sin hacer commit.
```bash
git stash                 # guardar
git stash list            # ver lo guardado
git stash pop             # recuperar lo último y sacarlo del cajón
```

## Ignorar archivos

### `.gitignore`
Archivo en la raíz del repo con los nombres o patrones que git debe ignorar.
```
*.log
node_modules/
.env
```

## Ojo
- `git reset --hard` y `git restore` borran cambios sin vuelta atrás.
- No uses `--amend` ni `reset` sobre commits que ya subiste con `push`.