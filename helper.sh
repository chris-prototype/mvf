# Prepend project root to PYTHONPATH without overwriting existing paths
export PYTHONPATH="/home/runner/workspace${PYTHONPATH:+:$PYTHONPATH}"

addPP() {
  export PYTHONPATH="/home/runner/workspace${PYTHONPATH:+:$PYTHONPATH}"
}

# aliases
alias py='python'