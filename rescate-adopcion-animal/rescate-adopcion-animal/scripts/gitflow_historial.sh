#!/usr/bin/env bash
# Reproduce el historial Gitflow del proyecto (main, develop, feature/*, release/*, hotfix/*).
# Uso:  bash scripts/gitflow_historial.sh
# Requisitos: git >= 2.28 y user.name / user.email configurados.
set -euo pipefail
cd "$(dirname "$0")/.."

[ -d .git ] && { echo "Ya existe un repositorio Git en esta carpeta."; exit 1; }
git config user.name  >/dev/null || { echo "Configura: git config --global user.name  \"Tu Nombre\"";  exit 1; }
git config user.email >/dev/null || { echo "Configura: git config --global user.email \"tu@correo.com\""; exit 1; }

# Línea final opcional de los mensajes de commit (déjala vacía si no la quieres).
TRAILER="Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"

msg() { if [ -n "$TRAILER" ]; then printf '%s\n\n%s' "$1" "$TRAILER"; else printf '%s' "$1"; fi; }
commit() { git commit -q -m "$(msg "$1")"; }

# Ejecuta una rama feature completa: crea desde develop, commitea y fusiona con --no-ff
# feature <nombre> <mensaje> <archivos...>
feature() {
  local nombre="$1" mensaje="$2"; shift 2
  git checkout -q -b "feature/$nombre" develop
  git add "$@"
  commit "$mensaje"
  git checkout -q develop
  git merge -q --no-ff "feature/$nombre" -m "$(msg "Merge branch 'feature/$nombre' into develop")"
  git branch -q -d "feature/$nombre"
  echo "  feature/$nombre  -> develop"
}

echo "== main: commit inicial =="
git init -q -b main
git add README.md .gitignore
commit "chore: commit inicial del repositorio"

echo "== develop =="
git checkout -q -b develop

echo "== features =="
feature analisis-requerimientos "docs: análisis de actores y requerimientos del sistema" docs/analisis.md
feature diagrama-casos-uso      "docs(uml): diagrama de casos de uso"                    docs/diagrams/casos_uso.dot docs/diagrams/casos_uso.png
feature diagrama-clases         "docs(uml): diagrama de clases del dominio"              docs/diagrams/clases.dot docs/diagrams/clases.png
feature patron-factory          "feat(factory): Factory Method para el registro de animales" \
        src/rescate_adopcion/__init__.py src/rescate_adopcion/animal.py src/rescate_adopcion/factory.py \
        docs/diagrams/patron_factory.dot docs/diagrams/patron_factory.png
feature patron-adapter          "feat(adapter): Adapter para notificaciones por correo y SMS" \
        src/rescate_adopcion/notificacion.py docs/diagrams/patron_adapter.dot docs/diagrams/patron_adapter.png
feature patron-observer         "feat(observer): Observer para cambios de estado de solicitudes" \
        src/rescate_adopcion/solicitud.py src/rescate_adopcion/observadores.py \
        docs/diagrams/patron_observer.dot docs/diagrams/patron_observer.png

echo "== release/1.0.0 =="
git checkout -q -b release/1.0.0 develop
git add src/main.py tests/test_patrones.py
commit "test: pruebas unitarias y demo de los tres patrones"
git add docs/diagrams/gitflow.png scripts/gitflow_historial.sh
commit "docs: diagrama Gitflow y script del historial"
git checkout -q main
git merge -q --no-ff release/1.0.0 -m "$(msg "Merge branch 'release/1.0.0'")"
git tag -a v1.0.0 -m "Versión 1.0.0: diseño completo con tres patrones"
git checkout -q develop
git merge -q --no-ff release/1.0.0 -m "$(msg "Merge branch 'release/1.0.0' into develop")"
git branch -q -d release/1.0.0

echo "== hotfix/1.0.1 =="
git checkout -q -b hotfix/1.0.1 main
cat >> README.md <<'EOF'

## Pruebas

```bash
python -m unittest discover -s tests
```
EOF
git add README.md
commit "fix(docs): agregar instrucciones para ejecutar las pruebas"
git checkout -q main
git merge -q --no-ff hotfix/1.0.1 -m "$(msg "Merge branch 'hotfix/1.0.1'")"
git tag -a v1.0.1 -m "Versión 1.0.1: documentación de pruebas"
git checkout -q develop
git merge -q --no-ff hotfix/1.0.1 -m "$(msg "Merge branch 'hotfix/1.0.1' into develop")"
git branch -q -d hotfix/1.0.1

echo
git log --graph --oneline --decorate --all
echo
echo "Listo. Para publicarlo en GitHub (repositorio vacío creado en la web):"
echo "  git remote add origin https://github.com/<tu-usuario>/rescate-adopcion-animal.git"
echo "  git push -u origin --all"
echo "  git push origin --tags"
